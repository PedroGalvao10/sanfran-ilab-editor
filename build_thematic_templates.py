"""
Gera 6 templates temáticos diversos para a biblioteca visual (não-evento).
Mantém a linguagem visual da referência iLab Conecta:
- Fundo dark + globe wireframe
- Tipografia branca + laranja
- Layout 1080x1350 (post Instagram)

Temas:
  1. Citação    — featured quote
  2. Pesquisa   — research/study release
  3. Manifesto  — values/principles
  4. Edital     — open applications
  5. Marco      — milestone/achievement
  6. Educa      — concept explainer

Saída: assets/templates/*.svg
"""
from pathlib import Path

OUT = Path(__file__).parent / "assets" / "templates"
OUT.mkdir(parents=True, exist_ok=True)

BG = "#0F0F0F"
ORANGE = "#FF6B35"
YELLOW = "#F4C430"
WHITE = "#FAFAFA"
GRAY = "#888"

W, H = 1080, 1350


def base_defs():
    return f'''
<defs>
  <radialGradient id="bg-radial" cx="50%" cy="100%" r="80%">
    <stop offset="0%" stop-color="#2a1a0a" stop-opacity="0.5"/>
    <stop offset="100%" stop-color="{BG}" stop-opacity="1"/>
  </radialGradient>
  <linearGradient id="orange-grad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{YELLOW}"/>
    <stop offset="100%" stop-color="{ORANGE}"/>
  </linearGradient>
  <pattern id="dots" x="0" y="0" width="36" height="36" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1" fill="{ORANGE}" opacity="0.15"/>
  </pattern>
  <symbol id="globe-wire" viewBox="0 0 400 400">
    <g fill="none" stroke="{ORANGE}" stroke-width="0.8" opacity="0.35">
      <circle cx="200" cy="200" r="200"/>
      <ellipse cx="200" cy="200" rx="200" ry="60"/>
      <ellipse cx="200" cy="200" rx="200" ry="120"/>
      <ellipse cx="200" cy="200" rx="60" ry="200"/>
      <ellipse cx="200" cy="200" rx="120" ry="200"/>
      <line x1="0" y1="200" x2="400" y2="200"/>
      <line x1="200" y1="0" x2="200" y2="400"/>
    </g>
  </symbol>
</defs>'''


def background_layer(globe_position="default"):
    """Fundo base com globos decorativos."""
    base = f'''
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect width="{W}" height="{H}" fill="url(#bg-radial)"/>
<rect width="{W}" height="{H}" fill="url(#dots)"/>'''
    if globe_position == "default":
        base += f'''
<use href="#globe-wire" x="{W-280}" y="-80" width="400" height="400"/>
<use href="#globe-wire" x="-180" y="{H-220}" width="400" height="400"/>'''
    elif globe_position == "center":
        base += f'''
<use href="#globe-wire" x="{W//2-300}" y="{H//2-300}" width="600" height="600" opacity="0.4"/>'''
    elif globe_position == "top":
        base += f'''
<use href="#globe-wire" x="-100" y="-100" width="400" height="400"/>
<use href="#globe-wire" x="{W-300}" y="-100" width="400" height="400"/>'''
    return base


def footer_brand():
    return f'''
<g transform="translate(80,{H-90})">
  <text font-family="Poppins, sans-serif" font-weight="900" font-size="28" letter-spacing="-1">
    <tspan fill="{YELLOW}">i</tspan><tspan fill="{ORANGE}">Lab</tspan>
  </text>
  <text x="0" y="36" font-family="JetBrains Mono, monospace" font-weight="700" font-size="12" fill="{WHITE}" letter-spacing="3" opacity="0.6">SANFRAN · FD-USP</text>
</g>
<text x="{W-80}" y="{H-60}" font-family="JetBrains Mono, monospace" font-weight="700" font-size="13" fill="{ORANGE}" text-anchor="end" letter-spacing="3">@SANFRANILAB</text>'''


def section_tag(label: str, y: int = 120):
    return f'''
<rect x="80" y="{y-30}" width="220" height="44" rx="22" fill="none" stroke="{ORANGE}" stroke-width="2"/>
<text x="190" y="{y}" font-family="JetBrains Mono, monospace" font-weight="700" font-size="14" fill="{ORANGE}" text-anchor="middle" letter-spacing="3">{label}</text>'''


def render(svg_body: str, filename: str):
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
{base_defs()}
{svg_body}
</svg>'''
    (OUT / filename).write_text(svg, encoding="utf-8")
    print(f"  OK {filename}")


# ─────────────────────────────────────────
# 1) CITAÇÃO — featured quote
# ─────────────────────────────────────────
def template_citacao():
    body = (
        background_layer("center")
        + section_tag("CITAÇÃO")
        + f'''
