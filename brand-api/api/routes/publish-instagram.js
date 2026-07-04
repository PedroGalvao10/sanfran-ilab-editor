// POST /brand/publish-instagram — publica direto no IG via Meta Graph API
// GET  /brand/instagram-info     — valida credenciais e retorna info da conta
import { publishToInstagram, getAccountInfo } from '../lib/instagram-publisher.js';
import { validateCopy } from '../lib/validator.js';

export default async function publishInstagramRoutes(fastify) {
  fastify.get('/brand/instagram-info', async (req, reply) => {
    try {
      const info = await getAccountInfo();
      return { connected: true, ...info };
    } catch (err) {
      reply.code(503);
      return { connected: false, error: err.message };
    }
  });

  fastify.post('/brand/publish-instagram', async (req, reply) => {
    const { image_url, caption, is_story, skip_validation } = req.body || {};
    if (!image_url || !caption) {
      reply.code(400);
      return { error: 'invalid_input', message: 'Body precisa { image_url: string, caption: string, is_story?: boolean, skip_validation?: boolean }' };
    }

    // Pré-validação do brand (a não ser que skip_validation)
    let validation = null;
    if (!skip_validation) {
      validation = validateCopy(caption, { type: 'caption' });
      if (!validation.valid) {
        reply.code(422);
        return {
          error: 'caption_off_brand',
          message: 'Caption não passou na validação do brand. Use { skip_validation: true } para ignorar.',
          validation
        };
      }
    }

    try {
      const result = await publishToInstagram({ image_url, caption, is_story: !!is_story });
      return { success: true, validation, ...result };
    } catch (err) {
      fastify.log.error(err);
      reply.code(500);
      return { error: 'publish_failed', message: err.message };
    }
  });
}
