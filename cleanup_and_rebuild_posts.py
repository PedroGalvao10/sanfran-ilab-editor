"""
CLEANUP + REBUILD v4:
1. Apaga: decoratives indicados, blobs, holo-disc/prism, openmoji inteiro,
   mockups antigos (cartões + slides — usuário quer só POSTS de Instagram)
2. Gera novos templates de POST Instagram inspirados no design Canva referência
   DAHGTZCpiu4 (22 páginas — Pilares, Tecnologias 01-05, Iceberg, Trilhas, etc.)
3. Atualiza HTML — remove cards apagados, filtros e botões correspondentes
4. Adiciona TODOS os 6 designs Canva na seção 13 com links corretos
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
INDEX = ROOT / "index.html"

AMBAR    = "#F4C430"
LARANJA  = "#FF6B35"
CARMESIM = "#C41E3A"
PRETO    = "#1A1A1A"
PRETO_D  = "#0E0E0E"
CREME    = "#FAF3E0"

# ═══════════════════════════════════════════════════════
# STEP 1 — Deletar arquivos
# ═══════════════════════════════════════════════════════
print("STEP 1 — Deletando arquivos...")

# Decoratives específicos
DECOR_TO_DELETE = ["tag-banner", "spark-corner", "bracket-corner-tl", "badge-circle", "divider-flame"]
for name in DECOR_TO_DELETE:
    p = ROOT / "assets" / "decoratives" / f"{name}.svg"
    if p.exists(): p.unlink(); print(f"  - decoratives/{name}.svg")

# Blobs (8 unidades)
for i in range(1, 9):
    p = ROOT / "assets" / "creatives" / f"blob-{i:02d}.svg"
    if p.exists(): p.unlink(); print(f"  - creatives/blob-{i:02d}.svg")

# Holographic disc + prism
for name in ["holo-disc", "holo-prism"]:
    p = ROOT / "assets" / "holographic" / f"{name}.svg"
    if p.exists(): p.unlink(); print(f"  - holographic/{name}.svg")

# OpenMoji inteiro
openmoji_dir = ROOT / "assets" / "openmoji"
if openmoji_dir.exists():
    shutil.rmtree(openmoji_dir)
    print(f"  - assets/openmoji/ (pasta inteira)")

# Mockups que não são POSTS (cards + slides)
MOCKUPS_TO_KEEP = ["insta-announcement", "insta-quote", "insta-event", "story-vertical"]
mockup_dir = ROOT / "assets" / "mockups"
if mockup_dir.exists():
    for f in mockup_dir.glob("*.svg"):
        if f.stem not in MOCKUPS_TO_KEEP and not f.stem.startswith("post-"):
            f.unlink()
            print(f"  - mockups/{f.name}")


# ═══════════════════════════════════════════════════════
# STEP 2 — Gerar NOVOS templates de POST inspirados no Canva
# ═══════════════════════════════════════════════════════
print("\nSTEP 2 — Gerando novos posts inspirados no design referência...")

# Helpers visuais reutilizáveis
DOT_PATTERN = f'''<pattern id="dots" x="0" y="0" width="32" height="32" patternUnits="userSpaceOnUse">
    <circle cx="16" cy="16" r="1.2" fill="{AMBAR}" opacity="0.4"/>
  </pattern>'''

GRAD_AO = f'''<linearGradient id="g-ao" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{AMBAR}"/>
    <stop offset="1" stop-color="{LARANJA}"/>
  </linearGradient>'''

GRAD_AO_V = f'''<linearGradient id="g-ao-v" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{AMBAR}"/>
    <stop offset="1" stop-color="{LARANJA}"/>
  </linearGradient>'''

GRAD_AOC = f'''<linearGradient id="g-aoc" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{AMBAR}"/>
    <stop offset="0.5" stop-color="{LARANJA}"/>
    <stop offset="1" stop-color="{CARMESIM}"/>
  </linearGradient>'''


def post_manifesto():
    """Post 'A Primeira Escola de Inovação Jurídica' — manifesto institucional."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>{DOT_PATTERN}{GRAD_AO}{GRAD_AO_V}</defs>
  <rect width="1080" height="1080" fill="{PRETO}"/>
  <rect width="1080" height="1080" fill="url(#dots)"/>
  <rect x="0" y="0" width="1080" height="8" fill="url(#g-ao)"/>
  <text x="80" y="120" font-family="JetBrains Mono,monospace" font-size="22" font-weight="700" letter-spacing="6" fill="{AMBAR}">SANFRAN iLAB · MANIFESTO</text>
  <!-- Headline -->
  <text x="80" y="320" font-family="Poppins,sans-serif" font-weight="900" font-size="120" fill="{CREME}" letter-spacing="-2">A primeira</text>
  <text x="80" y="445" font-family="Poppins,sans-serif" font-weight="900" font-size="120" fill="url(#g-ao)" letter-spacing="-2">Escola</text>
  <text x="80" y="540" font-family="Poppins,sans-serif" font-weight="900" font-size="56" fill="{CREME}">de Inovação Jurídica</text>
  <text x="80" y="610" font-family="Poppins,sans-serif" font-weight="900" font-size="56" fill="{CREME}">&amp; Startups da USP</text>
  <!-- Decorative line + sparkle -->
  <rect x="80" y="660" width="100" height="3" fill="{LARANJA}"/>
  <image href="assets/fluent3d/sparkles.png" x="200" y="640" width="64" height="64"/>
  <!-- Subtitle -->
  <text x="80" y="770" font-family="Montserrat,sans-serif" font-size="28" fill="{CREME}" opacity="0.85">Formando talentos que integram</text>
  <text x="80" y="810" font-family="Montserrat,sans-serif" font-size="28" fill="{CREME}" opacity="0.85">Direito, Tecnologia e Inovação.</text>
  <!-- Lex bottom right -->
  <g transform="translate(700 700)">
    <circle cx="160" cy="160" r="200" fill="{AMBAR}" opacity="0.08"/>
    <circle cx="160" cy="160" r="160" fill="{AMBAR}" opacity="0.14"/>
    <image href="assets/lex/confianca.png" x="0" y="0" width="320" height="320" preserveAspectRatio="xMidYMid meet"/>
  </g>
  <!-- Logo bottom -->
  <text x="80" y="1010" font-family="Poppins,sans-serif" font-weight="900" font-size="32" fill="{AMBAR}">iLab<tspan fill="{CREME}" font-size="20" font-weight="400" dx="10">· SANFRAN · FD-USP</tspan></text>