<!-- Aspas decorativas gigantes -->
<text x="80" y="380" font-family="Poppins, sans-serif" font-weight="900" font-size="280" fill="{ORANGE}" opacity="0.85">"</text>

<!-- Citação principal -->
<text x="80" y="540" font-family="Poppins, sans-serif" font-weight="700" font-size="58" fill="{WHITE}" letter-spacing="-1.5">A inovação no</text>
<text x="80" y="612" font-family="Poppins, sans-serif" font-weight="700" font-size="58" fill="{WHITE}" letter-spacing="-1.5">Direito começa</text>
<text x="80" y="684" font-family="Poppins, sans-serif" font-weight="700" font-size="58" fill="{ORANGE}" letter-spacing="-1.5">por dentro</text>
<text x="80" y="756" font-family="Poppins, sans-serif" font-weight="700" font-size="58" fill="{ORANGE}" letter-spacing="-1.5">das salas de aula.</text>

<!-- Linha + autoria -->
<line x1="80" y1="900" x2="200" y2="900" stroke="{ORANGE}" stroke-width="3"/>
<text x="80" y="960" font-family="Poppins, sans-serif" font-weight="900" font-size="32" fill="{WHITE}" letter-spacing="-.5">NOME DO AUTOR</text>
<text x="80" y="1000" font-family="JetBrains Mono, monospace" font-weight="400" font-size="18" fill="{WHITE}" opacity="0.75" letter-spacing="1.5">CARGO · INSTITUIÇÃO</text>
'''
        + footer_brand()
    )
    render(body, "ilab-citacao.svg")


# ─────────────────────────────────────────
# 2) PESQUISA — research release
# ─────────────────────────────────────────
def template_pesquisa():
    body = (
        background_layer("top")
        + section_tag("NOVA PESQUISA")
        + f'''
<!-- Título da pesquisa -->
<text x="80" y="260" font-family="Poppins, sans-serif" font-weight="900" font-size="88" fill="{WHITE}" letter-spacing="-3">Direito</text>
<text x="80" y="354" font-family="Poppins, sans-serif" font-weight="900" font-size="88" fill="{ORANGE}" letter-spacing="-3">+ IA</text>
<text x="80" y="448" font-family="Poppins, sans-serif" font-weight="900" font-size="88" fill="{WHITE}" letter-spacing="-3">no Brasil</text>
<text x="80" y="500" font-family="JetBrains Mono, monospace" font-weight="700" font-size="16" fill="{ORANGE}" letter-spacing="3">RELATÓRIO ANUAL · 2026</text>

<!-- Cards de números -->
<g transform="translate(80,580)">
  <rect width="280" height="160" rx="12" fill="none" stroke="{ORANGE}" stroke-width="2"/>
  <text x="24" y="80" font-family="Poppins, sans-serif" font-weight="900" font-size="76" fill="{ORANGE}">87%</text>
  <text x="24" y="118" font-family="JetBrains Mono, monospace" font-weight="700" font-size="13" fill="{WHITE}" letter-spacing="2">DOS ESCRITÓRIOS</text>
  <text x="24" y="140" font-family="JetBrains Mono, monospace" font-weight="700" font-size="13" fill="{WHITE}" letter-spacing="2">USAM IA EM 2026</text>
</g>

<g transform="translate(380,580)">
  <rect width="280" height="160" rx="12" fill="none" stroke="{YELLOW}" stroke-width="2"/>
  <text x="24" y="80" font-family="Poppins, sans-serif" font-weight="900" font-size="76" fill="{YELLOW}">3.2x</text>
  <text x="24" y="118" font-family="JetBrains Mono, monospace" font-weight="700" font-size="13" fill="{WHITE}" letter-spacing="2">AUMENTO DE</text>
  <text x="24" y="140" font-family="JetBrains Mono, monospace" font-weight="700" font-size="13" fill="{WHITE}" letter-spacing="2">PRODUTIVIDADE</text>
</g>

<!-- Subtítulo + autoria -->
<text x="80" y="820" font-family="Poppins, sans-serif" font-weight="700" font-size="22" fill="{WHITE}" letter-spacing="-.3">Estudo conduzido por:</text>
<text x="80" y="864" font-family="Poppins, sans-serif" font-weight="900" font-size="32" fill="{ORANGE}" letter-spacing="-.5">SanFran iLab</text>
<text x="80" y="908" font-family="JetBrains Mono, monospace" font-weight="400" font-size="16" fill="{WHITE}" opacity="0.7" letter-spacing="1">Faculdade de Direito da USP · 2026</text>

