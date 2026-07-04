// === Helper: valida texto contra regras de brand ===
// Retorna { valid, score, issues[] }

import { loadBrand } from './brand-loader.js';

export function validateCopy(text, context = {}) {
  const b = loadBrand();
  const issues = [];
  let score = 100;

  const len = text.length;
  const lower = text.toLowerCase();

  // === Tamanho ===
  if (context.type === 'caption' || !context.type) {
    if (len < b.rules.post.caption.minLength) {
      issues.push({ severity: 'warning', code: 'too_short', message: `Texto curto (${len} chars). Mínimo recomendado: ${b.rules.post.caption.minLength}.` });
      score -= 10;
    }
    if (len > b.rules.post.caption.maxLength) {
      issues.push({ severity: 'error', code: 'too_long', message: `Texto longo (${len} chars). Máximo: ${b.rules.post.caption.maxLength}.` });
      score -= 15;
    }
  }

  // === Emojis ===
  const emojiRegex = /[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/gu;
  const emojiCount = (text.match(emojiRegex) || []).length;
  if (emojiCount > 2) {
    issues.push({ severity: 'warning', code: 'too_many_emojis', message: `${emojiCount} emojis encontrados. Máximo recomendado: 2.` });
    score -= 8;
  }

  // === Hashtags ===
  const hashtags = text.match(/#\w+/g) || [];
  if (hashtags.length > 5) {
    issues.push({ severity: 'warning', code: 'too_many_hashtags', message: `${hashtags.length} hashtags. Máximo: 5.` });
    score -= 10;
  }
  if (hashtags.length > 0) {
    const coreUsed = b.hashtags.core.some(h => hashtags.map(x => x.toLowerCase()).includes(h.toLowerCase()));
    if (!coreUsed) {
      issues.push({ severity: 'warning', code: 'no_core_hashtag', message: `Nenhuma hashtag core (${b.hashtags.core.join(', ')}) detectada.` });
      score -= 8;
    }
  }

  // === Clichês / palavras proibidas ===
  const cliches = [
    'revolucionar', 'transforme sua vida', 'melhor versão', 'segredo que',
    'todos advogados de sucesso', 'fature', '6 dígitos', 'mude sua mente',
    'sinergia', 'alavancar', 'destrave', 'gameificar'
  ];
  cliches.forEach(c => {
    if (lower.includes(c)) {
      issues.push({ severity: 'error', code: 'cliche', message: `Clichê detectado: "${c}". Reescreva com termo concreto.` });
      score -= 15;
    }
  });

  // === Excesso de caixa alta ===
  const upperWords = text.match(/\b[A-Z]{4,}\b/g) || [];
  if (upperWords.length > 2) {
    issues.push({ severity: 'warning', code: 'too_much_caps', message: `${upperWords.length} palavras em CAIXA ALTA. Use no máximo 2.` });
    score -= 6;
  }

  // === Promessas absolutas ===
  const absolutes = ['100% garantido', 'em 7 dias', 'em 5 dias', 'sem esforço', 'qualquer um pode'];
  absolutes.forEach(p => {
    if (lower.includes(p)) {
      issues.push({ severity: 'error', code: 'absolute_promise', message: `Promessa absoluta: "${p}". Evite linguagem marqueteira.` });
      score -= 12;
    }
  });

  // Normaliza score
  score = Math.max(0, Math.min(100, score));

  return {
    valid: issues.filter(i => i.severity === 'error').length === 0,
    score,
    issues,
    stats: {
      length: len,
      emojis: emojiCount,
      hashtags: hashtags.length,
      hashtagsList: hashtags
    }
  };
}
