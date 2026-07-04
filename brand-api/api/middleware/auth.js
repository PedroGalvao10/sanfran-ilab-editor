// === Middleware: Bearer token auth ===
// Leitura de guidelines é SEMPRE pública (IAs consomem livremente).
// Apenas endpoints sensíveis (geram custo ou efeito externo) exigem o token.

// Rotas que exigem Authorization: Bearer <BRAND_API_TOKEN>
const PROTECTED = [
  '/brand/generate-copy',     // consome tokens da Anthropic ($)
  '/brand/render-story',      // CPU pesada (Playwright)
  '/brand/instagram-info',    // expõe dados da conta IG
  '/brand/publish-instagram'  // publica conteúdo público (crítico)
];

function isProtected(url) {
  const path = url.split('?')[0];
  return PROTECTED.some((p) => path === p || path.startsWith(p + '/'));
}

// IMPORTANTE: chamar direto no escopo raiz — applyAuth(fastify) —
// e NÃO via fastify.register(), senão o hook fica encapsulado e não
// se aplica às rotas irmãs (a proteção fica inerte).
export function applyAuth(fastify) {
  fastify.addHook('onRequest', async (req, reply) => {
    // Só protege as rotas sensíveis — o resto é público
    if (!isProtected(req.url)) return;

    const expected = process.env.BRAND_API_TOKEN || process.env.API_KEY;
    if (!expected) {
      // Sem token configurado: bloqueia as rotas sensíveis por segurança
      return reply.code(503).send({
        error: 'not_configured',
        message: 'Este endpoint exige BRAND_API_TOKEN configurado no servidor. Endpoints de leitura (/brand/context, /brand/voice, etc.) seguem públicos.'
      });
    }

    const auth = req.headers.authorization || '';
    const token = auth.startsWith('Bearer ') ? auth.slice(7) : '';

    if (token !== expected) {
      return reply.code(401).send({ error: 'unauthorized', message: 'Token inválido ou ausente. Use header: Authorization: Bearer <token>' });
    }
  });
}
