// === Story renderer: HTML → PNG 1080×1920 via Playwright ===
// Usa o index.html do brandbook como fonte única (window.iLabRender).
// Browser instance é singleton para reutilização (warm) e desligado on demand.
//
// MODO DUAL:
// - Local/Dev:        usa `playwright` com chromium bundled
// - Serverless (Vercel/AWS Lambda): usa `playwright-core` + `@sparticuz/chromium-min`
//   ativado via env IS_SERVERLESS=1 ou auto-detectado pelo VERCEL=1

import { fileURLToPath, pathToFileURL } from 'url';
import { dirname, resolve } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Resolução do brandbook:
// 1. env INDEX_HTML_PATH (override explícito)
// 2. ../index.html (Railway com Root Directory = brand-api/ + cópia)
// 3. ../../index.html (caso brand-api esteja 1 nível abaixo)
// 4. ../../../index.html (estrutura local dentro do scratch)
import { existsSync } from 'fs';

function resolveIndexPath() {
  if (process.env.INDEX_HTML_PATH) return process.env.INDEX_HTML_PATH;
  const candidates = [
    resolve(__dirname, '..', '..', 'index.html'),
    resolve(__dirname, '..', '..', '..', 'index.html'),
    resolve(__dirname, '..', '..', '..', '..', 'index.html'),
    resolve(process.cwd(), 'index.html'),
    resolve(process.cwd(), '..', 'index.html')
  ];
  for (const p of candidates) {
    if (existsSync(p)) return p;
  }
  // fallback: assume estrutura padrão
  return resolve(__dirname, '..', '..', '..', 'index.html');
}

const INDEX_HTML_PATH = resolveIndexPath();
const INDEX_URL = pathToFileURL(INDEX_HTML_PATH).href;

const IS_SERVERLESS = process.env.IS_SERVERLESS === '1' || !!process.env.VERCEL;

async function launchBrowser() {
  if (IS_SERVERLESS) {
    const [{ chromium: chromiumCore }, chromiumLambda] = await Promise.all([
      import('playwright-core'),
      import('@sparticuz/chromium-min').then(m => m.default || m)
    ]);
    return chromiumCore.launch({
      args: chromiumLambda.args,
      executablePath: await chromiumLambda.executablePath(
        process.env.CHROMIUM_PACK_URL ||
        'https://github.com/Sparticuz/chromium/releases/download/v131.0.1/chromium-v131.0.1-pack.tar'
      ),
      headless: true
    });
  }
  // Local/dev path
  const { chromium } = await import('playwright');
  return chromium.launch({ headless: true });
}

let browserPromise = null;
function getBrowser() {
  if (!browserPromise) browserPromise = launchBrowser();
  return browserPromise;
}

export async function closeBrowser() {
  if (browserPromise) {
    const b = await browserPromise;
    await b.close();
    browserPromise = null;
  }
}

/**
 * Renderiza um story como PNG 1080×1920.
 * @param {object} opts
 * @param {string} opts.template - id do template (encontro, dica, etc)
 * @param {object} opts.fields - mapa { fieldId: valor }
 * @param {string} [opts.image_data_url] - data:image/...;base64,... para foto
 * @returns {Promise<Buffer>} PNG buffer
 */
export async function renderStory({ template, fields = {}, image_data_url }) {
  if (!template) throw new Error('Parâmetro "template" obrigatório');

  const browser = await getBrowser();
  const context = await browser.newContext({
    viewport: { width: 1080, height: 1920 },
    deviceScaleFactor: 1
  });
  const page = await context.newPage();

  try {
    await page.goto(INDEX_URL, { waitUntil: 'load', timeout: 30000 });

    // Aguarda window.iLabRender e fontes
    await page.waitForFunction(() => typeof window.iLabRender === 'function', { timeout: 15000 });
    await page.evaluate(() => document.fonts && document.fonts.ready);

    // Executa render
    await page.evaluate(({ tpl, flds, img }) => {
      window.iLabRender(tpl, flds, img);
    }, { tpl: template, flds: fields, img: image_data_url || null });

    // Aguarda 1 frame + tempo para imagens carregarem
    await page.waitForTimeout(image_data_url ? 600 : 250);

    // Screenshot do layout dentro do render-target (suporta .story, .feed-post, .video-reel)
    const el = page.locator('#se-render-target > div').first();
    const buf = await el.screenshot({ type: 'png', omitBackground: false });
    return buf;
  } finally {
    await page.close();
    await context.close();
  }
}

export async function listTemplates() {
  const browser = await getBrowser();
  const context = await browser.newContext();
  const page = await context.newPage();
  try {
    await page.goto(INDEX_URL, { waitUntil: 'load' });
    await page.waitForFunction(() => typeof window.iLabTemplates === 'function');
    return await page.evaluate(() => window.iLabTemplates());
  } finally {
    await page.close();
    await context.close();
  }
}
