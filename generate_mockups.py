"""
Gera mockups reais SVG:
- 3 posts Instagram (1080x1080)
- 2 slides apresentação (1920x1080)
- 1 cartão visita (900x500, frente)
- 1 cartão visita verso

Usa: Lex (mascote raposa) + Fluent 3D PNGs + paleta oficial
Resultado: SVGs prontos para baixar como PNG transparente em alta resolução
"""
from pathlib import Path

AMBAR    = "#F4C430"
LARANJA  = "#FF6B35"
CARMESIM = "#C41E3A"
PRETO    = "#1A1A1A"
CREME    = "#FAF3E0"

ROOT = Path(__file__).parent
OUT = ROOT / "assets" / "mockups"
OUT.mkdir(parents=True, exist_ok=True)


# ════════════════════════════════════════════════
# Helper: dot pattern background
# ════════════════════════════════════════════════
DOT_PATTERN = f'''<defs>
  <pattern id="dots" x="0" y="0" width="32" height="32" patternUnits="userSpaceOnUse">
    <circle cx="16" cy="16" r="1.2" fill="{AMBAR}" opacity="0.4"/>
  </pattern>
</defs>'''

GRAD_AMBAR_ORANGE = f'''<linearGradient id="g-bar" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{AMBAR}"/>
  <stop offset="1" stop-color="{LARANJA}"/>
</linearGradient>'''


# ════════════════════════════════════════════════
# INSTAGRAM POSTS · 1080x1080
# ════════════════════════════════════════════════
def insta_announcement():
    """Post de anúncio com Lex + headline."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>
    {DOT_PATTERN}
    {GRAD_AMBAR_ORANGE}
  </defs>
  <!-- Background dark com dots -->
  <rect width="1080" height="1080" fill="{PRETO}"/>
  <rect width="1080" height="1080" fill="url(#dots)"/>
  <!-- Top gradient bar -->
  <rect x="0" y="0" width="1080" height="8" fill="url(#g-bar)"/>
  <!-- Label superior -->
  <text x="80" y="120" font-family="JetBrains Mono,monospace" font-size="22" font-weight="700" letter-spacing="6" fill="{AMBAR}">SANFRAN · ILAB · 2026</text>
  <!-- Headline -->
  <text x="80" y="320" font-family="Poppins,sans-serif" font-weight="900" font-size="96" fill="{CREME}">LANÇAMENTO</text>
  <text x="80" y="420" font-family="Poppins,sans-serif" font-weight="900" font-size="96" fill="url(#g-bar)">OFICIAL</text>
  <!-- Subtitle -->
  <text x="80" y="510" font-family="Montserrat,sans-serif" font-size="34" fill="{CREME}" opacity="0.85">Laboratório de Inovação em</text>
  <text x="80" y="555" font-family="Montserrat,sans-serif" font-size="34" fill="{CREME}" opacity="0.85">Direito &amp; Tecnologia · FD-USP</text>
  <!-- Lex mascote (foguete laranja sobre fundo claro) -->
  <g transform="translate(720 580)">
    <circle cx="150" cy="150" r="200" fill="{AMBAR}" opacity="0.1"/>
    <circle cx="150" cy="150" r="160" fill="{AMBAR}" opacity="0.2"/>
    <image href="assets/foxes/intelecto_idea.png" x="-30" y="-30" width="360" height="360" preserveAspectRatio="xMidYMid meet"/>
  </g>
  <!-- CTA bottom -->
  <rect x="80" y="900" width="280" height="76" rx="38" fill="url(#g-bar)"/>
  <text x="220" y="950" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="24" fill="{PRETO}">SAIBA MAIS →</text>
  <!-- Logo bottom right -->
  <g transform="translate(900 980)">
    <text x="0" y="0" font-family="Poppins,sans-serif" font-weight="900" font-size="32" fill="{AMBAR}">iLab</text>
    <text x="0" y="22" font-family="JetBrains Mono,monospace" font-size="11" fill="{CREME}" opacity="0.6" letter-spacing="2">SANFRAN</text>
  </g>
</svg>'''


def insta_quote():
    """Post de citação editorial."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>{GRAD_AMBAR_ORANGE}</defs>
  <rect width="1080" height="1080" fill="{CREME}"/>
  <!-- Decorative quote mark -->
  <text x="80" y="380" font-family="Poppins,sans-serif" font-weight="900" font-size="380" fill="{AMBAR}" opacity="0.18">"</text>
  <!-- Quote text -->
  <text x="120" y="520" font-family="Poppins,sans-serif" font-weight="900" font-size="56" fill="{PRETO}">O futuro do Direito</text>
  <text x="120" y="600" font-family="Poppins,sans-serif" font-weight="900" font-size="56" fill="{PRETO}">se escreve no encontro</text>
  <text x="120" y="680" font-family="Poppins,sans-serif" font-weight="900" font-size="56" fill="url(#g-bar)">entre tradição e código.</text>
  <!-- Divider -->
  <rect x="120" y="760" width="80" height="3" fill="{LARANJA}"/>
  <!-- Attribution -->
  <text x="120" y="810" font-family="JetBrains Mono,monospace" font-size="20" font-weight="700" letter-spacing="3" fill="{PRETO}">SANFRAN iLAB · MANIFESTO</text>
  <!-- Sparkle -->
  <image href="assets/fluent3d/sparkles.png" x="850" y="80" width="160" height="160"/>
  <!-- Bottom logo -->
  <text x="540" y="1000" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="28" fill="{LARANJA}">iLab</text>
  <text x="540" y="1030" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="11" fill="{PRETO}" opacity="0.5" letter-spacing="2">SANFRAN · DIREITO &amp; TECNOLOGIA</text>