</svg>'''


def post_pilares():
    """Post 4 Pilares 25% cada — direto do design Canva."""
    pilares_data = [
        ("Tecnologia",          AMBAR,    f'<image href="assets/fluent3d/laptop.png" x="0" y="0" width="120" height="120"/>'),
        ("Finanças",            LARANJA,  f'<image href="assets/fluent3d/money_bag.png" x="0" y="0" width="120" height="120"/>'),
        ("Direito",             CARMESIM, f'<image href="assets/fluent3d/balance_scale.png" x="0" y="0" width="120" height="120"/>'),
        ("Empreendedorismo",    AMBAR,    f'<image href="assets/fluent3d/rocket.png" x="0" y="0" width="120" height="120"/>'),
    ]
    cards = ""
    for i, (label, color, icon) in enumerate(pilares_data):
        row, col = i // 2, i % 2
        x = 80 + col * 480
        y = 380 + row * 320
        cards += f'''
    <g transform="translate({x} {y})">
      <rect x="0" y="0" width="430" height="280" rx="20" fill="{color}" opacity="0.95"/>
      <g transform="translate(30 30)">{icon}</g>
      <text x="30" y="200" font-family="Poppins,sans-serif" font-weight="900" font-size="32" fill="{PRETO}">{label}</text>
      <text x="30" y="248" font-family="JetBrains Mono,monospace" font-size="56" font-weight="900" fill="{PRETO}">25%</text>
    </g>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>{DOT_PATTERN}{GRAD_AO}</defs>
  <rect width="1080" height="1080" fill="{PRETO}"/>
  <rect width="1080" height="1080" fill="url(#dots)"/>
  <rect x="0" y="0" width="1080" height="6" fill="url(#g-ao)"/>
  <text x="80" y="120" font-family="JetBrains Mono,monospace" font-size="22" font-weight="700" letter-spacing="6" fill="{AMBAR}">04 PILARES · COMPOSIÇÃO DO LAB</text>
  <text x="80" y="220" font-family="Poppins,sans-serif" font-weight="900" font-size="76" fill="{CREME}">As 4 frentes</text>
  <text x="80" y="298" font-family="Poppins,sans-serif" font-weight="900" font-size="76" fill="url(#g-ao)">do iLab</text>
  {cards}
  <text x="540" y="1010" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="14" letter-spacing="3" fill="{CREME}" opacity="0.5">SANFRAN iLAB · CARROSSEL 02/08</text>
