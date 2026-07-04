import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

import { loadBrand, getTemplate, getHashtags } from '../lib/brand-loader.js';
import { buildSystemPrompt } from '../lib/prompt-builder.js';
import { validateCopy } from '../lib/validator.js';
import { listAssets } from '../lib/assets-loader.js';
import { saveDraft } from '../lib/draft-store.js';

// Base da URL pública do editor — em produção (Vercel/Railway) é o domínio;
// em dev local, porta 5051 ou 8080.
const EDITOR_BASE_URL = process.env.EDITOR_BASE_URL || 'http://localhost:5051';

// Gerenciamento de múltiplas sessões SSE
const sessions = new Map();

// --- Reutilizando ferramentas e handlers idênticos aos do stdio ---
const TOOLS = [
  {
    name: 'get_brand_context',
    description: 'Retorna as guidelines completas do brand SanFran iLab (identidade, cores, tipografia, voz, templates, hashtags, regras). Use ANTES de criar qualquer conteúdo para o iLab.',
    inputSchema: {
      type: 'object',
      properties: {
        format: { type: 'string', enum: ['json', 'prompt'], description: 'json = objeto completo · prompt = system prompt formatado pra LLM' }
      }
    }
  },
  {
    name: 'validate_copy',
    description: 'Valida um texto/copy contra as regras de brand do iLab. Retorna score 0-100 + lista de issues específicos (clichês, excesso de emojis, hashtags faltantes, tamanho, etc).',
    inputSchema: {
      type: 'object',
      properties: {
        text: { type: 'string', description: 'Texto a validar' },
        context_type: { type: 'string', enum: ['caption', 'story_title', 'story_desc'], description: 'Tipo de copy (default: caption)' }
      },
      required: ['text']
    }
  },
  {
    name: 'get_story_template',
    description: 'Retorna os detalhes de um template de Story do iLab: nome, useCase, campos editáveis. Templates disponíveis: encontro, novidade, reel, artigo, pessoa, dado, chamada, dica.',
    inputSchema: {
      type: 'object',
      properties: {
        id: { type: 'string', description: 'ID do template (ex: "dica", "artigo")' }
      },
      required: ['id']
    }
  },
  {
    name: 'list_hashtags',
    description: 'Lista hashtags aprovadas pelo brand iLab. Sem categoria = retorna todas agrupadas. Com categoria = retorna só uma (core, temas, eventos, conteudo).',
    inputSchema: {
      type: 'object',
      properties: {
        category: { type: 'string', enum: ['core', 'temas', 'eventos', 'conteudo'], description: 'Filtra por categoria (opcional)' }
      }
    }
  },
  {
    name: 'get_voice_guidelines',
    description: 'Retorna tom de voz, persona, DOs e DONTs, e exemplos de copy on-brand vs off-brand. Use ANTES de escrever qualquer texto para o iLab.',
    inputSchema: { type: 'object', properties: {} }
  },
  {
    name: 'list_assets',
    description: 'Retorna o catálogo completo de todas as imagens brutas, ícones, logos, mascotes e elementos 3D do iLab. Retorna as categorias e as URLs estáticas prontas para download/uso pela IA.',
    inputSchema: { type: 'object', properties: {} }
  },
  {
    name: 'get_brand_colors',
    description: 'Retorna APENAS as cores (design tokens) e gradientes primários e neutros para montar designs com HTML/CSS ou SVG do zero.',
    inputSchema: { type: 'object', properties: {} }
  },
  {
    name: 'create_post_draft',
    description: 'Monta um rascunho de post num template do iLab. IMPORTANTE: Você DEVE respeitar as regras de design e composição visual definidas no brand.json ao usar decorations (máx 3-5 decorações, opacidade baixa para backgrounds, não sobrepor texto, etc). Cada campo de texto é validado contra as regras de brand ANTES de criar o rascunho.',
    inputSchema: {
      type: 'object',
      properties: {
        template_id: { type: 'string', description: 'ID do template (use get_story_template pra ver os campos de cada um): encontro, novidade, reel, artigo, pessoa, dado, chamada, dica, feed_carrossel, video_reel' },
        fields: {
          type: 'object',
          description: 'Mapa {nome_do_campo: texto}. Os nomes de campo são os mesmos retornados por get_story_template (ex: "title", "cta", "handle"). Campos não reconhecidos pelo template são ignorados.',
          additionalProperties: { type: 'string' }
        },
        photo_url: { type: 'string', description: 'URL de uma imagem (ex: vinda de list_assets) pra preencher o slot de foto do template, se ele tiver um (hasPhoto:true). Opcional.' },
        decorations: { 
            type: 'array', 
            description: 'Array opcional de imagens decorativas (ex: SVGs tech, logos, ícones 3D) para espalhar pela arte (posição absoluta).',
            items: { 
                type: 'object', 
                properties: { 
                    url: { type: 'string' }, x: { type: 'number' }, y: { type: 'number' }, width: { type: 'number' }, height: { type: 'number' }, opacity: { type: 'number' }, name: { type: 'string' }
                }, required: ['url', 'x', 'y', 'width', 'height']
            }
        }
      },
      required: ['template_id', 'fields']
    }
  }
];