</svg>'''


def insta_event():
    """Post de evento com data destacada."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>
    {DOT_PATTERN}
    {GRAD_AMBAR_ORANGE}
    <linearGradient id="g-vert" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{AMBAR}"/>
      <stop offset="1" stop-color="{LARANJA}"/>
    </linearGradient>
  </defs>
  <!-- Split: top dark with dots, bottom amber -->
  <rect width="1080" height="680" fill="{PRETO}"/>
  <rect width="1080" height="680" fill="url(#dots)"/>
  <rect y="680" width="1080" height="400" fill="url(#g-vert)"/>
  <!-- Label top -->
  <text x="80" y="100" font-family="JetBrains Mono,monospace" font-size="20" font-weight="700" letter-spacing="5" fill="{AMBAR}">EVENTO · 2026</text>
  <!-- Title -->
  <text x="80" y="220" font-family="Poppins,sans-serif" font-weight="900" font-size="88" fill="{CREME}">PALESTRA</text>
  <text x="80" y="310" font-family="Poppins,sans-serif" font-weight="900" font-size="88" fill="{AMBAR}">MAGNA</text>
  <!-- Subtitle -->
  <text x="80" y="380" font-family="Montserrat,sans-serif" font-size="28" fill="{CREME}" opacity="0.85">IA, Direito e a Próxima Década</text>
  <!-- Speaker placeholder -->
  <g transform="translate(80 460)">
    <circle cx="60" cy="60" r="60" fill="{AMBAR}"/>
    <image href="assets/avatars/maria.svg" x="0" y="0" width="120" height="120"/>
    <text x="150" y="55" font-family="Poppins,sans-serif" font-weight="900" font-size="32" fill="{CREME}">Dra. Maria Silva</text>
    <text x="150" y="90" font-family="JetBrains Mono,monospace" font-size="16" fill="{CREME}" opacity="0.7" letter-spacing="1.5">FACULDADE DE DIREITO · USP</text>
  </g>
  <!-- Date block bottom -->
  <g transform="translate(80 760)">
    <text font-family="Poppins,sans-serif" font-weight="900" font-size="200" fill="{PRETO}">15</text>
    <text x="220" y="100" font-family="Poppins,sans-serif" font-weight="900" font-size="60" fill="{PRETO}">MAIO</text>
    <text x="220" y="155" font-family="JetBrains Mono,monospace" font-size="22" font-weight="700" fill="{PRETO}">19h · AUD. PROF. ALCINO LÁZARO</text>
    <text x="220" y="185" font-family="JetBrains Mono,monospace" font-size="22" font-weight="700" fill="{CARMESIM}">PRESENCIAL + ONLINE</text>
  </g>
</svg>'''


