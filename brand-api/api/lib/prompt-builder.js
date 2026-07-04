// === Helper: gera system prompt completo a partir do brand.json ===
// Output é uma string pronta pra injetar em qualquer LLM.

import { loadBrand } from './brand-loader.js';

export function buildSystemPrompt(lang = 'pt') {
  const b = loadBrand();
  const sections = [];

  // === IDENTIDADE ===
  sections.push(`Você é o assistente oficial de comunicação do ${b.identity.name} (${b.identity.org}).`);
  sections.push(`Handle oficial: ${b.identity.handle}`);
  sections.push(`Tagline: "${b.identity.tagline}"`);
  sections.push(`Missão: ${b.identity.mission}`);
  sections.push('');

  // === TOM DE VOZ ===
  sections.push('## Tom de voz');
  sections.push(`Tons: ${b.voice.tone.join(', ')}.`);
  sections.push(`Persona: ${b.voice.persona}`);
  sections.push('');
  sections.push('### Faça:');
  b.voice.dos.forEach(d => sections.push(`- ${d}`));
  sections.push('');
  sections.push('### Evite:');
  b.voice.donts.forEach(d => sections.push(`- ${d}`));
  sections.push('');

  // === CORES ===
  sections.push('## Paleta de cores oficial');
  sections.push(`Primárias: amarelo ${b.colors.primary.yellow}, laranja ${b.colors.primary.orange}, vermelho ${b.colors.primary.red}`);
  sections.push(`Neutras: preto ${b.colors.neutrals.black}, warm white ${b.colors.neutrals.warmWhite}`);
  sections.push('Não introduza cores fora desta paleta.');
  sections.push('');

  // === TIPOGRAFIA ===
  sections.push('## Tipografia');
  sections.push(`Display: ${b.typography.fonts.display} (títulos)`);
  sections.push(`Body: ${b.typography.fonts.body} (corpo)`);
  sections.push(`Mono: ${b.typography.fonts.mono} (labels, badges)`);
  sections.push('');

  // === TEMPLATES ===
  sections.push('## Templates de Story disponíveis');
  Object.entries(b.templates).forEach(([id, tpl]) => {
    sections.push(`- **${id}**: ${tpl.name} — ${tpl.useCase}`);
  });
  sections.push('');

  // === HASHTAGS ===
  sections.push('## Hashtags oficiais');
  sections.push(`Core (use pelo menos 1): ${b.hashtags.core.join(' ')}`);
  sections.push(`Temas: ${b.hashtags.temas.join(' ')}`);
  sections.push(`Eventos: ${b.hashtags.eventos.join(' ')}`);
  sections.push('Regras: máximo 5 hashtags por post.');
  sections.push('');

  // === REGRAS DE COPY ===
  sections.push('## Regras de copy');
  if (b.rules && b.rules.post) {
      sections.push(`Caption: ${b.rules.post.caption.minLength}-${b.rules.post.caption.maxLength} caracteres.`);
      sections.push(`Estrutura: ${b.rules.post.caption.structure}.`);
      sections.push(`Emojis: ${b.rules.post.emojiPolicy}`);
      sections.push(`Links: ${b.rules.post.linkPolicy}`);
  }
  sections.push('');

  // === REGRAS DE DESIGN & COMPOSIÇÃO ===
  if (b.designRules) {
      sections.push('## Regras de Design e Composição Visual (CRÍTICO)');
      b.designRules.composition.forEach(rule => sections.push(`- ${rule}`));
      sections.push('');
  }

  // === REGRAS ESTRITAS DE USO DOS NOVOS TEMPLATES PREMIUM ===
  sections.push('## Instruções estritas para a criação do Rascunho (CRÍTICO)');
  sections.push('- TEMPLATES PRÉ-FABRICADOS: Os templates do SanFran iLab agora são Premium. Eles JÁ INCLUEM nativamente as logos, texturas, efeitos glassmorphism e backgrounds escuros.');
  sections.push('- ARRAY DE DECORATIONS VAZIO: Na grande maioria das vezes, seu array de `decorations` deve ser enviado VAZIO `[]`. Você NÃO DEVE MAIS tentar adivinhar as coordenadas (X, Y) para injetar a logo ou malhas tecnológicas, pois o template já resolveu isso perfeitamente.');
  sections.push('- SEU FOCO É COPY: Sua função primária é criar o conteúdo de alto nível e preencher as chaves em `fields` (como headline, supertitle, cta, etc) seguindo as restrições de formatação e tom de voz.');
  sections.push('- EXCEÇÕES DE DECORATIONS: Use a propriedade `decorations` APENAS quando o post exigir uma foto externa obrigatória (como o rosto de um palestrante no template `encontro`) ou se quiser injetar um ícone 3D solto para ilustrar um post muito textual. Nunca para logos ou texturas de fundo.');
  sections.push('');

  // === EXEMPLOS ===
  sections.push('## Exemplos de copy ON-BRAND');
  b.voice.examples.good.forEach(ex => sections.push(`✓ "${ex}"`));
  sections.push('');
  sections.push('## Exemplos OFF-BRAND (NÃO faça)');
  b.voice.examples.bad.forEach(ex => sections.push(`✗ "${ex}"`));
  sections.push('');

  sections.push('---');
  sections.push('Antes de gerar qualquer conteúdo, valide se está alinhado com o tom, a paleta e as regras acima.');

  return sections.join('\n');
}
