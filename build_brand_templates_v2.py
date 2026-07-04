"""
6 templates SVG editáveis, cada um com visual próprio,
todos dentro do brandbook iLab (paleta + tipografia oficial).

Variedade proposital — não copia o iLab Conecta.
Cada template explora um lado diferente da identidade:
  · light (warm-white)    → Citação, Educa
  · gradient signature    → Pesquisa, Edital
  · split duotone         → Manifesto
  · dark + holográfico    → Marco

Formato: 1080×1350 (post Instagram).
Saída: assets/templates/*.svg
"""
from pathlib import Path

OUT = Path(__file__).parent / "assets" / "templates"
OUT.mkdir(parents=True, exist_ok=True)

# Paleta oficial do brand book
YELLOW = "#F4C430"
ORANGE = "#FF6B35"
RED = "#C41E3A"
BLACK = "#1A1A1A"
BLACK_DEEP = "#111111"
WHITE = "#F5F5F5"
WARM = "#FAF3E0"
GRAY = "#777"

W, H = 1080, 1350


def common_defs():
    """Gradientes e patterns reutilizados pela marca."""
    return f'''
<defs>
  <linearGradient id="brand-grad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{YELLOW}"/>
    <stop offset="100%" stop-color="{ORANGE}"/>
  </linearGradient>
  <linearGradient id="brand-grad-h" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{YELLOW}"/>
    <stop offset="100%" stop-color="{ORANGE}"/>
  </linearGradient>
  <linearGradient id="brand-grad-red" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{ORANGE}"/>
    <stop offset="100%" stop-color="{RED}"/>
  </linearGradient>
  <radialGradient id="mesh-hot" cx="50%" cy="50%" r="60%">
    <stop offset="0%" stop-color="{YELLOW}" stop-opacity="0.6"/>
    <stop offset="50%" stop-color="{ORANGE}" stop-opacity="0.3"/>
    <stop offset="100%" stop-color="{BLACK_DEEP}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="mesh-holo-1" cx="30%" cy="20%" r="40%">
    <stop offset="0%" stop-color="#FFB7A8" stop-opacity="0.8"/>
    <stop offset="100%" stop-color="#FFB7A8" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="mesh-holo-2" cx="80%" cy="80%" r="50%">
    <stop offset="0%" stop-color="#FFD580" stop-opacity="0.7"/>
    <stop offset="100%" stop-color="#FFD580" stop-opacity="0"/>
  </radialGradient>
  <pattern id="paper-dots" width="40" height="40" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1" fill="{BLACK}" opacity="0.08"/>
  </pattern>
</defs>'''


def ilab_signature(y_offset: int, color_i: str = YELLOW, color_lab: str = ORANGE, sub_color: str = BLACK):
    """Logo iLab no rodapé — versão compacta."""
    return f'''
<g transform="translate(80,{y_offset})">
  <text font-family="Poppins, sans-serif" font-weight="900" font-size="28" letter-spacing="-1">
    <tspan fill="{color_i}">i</tspan><tspan fill="{color_lab}">Lab</tspan>
  </text>
  <text x="0" y="36" font-family="JetBrains Mono, monospace" font-weight="700" font-size="12" fill="{sub_color}" letter-spacing="3" opacity="0.55">SANFRAN · FD-USP</text>
</g>'''


def handle(y_offset: int, color: str = ORANGE):
    return f'<text x="{W-80}" y="{y_offset}" font-family="JetBrains Mono, monospace" font-weight="700" font-size="13" fill="{color}" text-anchor="end" letter-spacing="3">@SANFRANILAB</text>'


def render(body: str, filename: str):
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
{common_defs()}
{body}
</svg>'''
    (OUT / filename).write_text(svg, encoding="utf-8")
    print(f"  OK {filename}")


# ═══════════════════════════════════════════════
# 1) CITAÇÃO — light, editorial, clean
# ═══════════════════════════════════════════════
def template_citacao():
    body = f'''
<rect width="{W}" height="{H}" fill="{WARM}"/>
<rect width="{W}" height="{H}" fill="url(#paper-dots)"/>

<!-- Círculo decorativo grande à direita -->
<circle cx="{W+40}" cy="200" r="320" fill="url(#brand-grad)" opacity="0.18"/>
<circle cx="{W+40}" cy="200" r="320" fill="none" stroke="{ORANGE}" stroke-width="2" opacity="0.3"/>