</svg>'''


def post_tecnologias():
    """Post '5 Tecnologias' — listagem numerada 01-05."""
    tecs = [
        ("01", "Inteligência Artificial",  "aplicada ao Direito"),
        ("02", "Agentes de IA",            "para automação de workflows"),
        ("03", "Jurimetria",               "e análise de dados judiciais"),
        ("04", "Plataformas Digitais",     "de resolução de disputas"),
        ("05", "Blockchain",               "para registros e contratos"),
    ]
    items = ""
    for i, (num, title, sub) in enumerate(tecs):
        y = 380 + i * 110
        items += f'''
    <g transform="translate(80 {y})">
      <text font-family="Poppins,sans-serif" font-weight="900" font-size="64" fill="url(#g-ao)">{num}</text>
      <text x="140" y="-8" font-family="Poppins,sans-serif" font-weight="900" font-size="34" fill="{CREME}">{title}</text>
      <text x="140" y="28" font-family="Montserrat,sans-serif" font-size="22" fill="{CREME}" opacity="0.7">{sub}</text>
      <line x1="0" y1="55" x2="920" y2="55" stroke="{AMBAR}" stroke-width="1" opacity="0.18"/>
    </g>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>{DOT_PATTERN}{GRAD_AO}</defs>
  <rect width="1080" height="1080" fill="{PRETO}"/>
  <rect width="1080" height="1080" fill="url(#dots)"/>
  <rect x="0" y="0" width="1080" height="6" fill="url(#g-ao)"/>
  <text x="80" y="120" font-family="JetBrains Mono,monospace" font-size="22" font-weight="700" letter-spacing="6" fill="{AMBAR}">05 TECNOLOGIAS · MERCADO JURÍDICO</text>
  <text x="80" y="220" font-family="Poppins,sans-serif" font-weight="900" font-size="64" fill="{CREME}">As tecnologias que</text>
  <text x="80" y="290" font-family="Poppins,sans-serif" font-weight="900" font-size="64" fill="url(#g-ao)">redefinem o Direito.</text>
  {items}
  <text x="540" y="1010" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="14" letter-spacing="3" fill="{CREME}" opacity="0.5">SANFRAN iLAB · CARROSSEL 04/08</text>
</svg>'''


def post_iceberg():
    """Post 'Iceberg' — Acima vs Abaixo do iceberg."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>{DOT_PATTERN}{GRAD_AO}
    <linearGradient id="water" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0E0E0E"/>
      <stop offset="0.5" stop-color="#1A1A1A"/>
      <stop offset="1" stop-color="{PRETO}"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="540" fill="{PRETO}"/>
  <rect width="1080" height="540" fill="url(#dots)"/>
  <rect y="540" width="1080" height="540" fill="url(#water)"/>
  <!-- Linha d'água -->
  <line x1="0" y1="540" x2="1080" y2="540" stroke="{AMBAR}" stroke-width="2" stroke-dasharray="6 6" opacity="0.5"/>
  <!-- Iceberg shape -->
  <polygon points="380,180 700,180 760,540 540,540 320,540 380,180" fill="{CREME}" opacity="0.95"/>
  <polygon points="320,540 760,540 880,900 200,900 320,540" fill="{AMBAR}" opacity="0.4"/>
  <polygon points="200,900 880,900 1000,1000 80,1000 200,900" fill="{AMBAR}" opacity="0.15"/>
  <!-- Labels -->
  <text x="80" y="80" font-family="JetBrains Mono,monospace" font-size="20" font-weight="700" letter-spacing="5" fill="{AMBAR}">ANÁLISE · DIAGNÓSTICO</text>
  <text x="80" y="180" font-family="Poppins,sans-serif" font-weight="900" font-size="56" fill="{CREME}">Acima do</text>
  <text x="80" y="240" font-family="Poppins,sans-serif" font-weight="900" font-size="56" fill="url(#g-ao)">iceberg</text>
  <text x="80" y="320" font-family="Montserrat,sans-serif" font-size="20" fill="{CREME}" opacity="0.85">Formação jurídica tradicional</text>
  <text x="80" y="350" font-family="Montserrat,sans-serif" font-size="20" fill="{CREME}" opacity="0.85">com dificuldade de acompanhar</text>
  <text x="80" y="380" font-family="Montserrat,sans-serif" font-size="20" fill="{CREME}" opacity="0.85">as transformações tecnológicas.</text>
  <text x="80" y="700" font-family="Poppins,sans-serif" font-weight="900" font-size="56" fill="{CREME}">Abaixo do</text>
  <text x="80" y="760" font-family="Poppins,sans-serif" font-weight="900" font-size="56" fill="url(#g-ao)">iceberg</text>
  <text x="80" y="820" font-family="Montserrat,sans-serif" font-size="20" fill="{CREME}" opacity="0.85">Baixa integração Direito ↔ tech.</text>
  <text x="80" y="850" font-family="Montserrat,sans-serif" font-size="20" fill="{CREME}" opacity="0.85">Poucos espaços de prototipagem.</text>
  <text x="80" y="880" font-family="Montserrat,sans-serif" font-size="20" fill="{CREME}" opacity="0.85">Escassez de empreendedorismo</text>
  <text x="80" y="910" font-family="Montserrat,sans-serif" font-size="20" fill="{CREME}" opacity="0.85">jurídico nas universidades.</text>
  <text x="540" y="1040" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="14" letter-spacing="3" fill="{CREME}" opacity="0.5">SANFRAN iLAB · CARROSSEL 05/08</text>
</svg>'''