# ════════════════════════════════════════════════
# SLIDES · 1920x1080
# ════════════════════════════════════════════════
def slide_cover():
    """Slide capa."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <defs>{DOT_PATTERN}{GRAD_AMBAR_ORANGE}</defs>
  <rect width="1920" height="1080" fill="{PRETO}"/>
  <rect width="1920" height="1080" fill="url(#dots)"/>
  <!-- Gradient bar left -->
  <rect x="0" y="0" width="8" height="1080" fill="url(#g-bar)"/>
  <!-- Top label -->
  <text x="120" y="180" font-family="JetBrains Mono,monospace" font-size="22" font-weight="700" letter-spacing="6" fill="{AMBAR}">CAPÍTULO 01 · APRESENTAÇÃO</text>
  <!-- Title -->
  <text x="120" y="380" font-family="Poppins,sans-serif" font-weight="900" font-size="148" fill="{CREME}">SanFran</text>
  <text x="120" y="540" font-family="Poppins,sans-serif" font-weight="900" font-size="148" fill="url(#g-bar)" font-style="italic">iLab</text>
  <!-- Subtitle -->
  <text x="120" y="650" font-family="Montserrat,sans-serif" font-size="40" fill="{CREME}" opacity="0.8">Laboratório de Inovação em Direito &amp; Tecnologia</text>
  <text x="120" y="710" font-family="Montserrat,sans-serif" font-size="32" fill="{CREME}" opacity="0.6">Faculdade de Direito do Largo São Francisco · USP</text>
  <!-- Lex right -->
  <g transform="translate(1280 280)">
    <circle cx="220" cy="280" r="280" fill="{AMBAR}" opacity="0.08"/>
    <circle cx="220" cy="280" r="220" fill="{AMBAR}" opacity="0.14"/>
    <image href="assets/foxes/intelecto_idea.png" x="0" y="60" width="440" height="440" preserveAspectRatio="xMidYMid meet"/>
  </g>
  <!-- Bottom info -->
  <rect x="120" y="940" width="1680" height="2" fill="{AMBAR}" opacity="0.3"/>
  <text x="120" y="1000" font-family="JetBrains Mono,monospace" font-size="20" letter-spacing="2" fill="{CREME}" opacity="0.7">© 2026 · SANFRAN iLAB · FD-USP</text>
  <text x="1800" y="1000" text-anchor="end" font-family="JetBrains Mono,monospace" font-size="20" letter-spacing="2" fill="{CREME}" opacity="0.7">01 / 24</text>
</svg>'''


def slide_content():
    """Slide de conteúdo (3 colunas com Fluent 3D)."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <defs>{GRAD_AMBAR_ORANGE}</defs>
  <rect width="1920" height="1080" fill="{CREME}"/>
  <!-- Top accent -->
  <rect width="1920" height="6" fill="url(#g-bar)"/>
  <!-- Section label -->
  <text x="120" y="120" font-family="JetBrains Mono,monospace" font-size="20" font-weight="700" letter-spacing="5" fill="{LARANJA}">03 · NOSSOS PILARES</text>
  <!-- Title -->
  <text x="120" y="220" font-family="Poppins,sans-serif" font-weight="900" font-size="84" fill="{PRETO}">Três frentes de atuação</text>
  <!-- 3 columns -->
  <g transform="translate(120 360)">
    <!-- Col 1 -->
    <rect x="0" y="0" width="540" height="560" fill="{PRETO}" rx="20"/>
    <image href="assets/fluent3d/brain.png" x="60" y="60" width="160" height="160"/>
    <text x="60" y="280" font-family="Poppins,sans-serif" font-weight="900" font-size="42" fill="{AMBAR}">Pesquisa</text>
    <rect x="60" y="300" width="60" height="3" fill="{LARANJA}"/>
    <text x="60" y="360" font-family="Montserrat,sans-serif" font-size="22" fill="{CREME}" opacity="0.85">Grupos de estudo em</text>
    <text x="60" y="395" font-family="Montserrat,sans-serif" font-size="22" fill="{CREME}" opacity="0.85">IA, blockchain, LGPD e</text>
    <text x="60" y="430" font-family="Montserrat,sans-serif" font-size="22" fill="{CREME}" opacity="0.85">novos modelos contratuais.</text>
    <text x="60" y="510" font-family="JetBrains Mono,monospace" font-size="16" letter-spacing="2" fill="{AMBAR}">12 GRUPOS · 80 ALUNOS</text>
  </g>
  <g transform="translate(700 360)">
    <rect x="0" y="0" width="540" height="560" fill="{LARANJA}" rx="20"/>
    <image href="assets/fluent3d/handshake.png" x="60" y="60" width="160" height="160"/>
    <text x="60" y="280" font-family="Poppins,sans-serif" font-weight="900" font-size="42" fill="{CREME}">Parcerias</text>
    <rect x="60" y="300" width="60" height="3" fill="{AMBAR}"/>
    <text x="60" y="360" font-family="Montserrat,sans-serif" font-size="22" fill="{CREME}" opacity="0.95">Escritórios, legaltechs e</text>
    <text x="60" y="395" font-family="Montserrat,sans-serif" font-size="22" fill="{CREME}" opacity="0.95">universidades em rede</text>
    <text x="60" y="430" font-family="Montserrat,sans-serif" font-size="22" fill="{CREME}" opacity="0.95">internacional ativa.</text>
    <text x="60" y="510" font-family="JetBrains Mono,monospace" font-size="16" letter-spacing="2" fill="{PRETO}">18 PARCEIROS · 6 PAÍSES</text>
  </g>
  <g transform="translate(1280 360)">
    <rect x="0" y="0" width="540" height="560" fill="{AMBAR}" rx="20"/>
    <image href="assets/fluent3d/rocket.png" x="60" y="60" width="160" height="160"/>
    <text x="60" y="280" font-family="Poppins,sans-serif" font-weight="900" font-size="42" fill="{PRETO}">Lançamentos</text>
    <rect x="60" y="300" width="60" height="3" fill="{CARMESIM}"/>
    <text x="60" y="360" font-family="Montserrat,sans-serif" font-size="22" fill="{PRETO}">Eventos, publicações,</text>
    <text x="60" y="395" font-family="Montserrat,sans-serif" font-size="22" fill="{PRETO}">protótipos de produto e</text>
    <text x="60" y="430" font-family="Montserrat,sans-serif" font-size="22" fill="{PRETO}">programas de mentoria.</text>
    <text x="60" y="510" font-family="JetBrains Mono,monospace" font-size="16" letter-spacing="2" fill="{CARMESIM}">42 EVENTOS · 2026</text>
  </g>
  <!-- Footer -->
  <text x="120" y="1030" font-family="JetBrains Mono,monospace" font-size="18" letter-spacing="2" fill="{PRETO}" opacity="0.5">SANFRAN iLAB · CAP 03</text>
  <text x="1800" y="1030" text-anchor="end" font-family="JetBrains Mono,monospace" font-size="18" letter-spacing="2" fill="{PRETO}" opacity="0.5">07 / 24</text>