<!-- Label categoria -->
<text x="80" y="140" font-family="JetBrains Mono, monospace" font-weight="700" font-size="14" fill="{ORANGE}" letter-spacing="4">— CITAÇÃO</text>

<!-- Aspas decorativas -->
<text x="80" y="360" font-family="Poppins, sans-serif" font-weight="900" font-size="320" fill="url(#brand-grad)" opacity="0.9">"</text>

<!-- Citação em serif feel -->
<text x="80" y="520" font-family="Poppins, sans-serif" font-weight="700" font-size="62" fill="{BLACK}" letter-spacing="-1.5">A inovação no</text>
<text x="80" y="595" font-family="Poppins, sans-serif" font-weight="700" font-size="62" fill="{BLACK}" letter-spacing="-1.5">Direito começa</text>
<text x="80" y="670" font-family="Poppins, sans-serif" font-weight="700" font-size="62" fill="{ORANGE}" letter-spacing="-1.5">por dentro das</text>
<text x="80" y="745" font-family="Poppins, sans-serif" font-weight="700" font-size="62" fill="{ORANGE}" letter-spacing="-1.5">salas de aula.</text>

<!-- Bloco autoria com avatar circle -->
<g transform="translate(80,900)">
  <!-- avatar placeholder circular -->
  <circle cx="50" cy="50" r="50" fill="url(#brand-grad)"/>
  <circle cx="50" cy="50" r="50" fill="{WARM}" opacity="0.85"/>
  <text x="50" y="58" font-family="Poppins, sans-serif" font-weight="900" font-size="32" fill="{BLACK}" text-anchor="middle" opacity="0.4">A</text>

  <text x="125" y="40" font-family="Poppins, sans-serif" font-weight="900" font-size="26" fill="{BLACK}" letter-spacing="-.5">NOME DO AUTOR</text>
  <text x="125" y="68" font-family="Montserrat, sans-serif" font-weight="400" font-size="16" fill="{BLACK}" opacity="0.7">Cargo · Instituição</text>
  <line x1="125" y1="82" x2="220" y2="82" stroke="{ORANGE}" stroke-width="2"/>
</g>

{ilab_signature(H-90, color_i=YELLOW, color_lab=ORANGE, sub_color=BLACK)}
{handle(H-60, ORANGE)}
'''
    render(body, "ilab-citacao.svg")


# ═══════════════════════════════════════════════
# 2) PESQUISA — gradient bg + cards
# ═══════════════════════════════════════════════
def template_pesquisa():
    body = f'''
<rect width="{W}" height="{H}" fill="url(#brand-grad)"/>

<!-- Mesh overlays sutis -->
<rect width="{W}" height="{H}" fill="url(#mesh-holo-1)"/>
<rect width="{W}" height="{H}" fill="url(#mesh-holo-2)"/>

<!-- Header -->
<text x="80" y="140" font-family="JetBrains Mono, monospace" font-weight="700" font-size="14" fill="{BLACK}" letter-spacing="4">PESQUISA · RELATÓRIO 2026</text>

<!-- Big title em preto sobre gradient -->
<text x="80" y="290" font-family="Poppins, sans-serif" font-weight="900" font-size="96" fill="{BLACK}" letter-spacing="-3.5">Direito</text>
<text x="80" y="390" font-family="Poppins, sans-serif" font-weight="900" font-size="96" fill="{BLACK}" letter-spacing="-3.5">+ IA</text>
<text x="80" y="490" font-family="Poppins, sans-serif" font-weight="900" font-size="96" fill="{WARM}" letter-spacing="-3.5">no Brasil</text>

<!-- Cards de dados em white floating -->
<g transform="translate(80,580)">
  <rect width="430" height="160" rx="16" fill="{WARM}" />
  <text x="28" y="84" font-family="Poppins, sans-serif" font-weight="900" font-size="84" fill="{ORANGE}" letter-spacing="-2">87%</text>
  <line x1="28" y1="106" x2="80" y2="106" stroke="{BLACK}" stroke-width="3"/>
  <text x="28" y="134" font-family="Montserrat, sans-serif" font-weight="700" font-size="15" fill="{BLACK}">dos escritórios usam</text>
  <text x="28" y="154" font-family="Montserrat, sans-serif" font-weight="700" font-size="15" fill="{BLACK}">IA em 2026</text>
