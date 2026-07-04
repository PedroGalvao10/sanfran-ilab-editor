// GET /brand/prompt — retorna system prompt pronto pra injetar em LLM
import { buildSystemPrompt } from '../lib/prompt-builder.js';

export default async function promptRoutes(fastify) {
  fastify.get('/brand/prompt', async (req, reply) => {
    const lang = req.query.lang || 'pt';
    const format = req.query.format || 'text';
    const prompt = buildSystemPrompt(lang);

    if (format === 'json') {
      return { prompt, lang, length: prompt.length };
    }
    reply.header('Content-Type', 'text/plain; charset=utf-8');
    return prompt;
  });
}
