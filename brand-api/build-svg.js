import fs from 'fs';
import path from 'path';

// ═══════════════════════════════════════════════════════
// BRAND TOKENS (extraídos de brand.json)
// ═══════════════════════════════════════════════════════
const C = {
  yellow: '#F4C430',
  orange: '#FF6B35',
  red: '#C41E3A',
  black: '#1A1A1A',
  blackDeep: '#111111',
  warmWhite: '#FAF3E0',
  gray: '#777777',
  white: '#FFFFFF',
};

// ═══════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════
const assetsPath = path.resolve(process.cwd(), '../assets');

function b64(relPath, mime = 'image/png') {
  const p = path.join(assetsPath, relPath);
  if (!fs.existsSync(p)) { console.warn('⚠️  Asset ausente:', p); return ''; }
  return `data:${mime};base64,${fs.readFileSync(p).toString('base64')}`;
}

function readSvgInline(relPath) {
  const p = path.join(assetsPath, relPath);
  if (!fs.existsSync(p)) return '';
  let svg = fs.readFileSync(p, 'utf-8');
  // Remove a tag SVG exterior — vamos injetar apenas o conteúdo como <g>
  svg = svg.replace(/<\?xml[^?]*\?>/g, '');
  return svg;
}

// Assets carregados
const logoB64 = b64('logo-provisoria.png');
const lexB64 = b64('lex/pesquisa.png');       // Lex pesquisando — maior e mais detalhado (448KB)
const lexIdeiaB64 = b64('lex/ideia-brilhante.png');

// Ícones SVG inline (24x24 viewBox, já com gradient brand)
const iconScales = readSvgInline('icons_v2/scales-gradient.svg');
const iconCpu    = readSvgInline('icons_v2/cpu-gradient.svg');
const iconGavel  = readSvgInline('icons_v2/gavel-gradient.svg');
const iconRocket = readSvgInline('icons_v2/rocket-gradient.svg');

// Texturas tech SVG inline
const techCircuit = readSvgInline('tech/tech-circuit.svg');
const techHexGrid = readSvgInline('tech/tech-hex-grid.svg');