</g>

<g transform="translate(530,580)">
  <rect width="430" height="160" rx="16" fill="{BLACK}"/>
  <text x="28" y="84" font-family="Poppins, sans-serif" font-weight="900" font-size="84" fill="{YELLOW}" letter-spacing="-2">3.2x</text>
  <line x1="28" y1="106" x2="80" y2="106" stroke="{ORANGE}" stroke-width="3"/>
  <text x="28" y="134" font-family="Montserrat, sans-serif" font-weight="700" font-size="15" fill="{WARM}">aumento na</text>
  <text x="28" y="154" font-family="Montserrat, sans-serif" font-weight="700" font-size="15" fill="{WARM}">produtividade jurídica</text>
</g>

<!-- Texto explicativo -->
<text x="80" y="800" font-family="Montserrat, sans-serif" font-weight="700" font-size="22" fill="{BLACK}">Estudo conduzido pelo SanFran iLab</text>
<text x="80" y="828" font-family="Montserrat, sans-serif" font-weight="400" font-size="18" fill="{BLACK}" opacity="0.75">com 1.200 escritórios em todo o país.</text>

<!-- CTA -->
<g transform="translate(80,900)">
  <rect width="420" height="76" rx="38" fill="{BLACK}"/>
  <text x="210" y="48" font-family="JetBrains Mono, monospace" font-weight="700" font-size="16" fill="{YELLOW}" text-anchor="middle" letter-spacing="3">BAIXAR RELATÓRIO ↓</text>
</g>

<!-- Decorativo: linhas geométricas no canto -->
<g transform="translate({W-200},{H-200})" stroke="{BLACK}" stroke-width="2" fill="none" opacity="0.3">
  <circle cx="80" cy="80" r="70"/>
  <circle cx="80" cy="80" r="40"/>
  <circle cx="80" cy="80" r="10" fill="{BLACK}"/>
</g>

{ilab_signature(H-90, color_i=BLACK, color_lab=BLACK, sub_color=BLACK)}
{handle(H-60, BLACK)}
'''
    render(body, "ilab-pesquisa.svg")


# ═══════════════════════════════════════════════
# 3) MANIFESTO — split duotone
# ═══════════════════════════════════════════════
def template_manifesto():
    # Diagonal split: warm-white acima, preto abaixo
    body = f'''
<rect width="{W}" height="{H}" fill="{WARM}"/>
<polygon points="0,{H} {W},{H} {W},520 0,720" fill="{BLACK}"/>
<line x1="0" y1="720" x2="{W}" y2="520" stroke="{ORANGE}" stroke-width="4"/>

<!-- Top: título sobre warm -->
<text x="80" y="140" font-family="JetBrains Mono, monospace" font-weight="700" font-size="14" fill="{ORANGE}" letter-spacing="4">— MANIFESTO 2026</text>

<text x="80" y="280" font-family="Poppins, sans-serif" font-weight="900" font-size="124" fill="{BLACK}" letter-spacing="-4">No que</text>
<text x="80" y="404" font-family="Poppins, sans-serif" font-weight="900" font-size="124" fill="url(#brand-grad-h)" letter-spacing="-4">acreditamos.</text>

<!-- Linha de detalhe -->
<line x1="80" y1="460" x2="240" y2="460" stroke="{ORANGE}" stroke-width="3"/>

<!-- Bottom: princípios sobre preto -->
<g transform="translate(80,800)" font-family="Poppins, sans-serif">
  <text x="0" y="0" font-weight="900" font-size="42" fill="{YELLOW}" letter-spacing="-1">01</text>
  <text x="100" y="-4" font-family="JetBrains Mono, monospace" font-weight="700" font-size="11" fill="{ORANGE}" letter-spacing="2">PRINCÍPIO</text>
  <text x="100" y="28" font-weight="700" font-size="26" fill="{WARM}">Direito sem fronteiras com tecnologia.</text>

  <text x="0" y="100" font-weight="900" font-size="42" fill="{YELLOW}" letter-spacing="-1">02</text>
  <text x="100" y="96" font-family="JetBrains Mono, monospace" font-weight="700" font-size="11" fill="{ORANGE}" letter-spacing="2">PRINCÍPIO</text>
  <text x="100" y="128" font-weight="700" font-size="26" fill="{WARM}">Estudantes como agentes de mudança.</text>

  <text x="0" y="200" font-weight="900" font-size="42" fill="{YELLOW}" letter-spacing="-1">03</text>
  <text x="100" y="196" font-family="JetBrains Mono, monospace" font-weight="700" font-size="11" fill="{ORANGE}" letter-spacing="2">PRINCÍPIO</text>
  <text x="100" y="228" font-weight="700" font-size="26" fill="{WARM}">Pesquisa aplicada ao mundo real.</text>

  <text x="0" y="300" font-weight="900" font-size="42" fill="{YELLOW}" letter-spacing="-1">04</text>
  <text x="100" y="296" font-family="JetBrains Mono, monospace" font-weight="700" font-size="11" fill="{ORANGE}" letter-spacing="2">PRINCÍPIO</text>
  <text x="100" y="328" font-weight="700" font-size="26" fill="{WARM}">Conhecimento aberto e colaborativo.</text>
