import { listAssets } from '../lib/assets-loader.js';

export default async function assetsRoutes(fastify) {
  fastify.get('/brand/assets', async (req, reply) => {
    const proto = req.headers['x-forwarded-proto'] || req.protocol;
    const host = req.headers.host;
    const baseUrl = `${proto}://${host}`;
    
    return listAssets(baseUrl);
  });
}
