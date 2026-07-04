// GET /brand/templates — lista
// GET /brand/templates/:id — detalhe
import { loadBrand, getTemplate } from '../lib/brand-loader.js';

export default async function templatesRoutes(fastify) {
  fastify.get('/brand/templates', async (req, reply) => {
    const brand = loadBrand();
    return {
      count: Object.keys(brand.templates).length,
      templates: brand.templates
    };
  });

  fastify.get('/brand/templates/:id', async (req, reply) => {
    const tpl = getTemplate(req.params.id);
    if (!tpl) {
      reply.code(404);
      return { error: 'not_found', message: `Template "${req.params.id}" não existe. Templates válidos: encontro, novidade, reel, artigo, pessoa, dado, chamada, dica.` };
    }
    return { id: req.params.id, ...tpl };
  });
}