// ═══════════════════════════════════════════════════════
// SVG WRAPPER PREMIUM
// ═══════════════════════════════════════════════════════
function wrap(content, slideNum = '01') {
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>
    <!-- Fontes Google -->
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&amp;family=Montserrat:wght@400;500;700&amp;family=JetBrains+Mono:wght@400;700&amp;display=swap');
    </style>

    <!-- Gradiente principal -->
    <linearGradient id="gradBrand" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="${C.yellow}"/>
      <stop offset="100%" stop-color="${C.orange}"/>
    </linearGradient>
    <linearGradient id="gradWarm" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="${C.orange}"/>
      <stop offset="100%" stop-color="${C.red}"/>
    </linearGradient>
    <linearGradient id="gradFull" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="${C.yellow}"/>
      <stop offset="50%" stop-color="${C.orange}"/>
      <stop offset="100%" stop-color="${C.red}"/>
    </linearGradient>
    <linearGradient id="gradVertical" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="${C.yellow}" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="${C.orange}" stop-opacity="0"/>
    </linearGradient>

    <!-- Glassmorphism blur -->
    <filter id="blur20">
      <feGaussianBlur in="SourceGraphic" stdDeviation="20"/>
    </filter>
    <filter id="glowYellow">
      <feGaussianBlur stdDeviation="12" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="subtleNoise">
      <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="4" stitchTiles="stitch"/>
      <feColorMatrix type="matrix" values="1 0 0 0 0, 0 1 0 0 0, 0 0 1 0 0, 0 0 0 0.03 0"/>
    </filter>

    <!-- Clip para arredondamento global -->
    <clipPath id="roundedFrame">
      <rect width="1080" height="1080" rx="0"/>
    </clipPath>
  </defs>

  <g clip-path="url(#roundedFrame)">
    <!-- Background base -->
    <rect width="1080" height="1080" fill="${C.blackDeep}"/>
    
    <!-- Textura de ruído sutil -->
    <rect width="1080" height="1080" filter="url(#subtleNoise)" opacity="1"/>

    <!-- Glow decorativo de fundo (esferas coloridas desfocadas) -->
    <circle cx="900" cy="200" r="300" fill="${C.yellow}" opacity="0.06" filter="url(#blur20)"/>
    <circle cx="100" cy="900" r="250" fill="${C.orange}" opacity="0.05" filter="url(#blur20)"/>

    ${content}

    <!-- ═══ FOOTER GLOBAL ═══ -->
    <!-- Linha gradiente no rodapé -->
    <rect x="80" y="980" width="920" height="2" fill="url(#gradFull)" opacity="0.3"/>

    <!-- Logo (tamanho adequado — 300px wide) -->
    <image href="${logoB64}" x="80" y="1005" width="300" height="55" preserveAspectRatio="xMinYMid meet" opacity="0.85"/>

    <!-- Indicador de página -->
    <text x="1000" y="1045" text-anchor="end" font-family="JetBrains Mono, monospace" font-size="24" font-weight="700" letter-spacing="2" fill="${C.gray}">${slideNum}/03</text>
  </g>
</svg>`;
}

// ═══════════════════════════════════════════════════════
// SLIDE 01 — CAPA
// ═══════════════════════════════════════════════════════
const slide1 = wrap(`
    <!-- Hex grid como textura de fundo -->
    <g transform="translate(0, 0) scale(2.25)" opacity="0.15">
      ${techHexGrid.replace(/<svg[^>]*>/, '').replace(/<\/svg>/, '').replace(/<rect[^/]*\/>/, '')}
    </g>

    <!-- Badge -->
    <rect x="80" y="100" width="320" height="52" rx="26" fill="url(#gradBrand)"/>
    <text x="240" y="134" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="20" font-weight="700" letter-spacing="3" fill="${C.blackDeep}" text-transform="uppercase">⚖ TECH &amp; DIREITO</text>

    <!-- Headline com letter-spacing negativo (regra do brand) -->
    <text x="80" y="280" font-family="Poppins, sans-serif" font-size="90" font-weight="900" fill="${C.white}" letter-spacing="-3">Quando o</text>
    <text x="80" y="390" font-family="Poppins, sans-serif" font-size="90" font-weight="900" fill="url(#gradBrand)" letter-spacing="-3">código fonte</text>
    <text x="80" y="500" font-family="Poppins, sans-serif" font-size="90" font-weight="900" fill="${C.white}" letter-spacing="-3">vira lei.</text>

    <!-- Barra decorativa -->
    <rect x="80" y="540" width="120" height="6" rx="3" fill="url(#gradBrand)"/>

    <!-- Lead / subtítulo -->
    <text x="80" y="610" font-family="Montserrat, sans-serif" font-size="36" font-weight="400" fill="${C.warmWhite}" opacity="0.8">A ascensão da automação algorítmica</text>
    <text x="80" y="660" font-family="Montserrat, sans-serif" font-size="36" font-weight="400" fill="${C.warmWhite}" opacity="0.8">nos tribunais brasileiros.</text>

    <!-- Ícones brand inline (escalados para 72px) -->
    <g transform="translate(80, 740) scale(3)">
      ${iconScales.replace(/<svg[^>]*>/, '').replace(/<\/svg>/, '')}
    </g>
    <g transform="translate(180, 740) scale(3)">
      ${iconCpu.replace(/<svg[^>]*>/, '').replace(/<\/svg>/, '')}
    </g>
    <g transform="translate(280, 740) scale(3)">
      ${iconGavel.replace(/<svg[^>]*>/, '').replace(/<\/svg>/, '')}
    </g>

    <!-- Mascote Lex no canto inferior direito -->
    <image href="${lexIdeiaB64}" x="680" y="580" width="380" height="380" preserveAspectRatio="xMidYMid meet" opacity="0.9"/>

    <!-- Seta → arraste -->
    <g transform="translate(980, 920)">
      <circle cx="0" cy="0" r="32" fill="none" stroke="${C.yellow}" stroke-width="2" opacity="0.5"/>
      <path d="M -10 0 L 10 0 M 4 -7 L 11 0 L 4 7" stroke="${C.white}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
`, '01');

// ═══════════════════════════════════════════════════════
// SLIDE 02 — CONTEÚDO (Vieses algorítmicos)
// ═══════════════════════════════════════════════════════
const slide2 = wrap(`
    <!-- Circuit board como textura -->
    <g transform="translate(300, 600) scale(2.25)" opacity="0.1">
      ${techCircuit.replace(/<svg[^>]*>/, '').replace(/<\/svg>/, '').replace(/<rect[^/]*\/>/, '')}
    </g>

    <!-- Badge superior -->
    <rect x="80" y="80" width="160" height="44" rx="22" fill="${C.orange}" fill-opacity="0.15" stroke="${C.orange}" stroke-width="1.5"/>
    <text x="160" y="110" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="16" font-weight="700" letter-spacing="2" fill="${C.orange}">ANÁLISE</text>

    <!-- Título -->
    <text x="80" y="210" font-family="Poppins, sans-serif" font-size="72" font-weight="800" fill="url(#gradBrand)" letter-spacing="-2">O Risco Preditivo</text>

    <!-- Barra -->
    <rect x="80" y="240" width="80" height="4" rx="2" fill="url(#gradBrand)"/>

    <!-- Texto corpo -->
    <text x="80" y="320" font-family="Montserrat, sans-serif" font-size="32" font-weight="400" fill="${C.warmWhite}" opacity="0.85">Sistemas judiciais automatizados treinados</text>
    <text x="80" y="365" font-family="Montserrat, sans-serif" font-size="32" font-weight="400" fill="${C.warmWhite}" opacity="0.85">em decisões passadas podem perpetuar</text>
    <text x="80" y="410" font-family="Montserrat, sans-serif" font-size="32" font-weight="400" fill="${C.warmWhite}" opacity="0.85">vieses sistêmicos nas sentenças.</text>

    <!-- ═══ Card Glassmorphism ═══ -->
    <rect x="80" y="470" width="920" height="220" rx="24" fill="${C.white}" fill-opacity="0.04" stroke="${C.yellow}" stroke-opacity="0.2" stroke-width="1.5"/>

    <!-- Número destaque -->
    <text x="140" y="570" font-family="Poppins, sans-serif" font-size="80" font-weight="900" fill="url(#gradBrand)" letter-spacing="-2">87%</text>
    <text x="430" y="545" font-family="Montserrat, sans-serif" font-size="28" font-weight="500" fill="${C.warmWhite}" opacity="0.8">de correlação entre predições</text>
    <text x="430" y="585" font-family="Montserrat, sans-serif" font-size="28" font-weight="500" fill="${C.warmWhite}" opacity="0.8">de certas IAs e precedentes</text>
    <text x="430" y="625" font-family="Montserrat, sans-serif" font-size="28" font-weight="500" fill="${C.warmWhite}" opacity="0.8">historicamente enviesados.</text>

    <!-- Barra de progresso visual -->
    <rect x="140" y="640" width="240" height="6" rx="3" fill="${C.black}"/>
    <rect x="140" y="640" width="210" height="6" rx="3" fill="url(#gradBrand)"/>

    <!-- ═══ Card 2 menor ═══ -->
    <rect x="80" y="730" width="440" height="180" rx="24" fill="${C.white}" fill-opacity="0.04" stroke="${C.orange}" stroke-opacity="0.15" stroke-width="1"/>
    <text x="140" y="800" font-family="Poppins, sans-serif" font-size="48" font-weight="900" fill="${C.orange}" letter-spacing="-1">2.400</text>
    <text x="140" y="850" font-family="Montserrat, sans-serif" font-size="24" font-weight="400" fill="${C.warmWhite}" opacity="0.7">sentenças brasileiras</text>
    <text x="140" y="880" font-family="Montserrat, sans-serif" font-size="24" font-weight="400" fill="${C.warmWhite}" opacity="0.7">analisadas neste estudo.</text>

    <rect x="560" y="730" width="440" height="180" rx="24" fill="${C.white}" fill-opacity="0.04" stroke="${C.red}" stroke-opacity="0.15" stroke-width="1"/>
    <text x="620" y="800" font-family="Poppins, sans-serif" font-size="48" font-weight="900" fill="${C.red}" letter-spacing="-1">3.2×</text>
    <text x="620" y="850" font-family="Montserrat, sans-serif" font-size="24" font-weight="400" fill="${C.warmWhite}" opacity="0.7">mais chances de viés em</text>
    <text x="620" y="880" font-family="Montserrat, sans-serif" font-size="24" font-weight="400" fill="${C.warmWhite}" opacity="0.7">modelos genéricos vs. especializados.</text>

    <!-- Fonte do dado -->
    <text x="80" y="958" font-family="JetBrains Mono, monospace" font-size="16" letter-spacing="1.5" fill="${C.gray}" opacity="0.6">FONTE: ESTUDO iLAB · FD-USP · N=2.400 · 2026</text>
`, '02');

// ═══════════════════════════════════════════════════════
// SLIDE 03 — CTA + LEX MASCOTE
// ═══════════════════════════════════════════════════════
const slide3 = wrap(`
    <!-- Glow adicional de fundo -->
    <circle cx="750" cy="500" r="400" fill="${C.yellow}" opacity="0.04" filter="url(#blur20)"/>
    <circle cx="300" cy="300" r="300" fill="${C.orange}" opacity="0.03" filter="url(#blur20)"/>

    <!-- Mascote Lex (grande, destaque) -->
    <image href="${lexB64}" x="550" y="100" width="500" height="500" preserveAspectRatio="xMidYMid meet" opacity="0.95"/>

    <!-- Badge superior -->
    <rect x="80" y="100" width="200" height="44" rx="22" fill="${C.red}" fill-opacity="0.15" stroke="${C.red}" stroke-width="1.5"/>
    <text x="180" y="130" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="16" font-weight="700" letter-spacing="2" fill="${C.red}">CHAMADA</text>

    <!-- Headline -->
    <text x="80" y="260" font-family="Poppins, sans-serif" font-size="76" font-weight="900" fill="${C.white}" letter-spacing="-3">Prepare-se</text>
    <text x="80" y="350" font-family="Poppins, sans-serif" font-size="76" font-weight="900" fill="${C.white}" letter-spacing="-3">para a</text>
    <text x="80" y="440" font-family="Poppins, sans-serif" font-size="76" font-weight="900" fill="url(#gradBrand)" letter-spacing="-3">Advocacia 5.0</text>

    <!-- Barra -->
    <rect x="80" y="470" width="100" height="5" rx="2" fill="url(#gradBrand)"/>

    <!-- Corpo -->
    <text x="80" y="540" font-family="Montserrat, sans-serif" font-size="30" font-weight="400" fill="${C.warmWhite}" opacity="0.85">Descubra como o SanFran iLab</text>
    <text x="80" y="585" font-family="Montserrat, sans-serif" font-size="30" font-weight="400" fill="${C.warmWhite}" opacity="0.85">está construindo o futuro do Direito.</text>

    <!-- Botão CTA Gradiente -->
    <rect x="80" y="650" width="460" height="80" rx="40" fill="url(#gradBrand)"/>
    <text x="310" y="700" text-anchor="middle" font-family="Poppins, sans-serif" font-size="28" font-weight="700" fill="${C.blackDeep}" letter-spacing="1">ACESSE O RELATÓRIO →</text>

    <!-- Ícone Rocket ao lado do botão -->
    <g transform="translate(570, 660) scale(2.5)">
      ${iconRocket.replace(/<svg[^>]*>/, '').replace(/<\/svg>/, '')}
    </g>

    <!-- Seção inferior: handle e org -->
    <text x="80" y="820" font-family="JetBrains Mono, monospace" font-size="22" font-weight="700" letter-spacing="2" fill="${C.yellow}">@sanfran.ilab</text>
    <text x="80" y="860" font-family="Montserrat, sans-serif" font-size="20" font-weight="400" fill="${C.gray}">Faculdade de Direito da USP · FD-USP</text>

    <!-- Card de convite -->
    <rect x="80" y="890" width="920" height="70" rx="16" fill="${C.white}" fill-opacity="0.04" stroke="${C.yellow}" stroke-opacity="0.15" stroke-width="1"/>
    <text x="540" y="934" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="18" letter-spacing="2" fill="${C.warmWhite}" opacity="0.6">SALVE · COMPARTILHE · SIGA O iLAB</text>
`, '03');

// ═══════════════════════════════════════════════════════
// SALVAR OS ARQUIVOS
// ═══════════════════════════════════════════════════════
const outPath = path.resolve(process.cwd(), '../');
fs.writeFileSync(path.join(outPath, 'carrossel_01.svg'), slide1);
fs.writeFileSync(path.join(outPath, 'carrossel_02.svg'), slide2);
fs.writeFileSync(path.join(outPath, 'carrossel_03.svg'), slide3);
console.log('✅ 3 SVGs premium gerados com sucesso!');
console.log(`   → ${path.join(outPath, 'carrossel_01.svg')}`);
console.log(`   → ${path.join(outPath, 'carrossel_02.svg')}`);
console.log(`   → ${path.join(outPath, 'carrossel_03.svg')}`);
