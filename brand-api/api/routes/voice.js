// GET /brand/voice — tom, persona, DOs e DON'Ts
import { loadBrand } from '../lib/brand-loader.js';

export default async function voiceRoutes(fastify) {
  fastify.get('/brand/voice', async (req, reply) => {
    const brand = loadBrand();
    return brand.voice;
  });
}