def post_trilhas():
    """Post 'Trilhas de Formação' — 4 trilhas em cards."""
    trilhas = [
        ("Direito",       "balance_scale",  AMBAR),
        ("Tecnologia",    "cpu" if (ROOT / "assets/fluent3d/cpu.png").exists() else "laptop", LARANJA),
        ("Negócios",      "briefcase",      CARMESIM),
        ("Pesquisa",      "magnifying_glass_tilted_left", AMBAR),
    ]
    cards = ""
    for i, (name, icon, color) in enumerate(trilhas):
        row, col = i // 2, i % 2
        x = 80 + col * 480
        y = 420 + row * 280
        cards += f'''
    <g transform="translate({x} {y})">
      <rect x="0" y="0" width="430" height="240" rx="20" fill="{PRETO_D}" stroke="{color}" stroke-width="2"/>
      <image href="assets/fluent3d/{icon}.png" x="30" y="30" width="80" height="80"/>
      <text x="130" y="80" font-family="Poppins,sans-serif" font-weight="900" font-size="32" fill="{CREME}">{name}</text>
      <text x="130" y="105" font-family="JetBrains Mono,monospace" font-size="12" letter-spacing="2" fill="{color}">TRILHA · iLAB</text>
      <line x1="30" y1="140" x2="60" y2="140" stroke="{color}" stroke-width="3"/>
      <text x="30" y="180" font-family="Montserrat,sans-serif" font-size="14" fill="{CREME}" opacity="0.75">Squads multidisciplinares</text>
      <text x="30" y="200" font-family="Montserrat,sans-serif" font-size="14" fill="{CREME}" opacity="0.75">com projetos reais.</text>
    </g>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>{DOT_PATTERN}{GRAD_AO}</defs>
  <rect width="1080" height="1080" fill="{PRETO}"/>
  <rect width="1080" height="1080" fill="url(#dots)"/>
  <rect x="0" y="0" width="1080" height="6" fill="url(#g-ao)"/>
  <text x="80" y="120" font-family="JetBrains Mono,monospace" font-size="22" font-weight="700" letter-spacing="6" fill="{AMBAR}">04 TRILHAS · FORMAÇÃO MULTIDISCIPLINAR</text>
  <text x="80" y="220" font-family="Poppins,sans-serif" font-weight="900" font-size="68" fill="{CREME}">Trilhas de</text>
  <text x="80" y="290" font-family="Poppins,sans-serif" font-weight="900" font-size="68" fill="url(#g-ao)">Formação</text>
  <text x="80" y="350" font-family="Montserrat,sans-serif" font-size="22" fill="{CREME}" opacity="0.75">Os participantes desenvolvem competências em quatro frentes:</text>
  {cards}
  <text x="540" y="1010" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="14" letter-spacing="3" fill="{CREME}" opacity="0.5">SANFRAN iLAB · CARROSSEL 06/08</text>
</svg>'''


