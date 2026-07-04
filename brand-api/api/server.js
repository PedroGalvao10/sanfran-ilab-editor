// === SanFran iLab Brand API — Server entry ===
// Fastify server expondo guidelines de brand via REST.

import Fastify from 'fastify';
import cors from '@fastify/cors';
import { applyAuth } from './middleware/auth.js';
import contextRoutes from './routes/context.js';
import promptRoutes from './routes/prompt.js';
import templatesRoutes from './routes/templates.js';
import validateRoutes from './routes/validate.js';
import hashtagsRoutes from './routes/hashtags.js';
import voiceRoutes from './routes/voice.js';
import generateCopyRoutes from './routes/generate-copy.js';
import renderStoryRoutes from './routes/render-story.js';
import publishInstagramRoutes from './routes/publish-instagram.js';
import assetsRoutes from './routes/assets.js';
import draftsRoutes from './routes/drafts.js';
import fastifyStatic from '@fastify/static';
import path from 'path';
import { loadBrand } from './lib/brand-loader.js';
import { closeBrowser } from './lib/story-renderer.js';
import { cleanupStaleDrafts } from './lib/draft-store.js';
import mcpSseRoutes from './routes/mcp-sse.js';

const fastify = Fastify({
  logger: { level: process.env.LOG_LEVEL || 'info' },
  bodyLimit: 20 * 1024 * 1024  // 20MB — para image_data_url base64
});

// CORS aberto (necessário para clientes browser e n8n/Make)
await fastify.register(cors, { origin: true });

// Auth via Bearer token
applyAuth(fastify);

// Servidor de estáticos: mapeia public/assets (da raiz do brandbook) para a rota web /assets/
fastify.register(fastifyStatic, {
  root: path.resolve(process.cwd(), '../assets'),
  prefix: '/assets/', 
});

// === Rotas públicas ===
fastify.get('/', async () => {
  const b = loadBrand();
  return {
    name: 'SanFran iLab Brand API',
    version: b.version,
    description: 'Brand guidelines API para uso por IAs e automações',
    endpoints: [
      'GET  /brand/context        — JSON completo das guidelines',
      'GET  /brand/prompt         — System prompt pronto pra LLM',
      'GET  /brand/templates      — Lista de templates',
      'GET  /brand/templates/:id  — Template específico',
      'POST /brand/validate       — Valida copy contra brand',
      'GET  /brand/hashtags       — Hashtags aprovadas',
      'GET  /brand/voice          — Tom de voz, persona, DOs/DON\'Ts',
      'GET  /brand/assets         — Catálogo dinâmico de SVGs/PNGs',
      'POST /brand/generate-copy  — Gera copy on-brand via LLM',
      'POST /brand/render-story   — Renderiza PNG 1080×1920 do template',
      'GET  /brand/instagram-info — Info da conta IG conectada',
      'POST /brand/publish-instagram — Publica feed/story no Instagram',
      'GET  /brand/drafts/:id     — Consome (lê+apaga) um rascunho criado via MCP create_post_draft',
      'GET  /mcp/sse              — Conexão MCP remota via SSE (para IAs externas)'
    ],
    auth: process.env.API_KEY ? 'Bearer token required' : 'OPEN (dev mode — set API_KEY env)'
  };
});

fastify.get('/health', async () => ({ status: 'ok', timestamp: Date.now() }));

// === Rotas de brand ===
await fastify.register(contextRoutes);
await fastify.register(promptRoutes);
await fastify.register(templatesRoutes);
await fastify.register(validateRoutes);
await fastify.register(hashtagsRoutes);
await fastify.register(voiceRoutes);
await fastify.register(generateCopyRoutes);
await fastify.register(renderStoryRoutes);
await fastify.register(publishInstagramRoutes);
await fastify.register(assetsRoutes);
await fastify.register(draftsRoutes);
await fastify.register(mcpSseRoutes);

// Limpa rascunhos com mais de 24h que nunca foram abertos (evita acúmulo em disco)
try { cleanupStaleDrafts(); } catch (err) { fastify.log.warn(`Limpeza de rascunhos falhou: ${err.message}`); }

// Cleanup browser on shutdown
process.on('SIGTERM', async () => { await closeBrowser(); process.exit(0); });
process.on('SIGINT', async () => { await closeBrowser(); process.exit(0); });

// === Serverless handler (Vercel) ===
// Vercel importa este arquivo e usa o export default como handler.
// Só chama fastify.listen() em ambiente tradicional (local / Railway).
export default async function handler(req, res) {
  await fastify.ready();
  fastify.server.emit('request', req, res);
}

// === Start (local / Railway) ===
if (!process.env.VERCEL) {
  const PORT = parseInt(process.env.PORT || '3000', 10);
  const HOST = process.env.HOST || '0.0.0.0';
  try {
    await fastify.listen({ port: PORT, host: HOST });
    if (!process.env.BRAND_API_TOKEN && !process.env.API_KEY) {
      fastify.log.warn('⚠️  BRAND_API_TOKEN não configurado — rodando em modo aberto (apenas dev).');
    }
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
}
