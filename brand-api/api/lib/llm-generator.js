// === LLM generator: gera copy on-brand via Anthropic SDK ===
// Usa prompt caching (cache_control) no system prompt do brand
// para evitar recomputar o contexto a cada chamada.

import Anthropic from '@anthropic-ai/sdk';
import { buildSystemPrompt } from './prompt-builder.js';
import { validateCopy } from './validator.js';
import { loadBrand, getTemplate } from './brand-loader.js';

let client = null;
function getClient() {
  if (client) return client;
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) throw new Error('ANTHROPIC_API_KEY não configurada no .env');
  client = new Anthropic({ apiKey });
  return client;
}

const MODEL = process.env.ANTHROPIC_MODEL || 'claude-sonnet-4-5-20250929';

/**
 * Gera copy on-brand a partir de um brief.
 * @param {object} opts
 * @param {string} opts.brief - Descrição do que precisa ser comunicado
 * @param {string} [opts.template] - Template alvo (encontro, dica, etc)
 * @param {string} [opts.format] - 'story' | 'caption' | 'both' (default: 'both')
 * @param {string} [opts.audience] - Público-alvo opcional
 * @returns {Promise<object>} { caption, story_title, story_desc, suggested_template, suggested_hashtags, validation }
 */
export async function generateCopy({ brief, template, format = 'both', audience }) {
  if (!brief || typeof brief !== 'string') throw new Error('Parâmetro "brief" obrigatório');

  const anthropic = getClient();
  const brand = loadBrand();
  const tplInfo = template ? getTemplate(template) : null;

  // System prompt do brand (este é o conteúdo CACHEADO)
  const systemPromptBrand = buildSystemPrompt();

  // Instruções específicas da task (NÃO cacheadas — variam por requisição)
  const userPrompt = buildUserPrompt({ brief, template, tplInfo, format, audience });

  const response = await anthropic.messages.create({
    model: MODEL,
    max_tokens: 1500,
    system: [
      {
        type: 'text',
        text: systemPromptBrand,
        cache_control: { type: 'ephemeral' }  // ← prompt caching habilitado
      },
      {
        type: 'text',
        text: 'Você SEMPRE responde com JSON válido seguindo o schema solicitado. Sem markdown, sem ```json, apenas o objeto JSON puro.'
      }
    ],
    messages: [{ role: 'user', content: userPrompt }]
  });

  const text = response.content[0]?.text || '';
  const parsed = parseJSONResponse(text);

  // Auto-valida a caption gerada
  if (parsed.caption) {
    parsed.validation = validateCopy(parsed.caption, { type: 'caption' });
  }

  // Adiciona metadados
  parsed._meta = {
    model: MODEL,
    cache_read_input_tokens: response.usage?.cache_read_input_tokens || 0,
    cache_creation_input_tokens: response.usage?.cache_creation_input_tokens || 0,
    input_tokens: response.usage?.input_tokens || 0,
    output_tokens: response.usage?.output_tokens || 0
  };

  return parsed;
}

function buildUserPrompt({ brief, template, tplInfo, format, audience }) {
  const parts = [];

  parts.push(`# Briefing\n${brief}`);
  if (audience) parts.push(`\n# Público-alvo\n${audience}`);

  if (template && tplInfo) {
    parts.push(`\n# Template alvo: ${template} (${tplInfo.name})`);
    parts.push(`Caso de uso: ${tplInfo.useCase}`);
    parts.push(`Campos do template: ${tplInfo.fields.join(', ')}`);
  } else {
    parts.push(`\n# Templates disponíveis (sugira o melhor)`);
    parts.push(Object.entries(loadBrand().templates).map(([id, t]) => `- ${id}: ${t.useCase}`).join('\n'));
  }

  parts.push(`\n# Formato de saída esperado`);
  parts.push(`Responda APENAS um JSON com:`);

  const schema = {
    suggested_template: 'string — id de um dos 8 templates',
    suggested_hashtags: ['array de 3-5 hashtags incluindo pelo menos 1 core']
  };

  if (format === 'story' || format === 'both') {
    schema.story_title = 'string — 2-8 palavras, força bruta, sem ponto final';
    schema.story_desc = 'string — máx 25 palavras se aplicável ao template';
    schema.story_fields = 'object — chaves correspondendo aos campos do template (ex: badge, title, meta, etc)';
  }
  if (format === 'caption' || format === 'both') {
    schema.caption = 'string — 80-600 chars, estrutura: provocação→dados→reflexão/CTA→hashtags';
  }

  parts.push('```json');
  parts.push(JSON.stringify(schema, null, 2));
  parts.push('```');

  parts.push(`\nRegras:`);
  parts.push(`- Aplique 100% as guidelines de tom acima`);
  parts.push(`- Hashtags: máx 5, incluir 1+ core`);
  parts.push(`- Sem clichês motivacionais ou promessas absolutas`);
  parts.push(`- Use dados específicos quando o briefing permitir`);

  return parts.join('\n');
}

function parseJSONResponse(text) {
  // Tenta parse direto
  try {
    return JSON.parse(text);
  } catch {}
  // Tenta extrair JSON de markdown code block
  const match = text.match(/```(?:json)?\s*([\s\S]*?)\s*```/);
  if (match) {
    try { return JSON.parse(match[1]); } catch {}
  }
  // Tenta extrair primeiro objeto JSON
  const obj = text.match(/\{[\s\S]*\}/);
  if (obj) {
    try { return JSON.parse(obj[0]); } catch {}
  }
  throw new Error(`Resposta do LLM não é JSON parseável. Recebido: ${text.slice(0, 200)}...`);
}
