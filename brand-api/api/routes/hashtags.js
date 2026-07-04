// GET /brand/hashtags?category=...
import { getHashtags } from '../lib/brand-loader.js';

export default async function hashtagsRoutes(fastify) {
  fastify.get('/brand/hashtags', async (req, reply) => {
    const category = req.query.category;
    if (category) {
      const tags = getHashtags(category);
      if (!Array.isArray(tags)) {
        reply.code(404);
        return { error: 'not_found', message: `Categoria "${category}" não existe. Válidas: core, temas, eventos, conteudo.` };
      }
      return { category, count: tags.length, hashtags: tags };
    }
    return getHashtags();
  });
}