</g>

{ilab_signature(H-90, color_i=YELLOW, color_lab=ORANGE, sub_color=WARM)}
{handle(H-60, YELLOW)}
'''
    render(body, "ilab-manifesto.svg")


# ═══════════════════════════════════════════════
# 4) EDITAL — bold gradient fullbleed
# ═══════════════════════════════════════════════
def template_edital():
    body = f'''
<rect width="{W}" height="{H}" fill="url(#brand-grad-red)"/>
<rect width="{W}" height="{H}" fill="url(#mesh-holo-1)"/>

<!-- Tarja superior -->
<rect x="0" y="0" width="{W}" height="80" fill="{BLACK}"/>
<text x="80" y="50" font-family="JetBrains Mono, monospace" font-weight="700" font-size="16" fill="{YELLOW}" letter-spacing="4">INSCRIÇÕES ABERTAS · 2026</text>

<!-- Estrela decorativa -->
<g transform="translate({W-160},220)" fill="{WARM}" opacity="0.5">
  <polygon points="0,-60 14,-20 60,-20 22,8 38,52 0,28 -38,52 -22,8 -60,-20 -14,-20"/>
</g>

<!-- Título massivo -->
<text x="80" y="280" font-family="Poppins, sans-serif" font-weight="900" font-size="118" fill="{WARM}" letter-spacing="-4">Faça parte</text>
<text x="80" y="404" font-family="Poppins, sans-serif" font-weight="900" font-size="118" fill="{WARM}" letter-spacing="-4">do</text>
<text x="80" y="528" font-family="Poppins, sans-serif" font-weight="900" font-size="118" fill="{BLACK}" letter-spacing="-4">iLab 2026.</text>

<!-- Card branco com info -->
<g transform="translate(80,620)">
  <rect width="920" height="320" rx="18" fill="{WARM}"/>
  <!-- Linha cabeçalho -->
  <rect x="0" y="0" width="120" height="6" fill="{ORANGE}"/>

  <text x="40" y="80" font-family="Poppins, sans-serif" font-weight="900" font-size="34" fill="{BLACK}" letter-spacing="-.8">Prazo · 15 de janeiro</text>
  <text x="40" y="116" font-family="JetBrains Mono, monospace" font-weight="700" font-size="14" fill="{ORANGE}" letter-spacing="2">23:59 · BRASÍLIA</text>

  <line x1="40" y1="148" x2="880" y2="148" stroke="{ORANGE}" stroke-width="1" opacity="0.4"/>

  <text x="40" y="194" font-family="Poppins, sans-serif" font-weight="900" font-size="22" fill="{BLACK}">Para quem</text>
  <text x="40" y="222" font-family="Montserrat, sans-serif" font-weight="400" font-size="17" fill="{BLACK}" opacity="0.85">Estudantes da Faculdade de Direito · FD-USP</text>

  <text x="40" y="266" font-family="Poppins, sans-serif" font-weight="900" font-size="60" fill="{ORANGE}" letter-spacing="-1.5">40 vagas</text>
  <text x="350" y="266" font-family="Montserrat, sans-serif" font-weight="700" font-size="16" fill="{BLACK}">Pesquisa + Projetos</text>
  <text x="350" y="288" font-family="Montserrat, sans-serif" font-weight="700" font-size="16" fill="{BLACK}">aplicados em legaltech</text>
</g>

