"""
Gera 4 templates de evento editáveis (SVG) baseados no modelo "iLab Conecta".
Saída: assets/templates/*.svg
Cada template tem placeholders claros e estrutura limpa para edição em Canva/Illustrator/Figma.
"""
from pathlib import Path

OUT = Path(__file__).parent / "assets" / "templates"
OUT.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────
# Paleta SanFran iLab
# ─────────────────────────────────────────
BG = "#1A1A1A"
BG_DEEP = "#0F0F0F"
ORANGE = "#FF6B35"
ORANGE_DEEP = "#E5552A"
YELLOW = "#F4C430"
WHITE = "#FAFAFA"
GRAY = "#888"

W, H = 1080, 1350  # 4:5 — formato post/flyer Instagram

# ─────────────────────────────────────────
# Componentes reutilizáveis (SVG defs)
# ─────────────────────────────────────────
def defs():
    return f'''
<defs>
  <radialGradient id="bg-radial" cx="50%" cy="100%" r="80%">
    <stop offset="0%" stop-color="#2a1a0a" stop-opacity="0.5"/>
    <stop offset="100%" stop-color="{BG_DEEP}" stop-opacity="1"/>
  </radialGradient>
  <linearGradient id="orange-grad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{YELLOW}"/>
    <stop offset="100%" stop-color="{ORANGE}"/>
  </linearGradient>
  <linearGradient id="photo-grad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#3a3a3a"/>
    <stop offset="100%" stop-color="#1a1a1a"/>
  </linearGradient>
  <pattern id="dots" x="0" y="0" width="36" height="36" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1" fill="{ORANGE}" opacity="0.15"/>
  </pattern>
  <!-- Globe wireframe corners (decorativo) -->
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


def background():
    """Fundo dark + globos decorativos nos cantos."""
    return f'''
<rect width="{W}" height="{H}" fill="{BG_DEEP}"/>
<rect width="{W}" height="{H}" fill="url(#bg-radial)"/>
<rect width="{W}" height="{H}" fill="url(#dots)"/>
<!-- Globe top right -->
<use href="#globe-wire" x="{W-280}" y="-80" width="400" height="400"/>
<!-- Globe bottom left -->
<use href="#globe-wire" x="-180" y="{H-220}" width="400" height="400"/>'''


def title_block(line1_white: str, line2_orange: str, tagline_lines: list[str]):
    """Título grande estilo iLab Conecta + tagline à direita."""
    tagline_svg = ""
    for i, line in enumerate(tagline_lines):
        # Primeira palavra de cada linha em laranja se vier marcada com #
        if line.startswith("#"):
            txt = line[1:]
            color = ORANGE
        else:
            txt = line
            color = WHITE
        tagline_svg += f'<text x="{W-80}" y="{160 + i*32}" font-family="Poppins, sans-serif" font-weight="700" font-size="22" fill="{color}" text-anchor="end" letter-spacing="1.5">{txt}</text>\n  '
    return f'''
<!-- Título -->
<text x="80" y="220" font-family="Poppins, sans-serif" font-weight="900" font-size="140" fill="{WHITE}" letter-spacing="-3">{line1_white}</text>
<text x="80" y="370" font-family="Poppins, sans-serif" font-weight="900" font-size="140" fill="{ORANGE}" letter-spacing="-3">{line2_orange}</text>
<!-- Tagline à direita -->
{tagline_svg}'''


def meta_block(date_text: str, time_text: str, location_text: str, y_start: int = 480):
    """Bloco de data + local com ícones."""
    return f'''
