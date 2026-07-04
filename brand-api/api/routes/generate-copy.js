// POST /brand/generate-copy — gera copy on-brand via LLM
import { generateCopy } from '../lib/llm-generator.js';

export default async function generateCopyRoutes(fastify) {
  fastify.post('/brand/generate-copy', async (req, reply) => {
    const { brief, template, format, audience } = req.body || {};
    if (!brief) {
      reply.code(400);
      return { error: 'invalid_input', message: 'Body precisa { brief: string, template?: string, format?: "story"|"caption"|"both", audience?: string }' };
    }
    try {
      const result = await generateCopy({ brief, template, format, audience });
      return result;
    } catch (err) {
      fastify.log.error(err);
      reply.code(err.message.includes('ANTHROPIC_API_KEY') ? 503 : 500);
      return { error: 'generation_failed', message: err.message };
    }
  });
}