<!-- CTA -->
<g transform="translate(80,1000)">
  <rect width="540" height="84" rx="42" fill="{BLACK}"/>
  <text x="270" y="54" font-family="JetBrains Mono, monospace" font-weight="700" font-size="18" fill="{YELLOW}" text-anchor="middle" letter-spacing="3">INSCREVA-SE — LINK NA BIO →</text>
</g>

{ilab_signature(H-90, color_i=BLACK, color_lab=BLACK, sub_color=BLACK)}
{handle(H-60, BLACK)}
'''
    render(body, "ilab-edital.svg")


# ═══════════════════════════════════════════════
# 5) MARCO — dark + holographic explosion
# ═══════════════════════════════════════════════
def template_marco():
    body = f'''
<rect width="{W}" height="{H}" fill="{BLACK_DEEP}"/>

<!-- Mesh holográfico atrás do número -->
<rect width="{W}" height="{H}" fill="url(#mesh-hot)"/>
<rect width="{W}" height="{H}" fill="url(#mesh-holo-2)"/>

<!-- Anéis concêntricos decorativos -->
<g transform="translate({W//2},480)" fill="none" stroke="{ORANGE}" opacity="0.25">
  <circle cx="0" cy="0" r="320" stroke-width="1"/>
  <circle cx="0" cy="0" r="240" stroke-width="1"/>
  <circle cx="0" cy="0" r="160" stroke-width="1"/>
</g>

<!-- Header -->
<text x="80" y="140" font-family="JetBrains Mono, monospace" font-weight="700" font-size="14" fill="{YELLOW}" letter-spacing="4">— MARCO HISTÓRICO</text>

<!-- Número massivo central com gradient -->
<text x="{W//2}" y="610" font-family="Poppins, sans-serif" font-weight="900" font-size="440" fill="url(#brand-grad)" text-anchor="middle" letter-spacing="-20">500</text>

<!-- Linha sob o número -->
<line x1="{W//2-180}" y1="660" x2="{W//2+180}" y2="660" stroke="{YELLOW}" stroke-width="3"/>

<!-- Descrição -->
<text x="{W//2}" y="740" font-family="Poppins, sans-serif" font-weight="900" font-size="56" fill="{WARM}" text-anchor="middle" letter-spacing="-1">estudantes formados</text>
<text x="{W//2}" y="800" font-family="Poppins, sans-serif" font-weight="700" font-size="32" fill="{ORANGE}" text-anchor="middle" letter-spacing="-.5">desde 2020</text>

<!-- Stats grid -->
<g transform="translate({W//2 - 380},950)" font-family="Poppins, sans-serif">
  <g transform="translate(0,0)">
    <text x="0" y="0" font-family="JetBrains Mono, monospace" font-weight="700" font-size="11" fill="{YELLOW}" letter-spacing="3">PROJETOS</text>
    <text x="0" y="56" font-weight="900" font-size="48" fill="{WARM}">42+</text>
  </g>
  <g transform="translate(280,0)">
    <text x="0" y="0" font-family="JetBrains Mono, monospace" font-weight="700" font-size="11" fill="{YELLOW}" letter-spacing="3">PARCEIROS</text>
    <text x="0" y="56" font-weight="900" font-size="48" fill="{WARM}">28</text>
  </g>
  <g transform="translate(560,0)">
    <text x="0" y="0" font-family="JetBrains Mono, monospace" font-weight="700" font-size="11" fill="{YELLOW}" letter-spacing="3">PUBLICAÇÕES</text>
    <text x="0" y="56" font-weight="900" font-size="48" fill="{WARM}">15</text>
  </g>
</g>

{ilab_signature(H-90, color_i=YELLOW, color_lab=ORANGE, sub_color=WARM)}
{handle(H-60, YELLOW)}
'''
    render(body, "ilab-marco.svg")


# ═══════════════════════════════════════════════
# 6) EDUCA — clean academic, two-column
# ═══════════════════════════════════════════════
def template_educa():
    body = f'''
<rect width="{W}" height="{H}" fill="{WARM}"/>
<rect width="{W}" height="{H}" fill="url(#paper-dots)"/>

<!-- Barra lateral de detalhe -->
<rect x="0" y="0" width="14" height="{H}" fill="url(#brand-grad)"/>

<!-- Header -->
<text x="80" y="140" font-family="JetBrains Mono, monospace" font-weight="700" font-size="14" fill="{ORANGE}" letter-spacing="4">— CONCEITO · LEGALTECH</text>

