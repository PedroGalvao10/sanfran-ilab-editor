// POST /brand/validate — valida copy contra regras
import { validateCopy } from '../lib/validator.js';

export default async function validateRoutes(fastify) {
  fastify.post('/brand/validate', async (req, reply) => {
    const { text, context } = req.body || {};
    if (!text || typeof text !== 'string') {
      reply.code(400);
      return { error: 'invalid_input', message: 'Body deve conter { text: string, context?: { type } }' };
    }
    return validateCopy(text, context || {});
  });
}
