import { readDraft, listDrafts } from '../lib/draft-store.js';

export default async function draftsRoutes(fastify) {
  // Lista todos os rascunhos disponíveis no servidor
  fastify.get('/brand/drafts', async (req, reply) => {
    return listDrafts();
  });

  // Carrega um rascunho específico
  fastify.get('/brand/drafts/:id', async (req, reply) => {
    const draft = readDraft(req.params.id);
    if (!draft) {
      reply.code(404);
      return { error: 'not_found', message: 'Rascunho não encontrado ou expirado (TTL 24h).' };
    }
    return draft;
  });
}