<!-- CTA -->
<g transform="translate(80,1010)">
  <rect width="380" height="64" rx="32" fill="url(#orange-grad)"/>
  <text x="190" y="40" font-family="JetBrains Mono, monospace" font-weight="700" font-size="15" fill="{BG}" text-anchor="middle" letter-spacing="3">BAIXE O RELATÓRIO ↓</text>
</g>
'''
        + footer_brand()
    )
    render(body, "ilab-pesquisa.svg")


# ─────────────────────────────────────────
# 3) MANIFESTO — values/principles
# ─────────────────────────────────────────
def template_manifesto():
    body = (
        background_layer("default")
        + section_tag("MANIFESTO", y=120)
        + f'''
<!-- Título -->
<text x="80" y="260" font-family="Poppins, sans-serif" font-weight="900" font-size="120" fill="{WHITE}" letter-spacing="-4">No que</text>
<text x="80" y="380" font-family="Poppins, sans-serif" font-weight="900" font-size="120" fill="{ORANGE}" letter-spacing="-4">acreditamos.</text>

<!-- Princípios numerados -->
<g transform="translate(80,520)" font-family="Poppins, sans-serif">
  <line x1="0" y1="0" x2="920" y2="0" stroke="{ORANGE}" stroke-width="1" opacity="0.4"/>
  <text x="0" y="60" font-weight="900" font-size="28" fill="{ORANGE}">01.</text>
  <text x="90" y="60" font-weight="700" font-size="28" fill="{WHITE}">Direito sem fronteiras com tecnologia.</text>

  <line x1="0" y1="100" x2="920" y2="100" stroke="{ORANGE}" stroke-width="1" opacity="0.4"/>
  <text x="0" y="160" font-weight="900" font-size="28" fill="{ORANGE}">02.</text>
  <text x="90" y="160" font-weight="700" font-size="28" fill="{WHITE}">Estudantes como agentes de mudança.</text>

  <line x1="0" y1="200" x2="920" y2="200" stroke="{ORANGE}" stroke-width="1" opacity="0.4"/>
  <text x="0" y="260" font-weight="900" font-size="28" fill="{ORANGE}">03.</text>
  <text x="90" y="260" font-weight="700" font-size="28" fill="{WHITE}">Pesquisa aplicada ao mundo real.</text>

  <line x1="0" y1="300" x2="920" y2="300" stroke="{ORANGE}" stroke-width="1" opacity="0.4"/>
  <text x="0" y="360" font-weight="900" font-size="28" fill="{ORANGE}">04.</text>
  <text x="90" y="360" font-weight="700" font-size="28" fill="{WHITE}">Diálogo entre Academia e mercado.</text>

  <line x1="0" y1="400" x2="920" y2="400" stroke="{ORANGE}" stroke-width="1" opacity="0.4"/>
  <text x="0" y="460" font-weight="900" font-size="28" fill="{ORANGE}">05.</text>
  <text x="90" y="460" font-weight="700" font-size="28" fill="{WHITE}">Conhecimento aberto e colaborativo.</text>

  <line x1="0" y1="500" x2="920" y2="500" stroke="{ORANGE}" stroke-width="1" opacity="0.4"/>
</g>
'''
        + footer_brand()
    )
    render(body, "ilab-manifesto.svg")


# ─────────────────────────────────────────
# 4) EDITAL — open applications
# ─────────────────────────────────────────
def template_edital():
    body = (
        background_layer("default")
        + section_tag("INSCRIÇÕES ABERTAS")
        + f'''
<!-- Título -->
<text x="80" y="290" font-family="Poppins, sans-serif" font-weight="900" font-size="100" fill="{WHITE}" letter-spacing="-3">Faça</text>
<text x="80" y="400" font-family="Poppins, sans-serif" font-weight="900" font-size="100" fill="{WHITE}" letter-spacing="-3">parte do</text>
<text x="80" y="510" font-family="Poppins, sans-serif" font-weight="900" font-size="100" fill="{ORANGE}" letter-spacing="-3">iLab 2026.</text>