<!-- Calendário -->
<g transform="translate(80,{y_start})">
  <rect x="0" y="6" width="56" height="56" rx="8" fill="none" stroke="{ORANGE}" stroke-width="3"/>
  <line x1="0" y1="22" x2="56" y2="22" stroke="{ORANGE}" stroke-width="3"/>
  <rect x="14" y="2" width="6" height="12" rx="2" fill="{ORANGE}"/>
  <rect x="36" y="2" width="6" height="12" rx="2" fill="{ORANGE}"/>
  <text x="80" y="38" font-family="Poppins, sans-serif" font-weight="900" font-size="42" fill="{WHITE}" letter-spacing="-1">{date_text}</text>
  <text x="80" y="76" font-family="JetBrains Mono, monospace" font-weight="700" font-size="22" fill="{WHITE}" letter-spacing="2">{time_text}</text>
</g>
<!-- Divisória -->
<line x1="80" y1="{y_start+108}" x2="380" y2="{y_start+108}" stroke="{ORANGE}" stroke-width="2"/>
<!-- Pin -->
<g transform="translate(80,{y_start+138})">
  <path d="M28,4 C16,4 8,14 8,26 C8,42 28,68 28,68 C28,68 48,42 48,26 C48,14 40,4 28,4 Z M28,18 C32,18 36,22 36,26 C36,30 32,34 28,34 C24,34 20,30 20,26 C20,22 24,18 28,18 Z" fill="none" stroke="{ORANGE}" stroke-width="3"/>
  <text x="80" y="34" font-family="Poppins, sans-serif" font-weight="900" font-size="32" fill="{WHITE}" letter-spacing="1">{location_text.upper()}</text>
</g>'''


def speaker_block(name_first: str, name_last: str, company: str, role_lines: list[str], y_start: int = 820):
    """Bloco do palestrante: nome, empresa, cargo."""
    role_svg = ""
    for i, line in enumerate(role_lines):
        role_svg += f'<text x="92" y="{y_start+222 + i*26}" font-family="JetBrains Mono, monospace" font-weight="400" font-size="18" fill="{WHITE}" letter-spacing="1.5">{line.upper()}</text>\n  '
    return f'''
<!-- Nome do palestrante -->
<text x="80" y="{y_start+40}" font-family="Poppins, sans-serif" font-weight="900" font-size="56" fill="{WHITE}" letter-spacing="-1">{name_first.upper()}</text>
<text x="80" y="{y_start+98}" font-family="Poppins, sans-serif" font-weight="900" font-size="56" fill="{ORANGE}" letter-spacing="-1">{name_last.upper()}</text>
<!-- Empresa: círculo logo placeholder + nome -->
<g transform="translate(80,{y_start+130})">
  <circle cx="24" cy="24" r="22" fill="none" stroke="url(#orange-grad)" stroke-width="3"/>
  <circle cx="24" cy="24" r="10" fill="none" stroke="url(#orange-grad)" stroke-width="3"/>
  <text x="60" y="36" font-family="Poppins, sans-serif" font-weight="900" font-size="36" fill="{WHITE}" letter-spacing="2">{company.upper()}</text>
</g>
<!-- Cargo (barra laranja + texto) -->
<line x1="80" y1="{y_start+200}" x2="84" y2="{y_start+280}" stroke="{ORANGE}" stroke-width="4"/>
{role_svg}'''


def photo_placeholder():
    """Placeholder de foto à direita (oval mascarado)."""
    return f'''
<!-- Photo placeholder -->
<defs>
  <clipPath id="photo-clip">
    <ellipse cx="{W-280}" cy="780" rx="380" ry="540"/>
  </clipPath>
</defs>
<ellipse cx="{W-280}" cy="780" rx="380" ry="540" fill="url(#photo-grad)" opacity="0.45"/>
<g clip-path="url(#photo-clip)" opacity="0.7">
  <!-- silhueta abstrata -->
  <ellipse cx="{W-280}" cy="600" rx="120" ry="140" fill="#2a2a2a"/>
  <ellipse cx="{W-280}" cy="950" rx="240" ry="220" fill="#2a2a2a"/>
