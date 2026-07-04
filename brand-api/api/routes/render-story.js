// POST /brand/render-story — renderiza PNG 1080×1920 do template
import { renderStory } from '../lib/story-renderer.js';

// Vercel/serverless free tier não suporta Chromium full de forma confiável.
// RENDER_DISABLED=1 desliga o endpoint com mensagem amigável.
const RENDER_DISABLED = process.env.RENDER_DISABLED === '1';

export default async function renderStoryRoutes(fastify) {
  fastify.post('/brand/render-story', async (req, reply) => {
    const { template, fields, image_data_url, format } = req.body || {};

    if (RENDER_DISABLED) {
      reply.code(501);
      return {
        error: 'render_unavailable',
        message: 'Render server-side desativado neste ambiente (serverless free tier). Gere o PNG diretamente no brandbook (clique no story → editar → baixar) ou rode a API localmente/Railway para usar este endpoint.',
        alternatives: {
          brandbook: 'Abra index.html → seção Stories → clique no template → editar → baixar PNG',
          local: 'npm start localmente com Playwright instalado',
          fields_endpoint: 'GET /brand/templates/' + (template || ':id') + ' retorna os campos editáveis'
        }
      };
    }

    if (!template) {
      reply.code(400);
      return { error: 'invalid_input', message: 'Body precisa { template: string, fields?: object, image_data_url?: string, format?: "png"|"base64" }' };
    }
    try {
      const buf = await renderStory({ template, fields: fields || {}, image_data_url });
      if (format === 'base64') {
        return {
          template,
          format: 'png',
          width: 1080,
          height: 1920,
          base64: buf.toString('base64'),
          size_bytes: buf.length
        };
      }
      reply.header('Content-Type', 'image/png');
      reply.header('Content-Disposition', `inline; filename="ilab-story-${template}-${Date.now()}.png"`);
      return reply.send(buf);
    } catch (err) {
      fastify.log.error(err);
      reply.code(500);
      return { error: 'render_failed', message: err.message };
    }
  });
}
