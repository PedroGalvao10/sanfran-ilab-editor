// === Instagram Publisher — Meta Graph API ===
// Fluxo oficial de publicação:
// 1. POST /{ig-user-id}/media           → cria container (image_url + caption)
// 2. GET  /{container_id}?fields=status → aguarda FINISHED
// 3. POST /{ig-user-id}/media_publish   → publica com creation_id
//
// REQUISITOS:
// - image_url precisa ser HTTPS público (Meta busca direto)
// - IG_USER_ID = ID da conta business/creator
// - META_ACCESS_TOKEN com permissões: instagram_basic, instagram_content_publish, pages_show_list
//
// Documentação: https://developers.facebook.com/docs/instagram-api/guides/content-publishing

const GRAPH_API = 'https://graph.facebook.com/v21.0';

function requireCreds() {
  const token = process.env.META_ACCESS_TOKEN;
  const igUserId = process.env.IG_USER_ID;
  if (!token) throw new Error('META_ACCESS_TOKEN não configurada');
  if (!igUserId) throw new Error('IG_USER_ID não configurado');
  return { token, igUserId };
}

async function metaRequest(path, opts = {}) {
  const { token } = requireCreds();
  const url = new URL(`${GRAPH_API}${path}`);
  url.searchParams.set('access_token', token);

  const res = await fetch(url.toString(), {
    method: opts.method || 'GET',
    headers: opts.body ? { 'Content-Type': 'application/json' } : undefined,
    body: opts.body ? JSON.stringify(opts.body) : undefined
  });
  const data = await res.json();
  if (!res.ok) {
    const errMsg = data.error?.message || JSON.stringify(data);
    throw new Error(`Meta API ${res.status}: ${errMsg}`);
  }
  return data;
}

/**
 * Cria o container (passo 1).
 */
async function createContainer({ image_url, caption, media_type = 'IMAGE', is_story = false }) {
  const { igUserId } = requireCreds();
  const body = { image_url, caption };
  if (is_story) body.media_type = 'STORIES';
  return metaRequest(`/${igUserId}/media`, { method: 'POST', body });
}

/**
 * Aguarda o container ficar FINISHED (passo 2).
 */
async function waitForContainer(containerId, { maxAttempts = 30, intervalMs = 2000 } = {}) {
  for (let i = 0; i < maxAttempts; i++) {
    const data = await metaRequest(`/${containerId}?fields=status_code,status`);
    if (data.status_code === 'FINISHED') return data;
    if (data.status_code === 'ERROR') throw new Error(`Container ${containerId} status=ERROR: ${data.status || 'desconhecido'}`);
    await new Promise(r => setTimeout(r, intervalMs));
  }
  throw new Error(`Container ${containerId} timeout — não ficou FINISHED em ${maxAttempts * intervalMs}ms`);
}

/**
 * Publica o container (passo 3).
 */
async function publishContainer(containerId) {
  const { igUserId } = requireCreds();
  return metaRequest(`/${igUserId}/media_publish`, {
    method: 'POST',
    body: { creation_id: containerId }
  });
}

/**
 * Pipeline completo: image_url → publicado.
 * @param {object} opts
 * @param {string} opts.image_url - URL HTTPS pública do PNG
 * @param {string} opts.caption - Legenda final (já com hashtags)
 * @param {boolean} [opts.is_story=false] - true = story (24h), false = feed permanente
 * @returns {Promise<object>} { container_id, media_id, permalink? }
 */
export async function publishToInstagram({ image_url, caption, is_story = false }) {
  if (!image_url) throw new Error('image_url obrigatório (deve ser HTTPS público)');
  if (!image_url.startsWith('https://')) {
    throw new Error('image_url deve ser HTTPS público (Meta não aceita HTTP ou localhost)');
  }

  const t0 = Date.now();

  // STEP 1: criar container
  const container = await createContainer({ image_url, caption, is_story });
  const containerId = container.id;

  // STEP 2: aguardar FINISHED
  await waitForContainer(containerId);

  // STEP 3: publicar
  const published = await publishContainer(containerId);
  const mediaId = published.id;

  // Tenta obter permalink (opcional, pode falhar dependendo do tipo)
  let permalink = null;
  try {
    const meta = await metaRequest(`/${mediaId}?fields=permalink`);
    permalink = meta.permalink;
  } catch {}

  return {
    container_id: containerId,
    media_id: mediaId,
    permalink,
    is_story,
    elapsed_ms: Date.now() - t0
  };
}

/**
 * Apenas valida credenciais e retorna informações da conta IG.
 */
export async function getAccountInfo() {
  const { igUserId } = requireCreds();
  return metaRequest(`/${igUserId}?fields=id,username,name,profile_picture_url,followers_count,media_count`);
}