<!-- Conceito massivo -->
<text x="80" y="280" font-family="Poppins, sans-serif" font-weight="900" font-size="124" fill="{BLACK}" letter-spacing="-4">Legal</text>
<text x="80" y="404" font-family="Poppins, sans-serif" font-weight="900" font-size="124" fill="url(#brand-grad-h)" letter-spacing="-4">Design.</text>

<!-- Categoria gramatical -->
<text x="80" y="460" font-family="JetBrains Mono, monospace" font-weight="700" font-size="13" fill="{BLACK}" opacity="0.6" letter-spacing="3">SUBSTANTIVO · MÉTODO · M.</text>

<!-- Definição -->
<g transform="translate(80,550)">
  <line x1="0" y1="0" x2="60" y2="0" stroke="{ORANGE}" stroke-width="4"/>
  <text x="0" y="50" font-family="Poppins, sans-serif" font-weight="700" font-size="30" fill="{BLACK}" letter-spacing="-.5">Aplicação de princípios do</text>
  <text x="0" y="92" font-family="Poppins, sans-serif" font-weight="700" font-size="30" fill="{BLACK}" letter-spacing="-.5">design ao Direito para</text>
  <text x="0" y="134" font-family="Poppins, sans-serif" font-weight="700" font-size="30" fill="{ORANGE}" letter-spacing="-.5">tornar documentos jurídicos</text>
  <text x="0" y="176" font-family="Poppins, sans-serif" font-weight="700" font-size="30" fill="{ORANGE}" letter-spacing="-.5">claros e acessíveis.</text>
</g>

<!-- 3 Pilares em cards -->
<g transform="translate(80,820)">
  <text x="0" y="0" font-family="JetBrains Mono, monospace" font-weight="700" font-size="14" fill="{ORANGE}" letter-spacing="3">3 PILARES</text>

  <g transform="translate(0,40)">
    <rect width="290" height="140" rx="14" fill="{BLACK}"/>
    <text x="24" y="40" font-family="Poppins, sans-serif" font-weight="900" font-size="42" fill="{YELLOW}">01</text>
    <text x="24" y="90" font-family="Poppins, sans-serif" font-weight="700" font-size="18" fill="{WARM}">Empatia com</text>
    <text x="24" y="114" font-family="Poppins, sans-serif" font-weight="700" font-size="18" fill="{WARM}">o leitor</text>
  </g>
  <g transform="translate(310,40)">
    <rect width="290" height="140" rx="14" fill="{BLACK}"/>
    <text x="24" y="40" font-family="Poppins, sans-serif" font-weight="900" font-size="42" fill="{ORANGE}">02</text>
    <text x="24" y="90" font-family="Poppins, sans-serif" font-weight="700" font-size="18" fill="{WARM}">Visualização da</text>
    <text x="24" y="114" font-family="Poppins, sans-serif" font-weight="700" font-size="18" fill="{WARM}">informação</text>
  </g>
  <g transform="translate(620,40)">
    <rect width="290" height="140" rx="14" fill="{BLACK}"/>
    <text x="24" y="40" font-family="Poppins, sans-serif" font-weight="900" font-size="42" fill="{RED}">03</text>
    <text x="24" y="90" font-family="Poppins, sans-serif" font-weight="700" font-size="18" fill="{WARM}">Iteração e</text>
    <text x="24" y="114" font-family="Poppins, sans-serif" font-weight="700" font-size="18" fill="{WARM}">teste contínuo</text>
  </g>
</g>

<!-- Fonte / referência -->
<text x="80" y="1080" font-family="JetBrains Mono, monospace" font-weight="400" font-size="12" fill="{BLACK}" opacity="0.5" letter-spacing="2">Fonte: Margaret Hagan · Stanford Legal Design Lab.</text>

{ilab_signature(H-90, color_i=YELLOW, color_lab=ORANGE, sub_color=BLACK)}
{handle(H-60, ORANGE)}
'''
    render(body, "ilab-educa.svg")


if __name__ == "__main__":
    print("Gerando 6 templates editáveis (estilos variados, mesma identidade)...")
    template_citacao()
    template_pesquisa()
    template_manifesto()
    template_edital()
    template_marco()
    template_educa()
    print(f"\n{OUT}")
