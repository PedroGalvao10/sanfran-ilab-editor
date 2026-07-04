// GET /brand/context — retorna brand.json completo
import { loadBrand } from '../lib/brand-loader.js';

export default async function contextRoutes(fastify) {
  fastify.get('/brand/context', async (req, reply) => {
    return loadBrand();
  });
}