<!-- Info blocks -->
<g transform="translate(80,620)" font-family="Poppins, sans-serif">
  <!-- Calendário -->
  <g>
    <rect x="0" y="6" width="56" height="56" rx="8" fill="none" stroke="{ORANGE}" stroke-width="3"/>
    <line x1="0" y1="22" x2="56" y2="22" stroke="{ORANGE}" stroke-width="3"/>
    <rect x="14" y="2" width="6" height="12" rx="2" fill="{ORANGE}"/>
    <rect x="36" y="2" width="6" height="12" rx="2" fill="{ORANGE}"/>
    <text x="80" y="34" font-weight="900" font-size="32" fill="{WHITE}" letter-spacing="-.5">PRAZO · 15.JAN</text>
    <text x="80" y="62" font-family="JetBrains Mono, monospace" font-weight="700" font-size="14" fill="{WHITE}" opacity="0.7" letter-spacing="2">23:59 · HORÁRIO DE BRASÍLIA</text>
  </g>
</g>

<g transform="translate(80,740)" font-family="Poppins, sans-serif">
  <!-- Pessoa -->
  <g>
    <circle cx="28" cy="22" r="14" fill="none" stroke="{ORANGE}" stroke-width="3"/>
    <path d="M4,60 C4,40 16,32 28,32 C40,32 52,40 52,60" fill="none" stroke="{ORANGE}" stroke-width="3"/>
    <text x="80" y="32" font-weight="900" font-size="26" fill="{WHITE}" letter-spacing="-.3">PARA QUEM</text>
    <text x="80" y="60" font-family="JetBrains Mono, monospace" font-weight="400" font-size="15" fill="{WHITE}" opacity="0.85" letter-spacing="1">Estudantes da Faculdade de Direito · FD-USP</text>
  </g>
</g>

<g transform="translate(80,870)" font-family="Poppins, sans-serif">
  <!-- Vagas -->
  <g>
    <text x="0" y="36" font-weight="900" font-size="52" fill="{ORANGE}" letter-spacing="-2">40 VAGAS</text>
    <text x="280" y="36" font-family="JetBrains Mono, monospace" font-weight="700" font-size="14" fill="{WHITE}" letter-spacing="2">PARA PESQUISA</text>
    <text x="280" y="58" font-family="JetBrains Mono, monospace" font-weight="700" font-size="14" fill="{WHITE}" letter-spacing="2">+ PROJETOS APLICADOS</text>
  </g>
</g>

<!-- CTA -->
<g transform="translate(80,990)">
  <rect width="440" height="76" rx="38" fill="url(#orange-grad)"/>
  <text x="220" y="48" font-family="JetBrains Mono, monospace" font-weight="700" font-size="17" fill="{BG}" text-anchor="middle" letter-spacing="3">INSCREVA-SE NO LINK DA BIO →</text>
</g>
'''
        + footer_brand()
    )
    render(body, "ilab-edital.svg")


# ─────────────────────────────────────────
# 5) MARCO — milestone
# ─────────────────────────────────────────
def template_marco():
    body = (
        background_layer("default")
        + section_tag("MARCO 2026", y=140)
        + f'''
<!-- Número gigante -->
<text x="80" y="540" font-family="Poppins, sans-serif" font-weight="900" font-size="400" fill="url(#orange-grad)" letter-spacing="-20">500</text>

<!-- Linha decorativa -->
<line x1="80" y1="600" x2="320" y2="600" stroke="{ORANGE}" stroke-width="4"/>

<!-- Descrição -->
<text x="80" y="680" font-family="Poppins, sans-serif" font-weight="900" font-size="56" fill="{WHITE}" letter-spacing="-1.5">estudantes</text>
<text x="80" y="744" font-family="Poppins, sans-serif" font-weight="900" font-size="56" fill="{WHITE}" letter-spacing="-1.5">já passaram</text>
<text x="80" y="808" font-family="Poppins, sans-serif" font-weight="900" font-size="56" fill="{ORANGE}" letter-spacing="-1.5">pelo iLab.</text>

<!-- Contexto -->
<text x="80" y="900" font-family="JetBrains Mono, monospace" font-weight="700" font-size="14" fill="{ORANGE}" letter-spacing="3">DESDE 2020</text>
<text x="80" y="940" font-family="Montserrat, sans-serif" font-weight="400" font-size="20" fill="{WHITE}" opacity="0.85">Construindo uma nova geração de juristas</text>
<text x="80" y="970" font-family="Montserrat, sans-serif" font-weight="400" font-size="20" fill="{WHITE}" opacity="0.85">capazes de transformar o Direito brasileiro.</text>