</svg>'''


# ════════════════════════════════════════════════
# CARTÃO DE VISITA · 900x500 (proporção 9x5cm)
# ════════════════════════════════════════════════
def card_front():
    """Frente do cartão — dark."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 500" width="900" height="500">
  <defs>{DOT_PATTERN}{GRAD_AMBAR_ORANGE}</defs>
  <rect width="900" height="500" fill="{PRETO}"/>
  <rect width="900" height="500" fill="url(#dots)"/>
  <rect x="0" y="0" width="900" height="6" fill="url(#g-bar)"/>
  <!-- Logo center-left -->
  <g transform="translate(60 180)">
    <text font-family="Poppins,sans-serif" font-weight="900" font-size="96" fill="{CREME}">SanFran</text>
    <text y="100" font-family="Poppins,sans-serif" font-weight="900" font-size="96" fill="url(#g-bar)" font-style="italic">iLab</text>
  </g>
  <!-- Mini Lex bottom right -->
  <g transform="translate(680 280)">
    <circle cx="100" cy="100" r="120" fill="{AMBAR}" opacity="0.08"/>
    <image href="assets/foxes/intelecto_idea.png" x="-20" y="-20" width="240" height="240" preserveAspectRatio="xMidYMid meet"/>
  </g>
  <!-- Tagline -->
  <text x="60" y="440" font-family="JetBrains Mono,monospace" font-size="14" font-weight="700" letter-spacing="3" fill="{AMBAR}">DIREITO · TECNOLOGIA · INOVAÇÃO</text>
</svg>'''


