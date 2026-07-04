// === Smoke test: valida que tudo carrega e funciona ===
import { loadBrand, getTemplate, getHashtags } from '../api/lib/brand-loader.js';
import { buildSystemPrompt } from '../api/lib/prompt-builder.js';
import { validateCopy } from '../api/lib/validator.js';

let pass = 0, fail = 0;
async function test(name, fn) {
  try { await fn(); console.log(`✓ ${name}`); pass++; }
  catch (e) { console.error(`✗ ${name}: ${e.message}`); fail++; }
}
function assert(cond, msg) { if (!cond) throw new Error(msg || 'assertion failed'); }

async function run() {
  // === Brand loader ===
  await test('brand.json carrega', () => {
    const b = loadBrand();
    assert(b.identity, 'identity ausente');
    assert(b.colors.primary.yellow === '#F4C430', 'cor amarela errada');
  });

  await test('templates retornam 10 entries', () => {
    const b = loadBrand();
    assert(Object.keys(b.templates).length === 10, 'esperado 10 templates');
  });

  await test('getTemplate("dica") funciona', () => {
    const t = getTemplate('dica');
    assert(t.hasPhoto === false, 'dica não deveria ter foto');
  });

  await test('getTemplate("invalid") retorna null', () => {
    assert(getTemplate('invalid') === null);
  });

  await test('getHashtags("core") retorna array', () => {
    const h = getHashtags('core');
    assert(Array.isArray(h) && h.length > 0);
  });

  // === Prompt builder ===
  await test('buildSystemPrompt retorna string >500 chars', () => {
    const p = buildSystemPrompt();
    assert(typeof p === 'string' && p.length > 500, `prompt curto: ${p.length}`);
    assert(p.includes('SanFran iLab'), 'sem nome do brand');
    assert(p.includes('#iLab'), 'sem hashtag core');
  });

  await test('buildSystemPrompt preserva espaçamento entre seções', () => {
    // Regressão: um refactor "clean-code" pode remover as linhas em branco entre
    // seções (sections.push('')) sem quebrar nenhum outro assert — mas isso piora
    // a legibilidade do prompt pro LLM. Trava esse invariante estrutural aqui.
    const p = buildSystemPrompt();
    const blankBeforeHeading = (p.match(/\n\n#{2,3} /g) || []).length;
    assert(blankBeforeHeading >= 10, `esperado >=10 headings com linha em branco antes, achou ${blankBeforeHeading}`);
  });

  // === Validator ===
  await test('valida copy boa (alto score)', () => {
    const r = validateCopy('Novo paper publicado pelo iLab: vieses algorítmicos em decisões judiciais. Análise empírica de 2.400 sentenças. Link na bio. #iLab #DireitoEIA');
    assert(r.score >= 80, `score baixo demais: ${r.score}`);
  });

  await test('detecta clichê', () => {
    const r = validateCopy('Vamos revolucionar sua carreira jurídica em 7 dias!');
    assert(r.valid === false, 'deveria invalidar');
    assert(r.issues.some(i => i.code === 'cliche'), 'deveria detectar clichê');
  });

  await test('detecta excesso de emojis', () => {
    const r = validateCopy('Texto teste 🚀🔥✨💯❤️ com muitos emojis para validar #iLab #SanFraniLab #DireitoEIA');
    assert(r.issues.some(i => i.code === 'too_many_emojis'));
  });

  await test('detecta texto muito curto', () => {
    const r = validateCopy('Curto.');
    assert(r.issues.some(i => i.code === 'too_short'));
  });

  // === Imports dinâmicos (módulos novos) ===
  await test('llm-generator carrega', async () => {
    const m = await import('../api/lib/llm-generator.js');
    assert(typeof m.generateCopy === 'function');
  });

  await test('story-renderer carrega', async () => {
    const m = await import('../api/lib/story-renderer.js');
    assert(typeof m.renderStory === 'function');
    assert(typeof m.closeBrowser === 'function');
  });

  await test('instagram-publisher carrega', async () => {
    const m = await import('../api/lib/instagram-publisher.js');
    assert(typeof m.publishToInstagram === 'function');
    assert(typeof m.getAccountInfo === 'function');
  });

  console.log(`\n${pass} passed, ${fail} failed`);
  process.exit(fail > 0 ? 1 : 0);
}

run();