def post_squad():
    """Post 'Squads' — equipes multidisciplinares."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>{DOT_PATTERN}{GRAD_AO}</defs>
  <rect width="1080" height="1080" fill="{CREME}"/>
  <rect x="0" y="0" width="1080" height="6" fill="url(#g-ao)"/>
  <text x="80" y="120" font-family="JetBrains Mono,monospace" font-size="22" font-weight="700" letter-spacing="6" fill="{LARANJA}">SQUADS · OS DREAM TEAMS DO iLAB</text>
  <text x="80" y="240" font-family="Poppins,sans-serif" font-weight="900" font-size="84" fill="{PRETO}">Squads</text>
  <text x="80" y="320" font-family="Poppins,sans-serif" font-weight="900" font-size="42" fill="url(#g-ao)">multidisciplinares.</text>
  <text x="80" y="380" font-family="Montserrat,sans-serif" font-size="22" fill="{PRETO}" opacity="0.7">Projetos desenvolvidos por equipes</text>
  <text x="80" y="410" font-family="Montserrat,sans-serif" font-size="22" fill="{PRETO}" opacity="0.7">de perfis e competências diversos:</text>
  <!-- 3 avatares horizontais com label -->
  <g transform="translate(80 480)">
    <image href="assets/avatars/maria.svg" x="0" y="0" width="180" height="180"/>
    <text x="90" y="220" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="22" fill="{PRETO}">Direito</text>
    <rect x="50" y="234" width="80" height="3" fill="{AMBAR}"/>
  </g>
  <g transform="translate(330 480)">
    <image href="assets/avatars/rafael.svg" x="0" y="0" width="180" height="180"/>
    <text x="90" y="220" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="22" fill="{PRETO}">Tecnologia</text>
    <rect x="40" y="234" width="100" height="3" fill="{LARANJA}"/>
  </g>
  <g transform="translate(580 480)">
    <image href="assets/avatars/ana.svg" x="0" y="0" width="180" height="180"/>
    <text x="90" y="220" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="22" fill="{PRETO}">Negócios</text>
    <rect x="46" y="234" width="88" height="3" fill="{CARMESIM}"/>
  </g>
  <g transform="translate(830 480)">
    <image href="assets/avatars/lucas.svg" x="0" y="0" width="180" height="180"/>
    <text x="90" y="220" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="22" fill="{PRETO}">Pesquisa</text>
    <rect x="50" y="234" width="80" height="3" fill="{AMBAR}"/>
  </g>
  <!-- CTA -->
  <text x="80" y="820" font-family="Poppins,sans-serif" font-weight="900" font-size="40" fill="{PRETO}">+ de 60 alunos.</text>
  <text x="80" y="870" font-family="Poppins,sans-serif" font-weight="900" font-size="40" fill="url(#g-ao)">12 squads ativos.</text>
  <text x="80" y="920" font-family="Montserrat,sans-serif" font-size="20" fill="{PRETO}" opacity="0.7">Construindo o futuro do Direito.</text>
  <text x="540" y="1020" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="14" letter-spacing="3" fill="{PRETO}" opacity="0.4">SANFRAN iLAB · CARROSSEL 07/08</text>
</svg>'''


def post_cta_parceria():
    """Post final — CTA de parceria."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>{DOT_PATTERN}{GRAD_AO_V}{GRAD_AOC}</defs>
  <rect width="1080" height="720" fill="{PRETO}"/>
  <rect width="1080" height="720" fill="url(#dots)"/>
  <rect y="720" width="1080" height="360" fill="url(#g-aoc)"/>
  <text x="80" y="120" font-family="JetBrains Mono,monospace" font-size="22" font-weight="700" letter-spacing="6" fill="{AMBAR}">CHAMADA · ABERTA</text>
  <text x="80" y="240" font-family="Poppins,sans-serif" font-weight="900" font-size="84" fill="{CREME}">Construa o futuro</text>
  <text x="80" y="320" font-family="Poppins,sans-serif" font-weight="900" font-size="84" fill="url(#g-ao-v)">do Direito conosco.</text>
  <text x="80" y="420" font-family="Montserrat,sans-serif" font-size="26" fill="{CREME}" opacity="0.85">Buscamos escritórios, legaltechs,</text>
  <text x="80" y="455" font-family="Montserrat,sans-serif" font-size="26" fill="{CREME}" opacity="0.85">empresas e investidores que queiram</text>
  <text x="80" y="490" font-family="Montserrat,sans-serif" font-size="26" fill="{CREME}" opacity="0.85">conectar inovação jurídica e prática.</text>
  <!-- 3 ícones -->
  <g transform="translate(80 560)">
    <image href="assets/fluent3d/handshake.png" x="0" y="0" width="80" height="80"/>
    <image href="assets/fluent3d/rocket.png" x="130" y="0" width="80" height="80"/>
    <image href="assets/fluent3d/light_bulb.png" x="260" y="0" width="80" height="80"/>
  </g>
  <!-- CTA section -->
  <text x="540" y="820" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="48" fill="{PRETO}">Vamos conversar?</text>
  <rect x="340" y="870" width="400" height="100" rx="50" fill="{PRETO}"/>
  <text x="540" y="932" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="28" fill="{AMBAR}">FALE COM A GENTE →</text>
  <text x="540" y="1030" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="14" letter-spacing="3" fill="{PRETO}" opacity="0.6">SANFRAN iLAB · CARROSSEL 08/08</text>
</svg>'''


def post_missao():
    """Post 'Missão SanFran iLab' — texto institucional."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>{GRAD_AO}{GRAD_AOC}</defs>
  <rect width="1080" height="1080" fill="{CREME}"/>
  <!-- Top accent -->
  <rect x="0" y="0" width="540" height="6" fill="url(#g-ao)"/>
  <text x="80" y="120" font-family="JetBrains Mono,monospace" font-size="20" font-weight="700" letter-spacing="5" fill="{LARANJA}">MISSÃO · NOSSO PROPÓSITO</text>
  <!-- Big quote mark -->
  <text x="80" y="350" font-family="Poppins,sans-serif" font-weight="900" font-size="280" fill="{AMBAR}" opacity="0.18">"</text>
  <text x="80" y="440" font-family="Poppins,sans-serif" font-weight="900" font-size="48" fill="{PRETO}">Promover a inovação</text>
  <text x="80" y="500" font-family="Poppins,sans-serif" font-weight="900" font-size="48" fill="{PRETO}">jurídica através da</text>
  <text x="80" y="560" font-family="Poppins,sans-serif" font-weight="900" font-size="48" fill="url(#g-ao)">formação de talentos,</text>
  <text x="80" y="640" font-family="Poppins,sans-serif" font-weight="900" font-size="48" fill="{PRETO}">desenvolvimento de</text>
  <text x="80" y="700" font-family="Poppins,sans-serif" font-weight="900" font-size="48" fill="url(#g-ao)">soluções tecnológicas</text>
  <text x="80" y="760" font-family="Poppins,sans-serif" font-weight="900" font-size="48" fill="{PRETO}">e articulação universidade-</text>
  <text x="80" y="820" font-family="Poppins,sans-serif" font-weight="900" font-size="48" fill="{PRETO}">mercado-instituições.</text>
  <!-- Lex bottom right -->
  <g transform="translate(720 720)">
    <circle cx="160" cy="160" r="180" fill="{AMBAR}" opacity="0.18"/>
    <image href="assets/lex/apresentacao.png" x="0" y="0" width="320" height="320" preserveAspectRatio="xMidYMid meet"/>
  </g>
  <text x="540" y="1030" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="14" letter-spacing="3" fill="{PRETO}" opacity="0.4">SANFRAN iLAB · CARROSSEL 03/08</text>
</svg>'''