<!-- Stats grid -->
<g transform="translate(80,1030)" font-family="JetBrains Mono, monospace">
  <text x="0" y="20" font-weight="700" font-size="11" fill="{ORANGE}" letter-spacing="2">PROJETOS</text>
  <text x="0" y="56" font-family="Poppins, sans-serif" font-weight="900" font-size="36" fill="{WHITE}">42+</text>

  <text x="200" y="20" font-weight="700" font-size="11" fill="{ORANGE}" letter-spacing="2">PARCEIROS</text>
  <text x="200" y="56" font-family="Poppins, sans-serif" font-weight="900" font-size="36" fill="{WHITE}">28</text>

  <text x="400" y="20" font-weight="700" font-size="11" fill="{ORANGE}" letter-spacing="2">PUBLICAÇÕES</text>
  <text x="400" y="56" font-family="Poppins, sans-serif" font-weight="900" font-size="36" fill="{WHITE}">15</text>
</g>
'''
        + footer_brand()
    )
    render(body, "ilab-marco.svg")


# ─────────────────────────────────────────
# 6) EDUCA — concept explainer
# ─────────────────────────────────────────
def template_educa():
    body = (
        background_layer("default")
        + section_tag("CONCEITO", y=120)
        + f'''
<!-- Conceito gigante -->
<text x="80" y="290" font-family="Poppins, sans-serif" font-weight="900" font-size="140" fill="{WHITE}" letter-spacing="-4">Legal</text>
<text x="80" y="430" font-family="Poppins, sans-serif" font-weight="900" font-size="140" fill="{ORANGE}" letter-spacing="-4">Design</text>
<text x="80" y="490" font-family="JetBrains Mono, monospace" font-weight="700" font-size="16" fill="{WHITE}" opacity="0.6" letter-spacing="4">SUBSTANTIVO · MÉTODO</text>

<!-- Definição -->
<g transform="translate(80,550)">
  <line x1="0" y1="0" x2="60" y2="0" stroke="{ORANGE}" stroke-width="4"/>
  <text x="0" y="50" font-family="Poppins, sans-serif" font-weight="700" font-size="26" fill="{WHITE}">Aplicação de princípios</text>
  <text x="0" y="86" font-family="Poppins, sans-serif" font-weight="700" font-size="26" fill="{WHITE}">do design ao Direito para</text>
  <text x="0" y="122" font-family="Poppins, sans-serif" font-weight="700" font-size="26" fill="{ORANGE}">tornar documentos jurídicos</text>
  <text x="0" y="158" font-family="Poppins, sans-serif" font-weight="700" font-size="26" fill="{ORANGE}">mais claros e acessíveis.</text>
</g>

<!-- Pontos-chave -->
<g transform="translate(80,800)" font-family="Poppins, sans-serif">
  <text x="0" y="0" font-family="JetBrains Mono, monospace" font-weight="700" font-size="14" fill="{ORANGE}" letter-spacing="3">3 PILARES</text>

  <g transform="translate(0,40)">
    <circle cx="14" cy="14" r="12" fill="none" stroke="{ORANGE}" stroke-width="2"/>
    <text x="14" y="20" font-weight="900" font-size="14" fill="{ORANGE}" text-anchor="middle">1</text>
    <text x="44" y="22" font-weight="700" font-size="22" fill="{WHITE}">Empatia com o leitor</text>
  </g>

  <g transform="translate(0,90)">
    <circle cx="14" cy="14" r="12" fill="none" stroke="{ORANGE}" stroke-width="2"/>
    <text x="14" y="20" font-weight="900" font-size="14" fill="{ORANGE}" text-anchor="middle">2</text>
    <text x="44" y="22" font-weight="700" font-size="22" fill="{WHITE}">Visualização da informação</text>
  </g>

  <g transform="translate(0,140)">
    <circle cx="14" cy="14" r="12" fill="none" stroke="{ORANGE}" stroke-width="2"/>
    <text x="14" y="20" font-weight="900" font-size="14" fill="{ORANGE}" text-anchor="middle">3</text>
    <text x="44" y="22" font-weight="700" font-size="22" fill="{WHITE}">Iteração e teste</text>
  </g>
</g>

<!-- Citação fonte -->
<text x="80" y="1080" font-family="JetBrains Mono, monospace" font-weight="400" font-size="12" fill="{WHITE}" opacity="0.5" letter-spacing="2">Fonte: Margaret Hagan, Stanford Legal Design Lab.</text>
'''
        + footer_brand()
    )
    render(body, "ilab-educa.svg")


if __name__ == "__main__":
    print("Gerando 6 templates temáticos diversos...")
    template_citacao()
    template_pesquisa()
    template_manifesto()
    template_edital()
    template_marco()
    template_educa()
    print(f"\nTotal: 6 templates em {OUT}")