function createMCPServer(sessionId) {
  const server = new Server(
    { name: `sanfran-ilab-brand-sse-${sessionId}`, version: '1.0.0' },
    { capabilities: { tools: {} } }
  );

  server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: TOOLS }));

  server.setRequestHandler(CallToolRequestSchema, async (req) => {
    const { name, arguments: args = {} } = req.params;
    try {
      switch (name) {
        case 'get_brand_context': {
          const format = args.format || 'json';
          if (format === 'prompt') {
            return { content: [{ type: 'text', text: buildSystemPrompt() }] };
          }
          return { content: [{ type: 'text', text: JSON.stringify(loadBrand(), null, 2) }] };
        }
        case 'validate_copy': {
          if (!args.text) throw new Error('Parâmetro "text" obrigatório');
          const result = validateCopy(args.text, { type: args.context_type });
          return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
        }
        case 'get_story_template': {
          if (!args.id) throw new Error('Parâmetro "id" obrigatório');
          const tpl = getTemplate(args.id);
          if (!tpl) {
            return { content: [{ type: 'text', text: `Template "${args.id}" não existe.` }], isError: true };
          }
          return { content: [{ type: 'text', text: JSON.stringify({ id: args.id, ...tpl }, null, 2) }] };
        }
        case 'list_hashtags': {
          const result = args.category ? { category: args.category, hashtags: getHashtags(args.category) } : getHashtags();
          return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
        }
        case 'get_voice_guidelines': {
          return { content: [{ type: 'text', text: JSON.stringify(loadBrand().voice, null, 2) }] };
        }
        case 'list_assets': {
          const assets = listAssets('');
          return { content: [{ type: 'text', text: JSON.stringify(assets, null, 2) }] };
        }
        case 'get_brand_colors': {
          const colors = loadBrand().colors;
          return { content: [{ type: 'text', text: JSON.stringify(colors, null, 2) }] };
        }
        case 'create_post_draft': {
          if (!args.template_id) throw new Error('Parâmetro "template_id" obrigatório');
          if (!args.fields || typeof args.fields !== 'object') throw new Error('Parâmetro "fields" obrigatório');

          const tpl = getTemplate(args.template_id);
          if (!tpl) {
            return { content: [{ type: 'text', text: `Template "${args.template_id}" não existe.` }], isError: true };
          }

          const validFields = {};
          for (const key of tpl.fields || []) {
            if (args.fields[key] !== undefined) validFields[key] = args.fields[key];
          }

          const allIssues = [];
          for (const [key, text] of Object.entries(validFields)) {
            const result = validateCopy(String(text), { type: 'story_title' });
            const errors = (result.issues || []).filter(i => i.severity === 'error');
            if (errors.length > 0) allIssues.push({ field: key, issues: errors });
          }
          if (allIssues.length > 0) {
            return {
              content: [{ type: 'text', text: JSON.stringify({ error: 'validation_failed', fields: allIssues }, null, 2) }],
              isError: true
            };
          }

          const draftId = saveDraft({ templateId: args.template_id, fields: validFields, photoUrl: args.photo_url || null, decorations: args.decorations || [] });
          const editorUrl = `${EDITOR_BASE_URL}/editor-pro.html?draft=${draftId}`;
          return {
            content: [{ type: 'text', text: JSON.stringify({ draftId, editorUrl, note: 'Link de uso único.' }, null, 2) }]
          };
        }
        default:
          return { content: [{ type: 'text', text: `Tool desconhecida: ${name}` }], isError: true };
      }
    } catch (err) {
      return { content: [{ type: 'text', text: `Erro: ${err.message}` }], isError: true };
    }
  });

  return server;
}

export default async function mcpSseRoutes(fastify) {
  // Rota GET /mcp/sse - inicia uma conexão e anexa um transport
  fastify.get('/mcp/sse', async (req, reply) => {
    // Apenas passamos o endpoint base (/mcp/messages). O SSEServerTransport 
    // anexa sozinho um ?sessionId=... (gerado internamente) à URL enviada para o cliente.
    const transport = new SSEServerTransport('/mcp/messages', reply.raw);

    // Agora pegamos o ID *real* que o transport gerou e usou na URL
    const sessionId = transport.sessionId;

    const mcpServer = createMCPServer(sessionId);
    await mcpServer.connect(transport);
    
    sessions.set(sessionId, transport);
    
    transport.onclose = () => {
      sessions.delete(sessionId);
    };
    
    // SSEServerTransport assume controle do response raw para streaming SSE
    reply.hijack();
  });

  // Rota POST /mcp/messages - recebe mensagens do cliente
  fastify.post('/mcp/messages', async (req, reply) => {
    const { sessionId } = req.query;
    const transport = sessions.get(sessionId);
    
    if (!transport) {
      console.error(`[MCP POST] Session ${sessionId} not found!`);
      return reply.code(404).send({ error: 'Session not found' });
    }

    try {
      // Passa o req.body (que o Fastify já parseou) como argumento pro handlePostMessage.
      // E passa req.raw e reply.raw para compatibilidade da lib.
      await transport.handlePostMessage(req.raw, reply.raw, req.body);
    } catch (e) {
      console.error('Error handling post message:', e);
    }
  });
}