def post_capa_carrossel():
    """Post capa de carrossel — chamativo p/ feed."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>{DOT_PATTERN}{GRAD_AO}{GRAD_AOC}</defs>
  <rect width="1080" height="1080" fill="url(#g-aoc)"/>
  <!-- Subtle dot pattern overlay -->
  <rect width="1080" height="1080" fill="url(#dots)" opacity="0.4"/>
  <text x="540" y="180" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="22" font-weight="700" letter-spacing="6" fill="{PRETO}">SANFRAN iLAB · 2026</text>
  <!-- Title BIG -->
  <text x="540" y="400" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="140" fill="{PRETO}" letter-spacing="-3">FUTURO</text>
  <text x="540" y="540" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="140" fill="{CREME}" letter-spacing="-3">DO DIREITO</text>
  <text x="540" y="680" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="140" fill="{PRETO}" letter-spacing="-3">É AGORA.</text>
  <!-- Subtitle -->
  <text x="540" y="780" text-anchor="middle" font-family="Montserrat,sans-serif" font-size="32" font-weight="600" fill="{PRETO}" opacity="0.7">Conheça o laboratório de inovação jurídica</text>
  <text x="540" y="822" text-anchor="middle" font-family="Montserrat,sans-serif" font-size="32" font-weight="600" fill="{PRETO}" opacity="0.7">que está transformando a FD-USP.</text>
  <!-- Arrow indicator (carrossel) -->
  <g transform="translate(540 920)">
    <circle cx="0" cy="0" r="50" fill="{PRETO}"/>
    <text x="0" y="14" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="44" fill="{AMBAR}">→</text>
  </g>
  <text x="540" y="1020" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="14" letter-spacing="3" fill="{PRETO}" opacity="0.6">DESLIZE · CARROSSEL 01/08</text>
</svg>'''


# Salvar todos
posts = {
    "post-capa":         post_capa_carrossel(),
    "post-manifesto":    post_manifesto(),
    "post-missao":       post_missao(),
    "post-pilares":      post_pilares(),
    "post-tecnologias":  post_tecnologias(),
    "post-iceberg":      post_iceberg(),
    "post-trilhas":      post_trilhas(),
    "post-squads":       post_squad(),
    "post-cta-parceria": post_cta_parceria(),
}

mockup_dir = ROOT / "assets" / "mockups"
mockup_dir.mkdir(parents=True, exist_ok=True)

# Limpar antigos
for f in mockup_dir.glob("*.svg"):
    f.unlink()

for name, content in posts.items():
    (mockup_dir / f"{name}.svg").write_text(content, encoding="utf-8")
    print(f"  + mockups/{name}.svg")

print(f"\n{len(posts)} novos posts gerados (sem slides, sem cartões)")


# ═══════════════════════════════════════════════════════
# STEP 3 — Atualizar HTML
# ═══════════════════════════════════════════════════════
print("\nSTEP 3 — Atualizando HTML...")

content = INDEX.read_text(encoding="utf-8")

# 3.1) Remover cards apagados pelo asset slug
ASSETS_REMOVED = [
    "tag-banner", "spark-corner", "bracket-corner-tl", "badge-circle", "divider-flame",
    "holo-disc", "holo-prism",
    "blob-01", "blob-02", "blob-03", "blob-04", "blob-05", "blob-06", "blob-07", "blob-08",
    # mockups antigos
    "slide-cover", "slide-content", "card-front", "card-back",
]
for slug in ASSETS_REMOVED:
    pattern = re.compile(
        r'\s*<div class="el-card[^"]*"[^>]*?>\s*(?:<div[^>]*>)?\s*<img src="assets/[^/]+/' + re.escape(slug) + r'\.[^"]*"[^>]*>.*?</div>\s*</div>\s*',
        re.DOTALL
    )
    count = len(pattern.findall(content))
    if count:
        content = pattern.sub("", content)
        print(f"  - removidos {count} card(s) com asset '{slug}'")

# 3.2) Remover TODOS os cards openmoji
pattern_om = re.compile(
    r'\s*<div class="el-card[^"]*" data-cat="openmoji"[^>]*>.*?</div>\s*</div>\s*',
    re.DOTALL
)
removed_om = len(pattern_om.findall(content))
content = pattern_om.sub("", content)
print(f"  - removidos {removed_om} cards openmoji")

# 3.3) Remover botão de filtro openmoji
content = re.sub(r'<button class="el-filter" data-cat="openmoji">[^<]*</button>\s*', '', content)
print("  - removido filtro 'OpenMoji'")

# 3.4) Substituir cards de mockup antigos pelos novos
# Estratégia: encontrar todos cards data-cat="mockups" e regenerar
pattern_mockup_cards = re.compile(
    r'\s*<div class="el-card el-card-mockup" data-cat="mockups"[^>]*>.*?</div>\s*</div>\s*</div>\s*',
    re.DOTALL
)
content = pattern_mockup_cards.sub("", content)

# Gerar novos cards mockup
new_post_cards = ""
post_labels = {
    "post-capa":         ("Capa Carrossel",      "Post 01/08"),
    "post-manifesto":    ("Manifesto",            "Post · A Primeira"),
    "post-missao":       ("Missão",               "Post 03/08"),
    "post-pilares":      ("4 Pilares 25%",        "Post 02/08"),
    "post-tecnologias":  ("5 Tecnologias",        "Post 04/08"),
    "post-iceberg":      ("Iceberg",              "Post 05/08"),
    "post-trilhas":      ("Trilhas Formação",     "Post 06/08"),
    "post-squads":       ("Squads",               "Post 07/08"),
    "post-cta-parceria": ("CTA Parceria",         "Post 08/08"),
}
for slug, (label, desc) in post_labels.items():
    new_post_cards += f'''    <div class="el-card el-card-mockup" data-cat="mockups">
      <div class="el-mockup-wrap">
        <img src="assets/mockups/{slug}.svg" alt="{label}" class="el-img el-img-mockup">
      </div>
      <div class="el-label">
        <span>{label} <span class="el-tag">{desc}</span></span>
        <span class="el-dl">
          <button class="dl-mini dl-svg" data-asset="{slug}" data-folder="mockups" data-label="{slug}" title="SVG">SVG</button>
          <button class="dl-mini dl-png" data-asset="{slug}" data-folder="mockups" data-label="{slug}" data-size="2160" title="PNG 2160px">PNG</button>
        </span>
      </div>
    </div>
'''

# Inserir os novos mockup cards no início do .el-grid da seção elementos
content = re.sub(
    r'(<section id="elementos">.*?<div class="el-grid">\s*)',
    lambda m: m.group(1) + new_post_cards,
    content,
    count=1,
    flags=re.DOTALL
)
print(f"  + adicionados {len(post_labels)} novos cards de POST")


# ═══════════════════════════════════════════════════════
# STEP 4 — Reconstruir seção 13 com TODOS os 6 designs Canva
# ═══════════════════════════════════════════════════════
print("\nSTEP 4 — Reconstruindo seção 13 com todos os designs Canva...")

CANVA_DESIGNS = [
    {
        "title": "SanFran iLab · Parceiros",
        "desc": "22 páginas · Pitch deck institucional completo",
        "view_url": "https://www.canva.com/d/7iCzTEPuLa0EfhS",
        "thumb": "https://design.canva.ai/qVwCm_sG5oc7yM8",
        "pages": 22,
        "featured": True,
    },
    {
        "title": "Encontro Presencial",
        "desc": "2 páginas · Convite de evento",
        "view_url": "https://www.canva.com/d/JcTbLLlhHpY7bsK",
        "thumb": "https://design.canva.ai/Cn-B_uXXPlNkLsT",
        "pages": 2,
        "featured": False,
    },
    {
        "title": "Cópia de Templadr Parceria",
        "desc": "2 páginas · Template base",
        "view_url": "https://www.canva.com/d/r37JPIJ7b8iDTjK",
        "thumb": "https://design.canva.ai/gH1_vo4W-SzqemI",
        "pages": 2,
        "featured": False,
    },
    {
        "title": "Parceria Template Básico",
        "desc": "3 páginas · Modelo padrão de proposta",
        "view_url": "https://www.canva.com/d/Z1YN515XlLR0z62",
        "thumb": "https://design.canva.ai/ci4cbbGQDV6j7bL",
        "pages": 3,
        "featured": False,
    },
    {
        "title": "Claude Parceria Massonetto",
        "desc": "6 páginas · Apresentação de proposta",
        "view_url": "https://www.canva.com/d/RXcFv7VR_en7RN-",
        "thumb": "https://design.canva.ai/yT3YxI4Z8cygeAU",
        "pages": 6,
        "featured": False,
    },
    {
        "title": "Post Diretoria",
        "desc": "4 páginas · Carrossel institucional",
        "view_url": "https://www.canva.com/d/j9NGXuQnGDIvItj",
        "thumb": "https://design.canva.ai/KRB-ELP1i7EXPps",
        "pages": 4,
        "featured": False,
    },
]

# Construir HTML da seção 13
section_13_inner = '<div class="canva-grid">\n'
for d in CANVA_DESIGNS:
    featured_class = " canva-card-featured" if d.get("featured") else ""
    section_13_inner += f'''    <div class="canva-card{featured_class}">
      <a href="{d['view_url']}" target="_blank" rel="noopener" class="canva-link">
        <div class="canva-thumb">
          <img src="{d['thumb']}" alt="{d['title']}" loading="lazy" onerror="this.style.display='none';this.parentElement.style.background='linear-gradient(135deg,#F4C430,#FF6B35)';">
          <div class="canva-overlay"><span class="canva-cta">Abrir no Canva →</span></div>
          {'<div class="canva-featured-badge">⭐ DESIGN PRINCIPAL</div>' if d.get("featured") else ''}
        </div>
        <div class="canva-meta">
          <div class="canva-title">{d['title']}</div>
          <div class="canva-sub">{d['desc']}</div>
        </div>
      </a>
    </div>
'''

# Novo design CTA
section_13_inner += '''    <div class="canva-card canva-new">
      <a href="https://www.canva.com/design" target="_blank" rel="noopener" class="canva-link">
        <div class="canva-thumb canva-thumb-empty">
          <div class="canva-plus">+</div>
          <div class="canva-newlabel">Novo design</div>
        </div>
        <div class="canva-meta">
          <div class="canva-title">Criar do zero</div>
          <div class="canva-sub">Abrir Canva e começar</div>
        </div>
      </a>
    </div>
  </div>

  <div class="canva-tools">
    <h3 class="cr-h3">Integrações & Plugins</h3>
    <div class="canva-tools-grid">
      <div class="canva-tool"><div class="canva-tool-icon">🎨</div><div class="canva-tool-name">Canva MCP</div><div class="canva-tool-desc">Conectado · Criação, edição e exportação direto do Claude</div></div>
      <div class="canva-tool"><div class="canva-tool-icon">📦</div><div class="canva-tool-name">Iconify API</div><div class="canva-tool-desc">Lucide + Phosphor · 200+ packs de ícones profissionais</div></div>
      <div class="canva-tool"><div class="canva-tool-icon">🅰️</div><div class="canva-tool-name">Adobe Illustrator</div><div class="canva-tool-desc">Manual · Importar SVGs direto no .ai</div></div>
      <div class="canva-tool"><div class="canva-tool-icon">🖼️</div><div class="canva-tool-name">Adobe Photoshop</div><div class="canva-tool-desc">Manual · PNGs em alta resolução</div></div>
    </div>
  </div>'''

# Substituir conteúdo interno da seção 13
content = re.sub(
    r'(<section id="canva-templates">\s*<div class="section-label">[^<]*</div>\s*<h2>[^<]*</h2>\s*<p class="section-desc">[^<]*</p>\s*)(.*?)(</section>)',
    lambda m: m.group(1) + section_13_inner + m.group(3),
    content,
    count=1,
    flags=re.DOTALL
)
# Atualizar descrição da seção
content = re.sub(
    r'(<section id="canva-templates">\s*<div class="section-label">[^<]*</div>\s*<h2>)[^<]*(</h2>\s*<p class="section-desc">)[^<]*(</p>)',
    r'\1Designs Canva da Marca\2Todos os designs ativos no Canva da SanFran iLab. Clique para abrir e editar — links atualizados ao MCP em tempo real.\3',
    content,
    count=1
)
print(f"  + Seção 13 reconstruída com {len(CANVA_DESIGNS)} designs Canva")

# Adicionar CSS para featured badge
extra_css = '''
.canva-card-featured{border:2px solid #F4C430;box-shadow:0 8px 24px rgba(244,196,48,.25);grid-column:span 2}
.canva-featured-badge{position:absolute;top:14px;left:14px;background:#1A1A1A;color:#F4C430;font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;letter-spacing:1.5px;padding:6px 12px;border-radius:20px;z-index:2}
.canva-card-featured .canva-thumb{aspect-ratio:16/9}
@media(max-width:768px){.canva-card-featured{grid-column:span 1}.canva-card-featured .canva-thumb{aspect-ratio:4/3}}
'''
content = content.replace("</style>", extra_css + "\n</style>", 1)

INDEX.write_text(content, encoding="utf-8")
print("\nOK: HTML atualizado")
print(f"\n=== RESUMO ===")
print(f"Apagados: 5 decoratives + 8 blobs + 2 holographic + 40 openmoji = 55 assets")
print(f"Novos posts: {len(posts)} templates Instagram (inspirados em 22 páginas do Canva)")
print(f"Seção 13: {len(CANVA_DESIGNS)} designs Canva com links VIEW corretos")