def card_back():
    """Verso do cartão — amber com contatos."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 500" width="900" height="500">
  <defs>
    {GRAD_AMBAR_ORANGE}
    <linearGradient id="bg-card" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{AMBAR}"/>
      <stop offset="1" stop-color="{LARANJA}"/>
    </linearGradient>
  </defs>
  <rect width="900" height="500" fill="url(#bg-card)"/>
  <!-- Name -->
  <text x="60" y="120" font-family="Poppins,sans-serif" font-weight="900" font-size="48" fill="{PRETO}">Pedro Galvão</text>
  <text x="60" y="160" font-family="JetBrains Mono,monospace" font-size="18" font-weight="700" letter-spacing="2" fill="{PRETO}" opacity="0.7">COORDENADOR · LEGALTECH</text>
  <!-- Divider -->
  <rect x="60" y="200" width="60" height="3" fill="{PRETO}"/>
  <!-- Contacts -->
  <g transform="translate(60 260)">
    <image href="assets/fluent3d/megaphone.png" x="0" y="0" width="32" height="32"/>
    <text x="48" y="22" font-family="Montserrat,sans-serif" font-size="20" fill="{PRETO}">+55 11 99999-0000</text>
  </g>
  <g transform="translate(60 320)">
    <image href="assets/fluent3d/laptop.png" x="0" y="0" width="32" height="32"/>
    <text x="48" y="22" font-family="Montserrat,sans-serif" font-size="20" fill="{PRETO}">pedro@sanfran-ilab.usp.br</text>
  </g>
  <g transform="translate(60 380)">
    <image href="assets/fluent3d/globe_with_meridians.png" x="0" y="0" width="32" height="32"/>
    <text x="48" y="22" font-family="Montserrat,sans-serif" font-size="20" fill="{PRETO}">sanfran-ilab.surge.sh</text>
  </g>
  <!-- Logo bottom right -->
  <g transform="translate(700 380)">
    <text font-family="Poppins,sans-serif" font-weight="900" font-size="36" fill="{PRETO}">iLab</text>
    <text y="22" font-family="JetBrains Mono,monospace" font-size="11" font-weight="700" fill="{PRETO}" opacity="0.6" letter-spacing="2">SANFRAN</text>
  </g>
</svg>'''


def story_vertical():
    """Story 9:16 (1080x1920) — vertical"""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
  <defs>{DOT_PATTERN}{GRAD_AMBAR_ORANGE}</defs>
  <rect width="1080" height="1920" fill="{PRETO}"/>
  <rect width="1080" height="1920" fill="url(#dots)"/>
  <rect x="0" y="0" width="1080" height="8" fill="url(#g-bar)"/>
  <!-- Top label -->
  <text x="80" y="160" font-family="JetBrains Mono,monospace" font-size="26" font-weight="700" letter-spacing="6" fill="{AMBAR}">SANFRAN iLAB · STORY</text>
  <!-- Center: large Fluent 3D + headline -->
  <image href="assets/fluent3d/light_bulb.png" x="340" y="380" width="400" height="400"/>
  <text x="540" y="900" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="84" fill="{CREME}">Ideia nova</text>
  <text x="540" y="990" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="84" fill="url(#g-bar)">acende aqui.</text>
  <!-- Subtitle -->
  <text x="540" y="1100" text-anchor="middle" font-family="Montserrat,sans-serif" font-size="32" fill="{CREME}" opacity="0.85">Inscrições abertas para o programa</text>
  <text x="540" y="1150" text-anchor="middle" font-family="Montserrat,sans-serif" font-size="32" fill="{CREME}" opacity="0.85">de mentoria iLab 2026.</text>
  <!-- CTA button -->
  <rect x="340" y="1290" width="400" height="100" rx="50" fill="url(#g-bar)"/>
  <text x="540" y="1352" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="32" fill="{PRETO}">INSCREVA-SE →</text>
  <!-- Lex bottom -->
  <g transform="translate(380 1480)">
    <circle cx="160" cy="160" r="200" fill="{AMBAR}" opacity="0.1"/>
    <image href="assets/foxes/intelecto_idea.png" x="0" y="0" width="320" height="320" preserveAspectRatio="xMidYMid meet"/>
  </g>
  <!-- Logo -->
  <text x="540" y="1880" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="36" fill="{AMBAR}">iLab</text>
</svg>'''


# ════════════════════════════════════════════════
# SAVE
# ════════════════════════════════════════════════
mockups = {
    "insta-announcement":   insta_announcement(),
    "insta-quote":          insta_quote(),
    "insta-event":          insta_event(),
    "slide-cover":          slide_cover(),
    "slide-content":        slide_content(),
    "card-front":           card_front(),
    "card-back":            card_back(),
    "story-vertical":       story_vertical(),
}

for name, content in mockups.items():
    (OUT / f"{name}.svg").write_text(content, encoding="utf-8")
    print(f"  {name}.svg  OK")

print(f"\n{len(mockups)} mockups gerados em {OUT}")