</g>
<text x="{W-280}" y="780" font-family="JetBrains Mono, monospace" font-weight="700" font-size="20" fill="{GRAY}" text-anchor="middle" letter-spacing="3">[ FOTO DO ]</text>
<text x="{W-280}" y="810" font-family="JetBrains Mono, monospace" font-weight="700" font-size="20" fill="{GRAY}" text-anchor="middle" letter-spacing="3">[ PALESTRANTE ]</text>'''


def footer_brand():
    """Logo iLab pequeno no rodapé."""
    return f'''
<!-- Footer -->
<g transform="translate(80,{H-90})">
  <text font-family="Poppins, sans-serif" font-weight="900" font-size="28" letter-spacing="-1">
    <tspan fill="{YELLOW}">i</tspan><tspan fill="{ORANGE}">Lab</tspan>
  </text>
  <text x="0" y="36" font-family="JetBrains Mono, monospace" font-weight="700" font-size="12" fill="{WHITE}" letter-spacing="3" opacity="0.6">SANFRAN · FD-USP</text>
</g>
<text x="{W-80}" y="{H-60}" font-family="JetBrains Mono, monospace" font-weight="700" font-size="13" fill="{ORANGE}" text-anchor="end" letter-spacing="3">@SANFRANILAB</text>'''


# ─────────────────────────────────────────
# Templates
# ─────────────────────────────────────────
def render(svg_body: str, filename: str):
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
{defs()}
{svg_body}
</svg>'''
    (OUT / filename).write_text(svg, encoding="utf-8")
    print(f"  ✓ {filename}")


# 1) iLab Conecta — palestrante (modelo base)
def template_conecta():
    body = (
        background()
        + photo_placeholder()
        + title_block("iLab", "conecta", ["IDEIAS QUE", "#CONECTAM,", "FUTUROS QUE", "#TRANSFORMAM."])
        + meta_block("DD.MM", "HH:MMPM", "Sanfran iLab")
        + speaker_block("Nome", "Sobrenome", "Empresa", ["Cargo e função do", "palestrante na empresa"])
        + footer_brand()
    )
    render(body, "ilab-conecta-palestrante.svg")


# 2) iLab Talks — bate-papo
def template_talks():
    body = (
        background()
        + photo_placeholder()
        + title_block("iLab", "talks", ["BATE-PAPO", "#ABERTO", "SOBRE DIREITO", "#E INOVAÇÃO."])
        + meta_block("DD.MM", "HH:MMPM", "Sanfran iLab")
        + speaker_block("Nome", "Sobrenome", "Empresa", ["Cargo · Empresa", "Tema da conversa"])
        + footer_brand()
    )
    render(body, "ilab-talks-batepapo.svg")


# 3) iLab Workshop — formato workshop prático
def template_workshop():
    body = (
        background()
        + photo_placeholder()
        + title_block("iLab", "workshop", ["MÃO NA MASSA.", "#RESULTADO", "REAL EM", "#90 MIN."])
        + meta_block("DD.MM", "HH:MMPM", "Sanfran iLab")
        + speaker_block("Facilitador", "Sobrenome", "Empresa", ["Workshop prático", "Vagas limitadas · Inscrições abertas"])
        + footer_brand()
    )
    render(body, "ilab-workshop.svg")


# 4) iLab Pitch — pitch competition
def template_pitch():
    body = (
        background()
        + photo_placeholder()
        + title_block("iLab", "pitch", ["APRESENTE", "#SUA IDEIA.", "CONECTE COM", "#INVESTIDORES."])
        + meta_block("DD.MM", "HH:MMPM", "Sanfran iLab")
        + speaker_block("Pitch", "Day", "iLab", ["Apresentação de startups", "Time pitch · 5 min cada"])
        + footer_brand()
    )
    render(body, "ilab-pitch-day.svg")


if __name__ == "__main__":
    print("Gerando templates de evento (1080x1350)…")
    template_conecta()
    template_talks()
    template_workshop()
    template_pitch()
    print(f"\nTotal: 4 templates SVG em {OUT}")
