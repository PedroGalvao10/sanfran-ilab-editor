"""
Gerador completo de assets visuais SanFran iLab.
Produz SVGs vetorizados em alta qualidade:
- 32 ícones em 3 estilos (outline, solid, duotone)
- 12 backgrounds abstratos (mesh gradients, blobs)
- 6 cenas 3D isométricas
- 4 padrões geométricos
- Componentes decorativos
Tudo dentro da paleta oficial.
"""
import os
from pathlib import Path

# Paleta oficial SanFran iLab
AMBAR    = "#F4C430"
LARANJA  = "#FF6B35"
CARMESIM = "#C41E3A"
PRETO    = "#1A1A1A"
CREME    = "#FAF3E0"
CINZA    = "#8E8E8E"

ROOT = Path(__file__).parent
OUT_ICONS     = ROOT / "assets" / "icons_v2"
OUT_CREATIVES = ROOT / "assets" / "creatives"
OUT_PATTERNS  = ROOT / "assets" / "patterns"
OUT_3D        = ROOT / "assets" / "scenes_3d"
OUT_DECOR     = ROOT / "assets" / "decoratives"

for d in [OUT_ICONS, OUT_CREATIVES, OUT_PATTERNS, OUT_3D, OUT_DECOR]:
    d.mkdir(parents=True, exist_ok=True)


# ════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════
def svg(content, w=64, h=64, vb=None):
    """Wrapper SVG padrão."""
    vb = vb or f"0 0 {w} {h}"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="{vb}" fill="none" stroke-linecap="round" stroke-linejoin="round">'
        f'{content}</svg>'
    )


def save(path, content):
    Path(path).write_text(content, encoding="utf-8")


# ════════════════════════════════════════════════
# ÍCONES — 32 unidades em 8 temas
# Cada ícone retorna o miolo do SVG (path/g elements)
# Geramos depois em 3 variantes: outline / solid / duotone
# ════════════════════════════════════════════════
ICON_PATHS = {
    # ─── JURÍDICO ───
    "scales": '<path d="M32 8v48M16 56h32M22 20h20M14 24l-6 16h12zM50 24l-6 16h12zM8 40c0 4 4 6 6 6s6-2 6-6M44 40c0 4 4 6 6 6s6-2 6-6"/>',
    "gavel": '<path d="M14 50l28-28M18 54l8-8M40 22l14 14M30 12l22 22M14 50l-4 4 4 4 4-4z"/>',
    "contract": '<path d="M14 8h28l8 8v40H14zM42 8v8h8M20 24h24M20 32h24M20 40h16M28 48h16l-2-3-2 3-2-3-2 3-2-3-2 3z"/>',
    "courthouse": '<path d="M8 56h48M12 56V28M20 56V28M28 56V28M36 56V28M44 56V28M52 56V28M6 28h52L32 12z"/>',

    # ─── TECH ───
    "cpu": '<path d="M16 16h32v32H16zM24 24h16v16H24zM24 8v8M40 8v8M24 48v8M40 48v8M8 24h8M8 40h8M48 24h8M48 40h8"/>',
    "code": '<path d="M22 18L8 32l14 14M42 18l14 14-14 14M38 12l-12 40"/>',
    "cloud": '<path d="M20 40c-6 0-10-4-10-10s4-10 10-10c2-8 10-12 18-10s12 10 10 18c4 0 8 4 8 8s-4 8-8 8H20z"/>',
    "api": '<rect x="8" y="20" width="48" height="24" rx="4"/><path d="M16 32h6M28 32h8M42 32h6M20 16v4M44 16v4M20 44v4M44 44v4"/>',

    # ─── INOVAÇÃO ───
    "lightbulb": '<path d="M32 6c-10 0-18 8-18 18 0 8 4 12 8 16v8h20v-8c4-4 8-8 8-16 0-10-8-18-18-18zM22 56h20M26 60h12"/>',
    "rocket": '<path d="M32 6c-8 8-12 16-12 26v16l6-4 6 4 6-4 6 4V32c0-10-4-18-12-26zM26 28a6 6 0 1 0 12 0 6 6 0 1 0-12 0zM18 44l-8 4v8l10-4M46 44l8 4v8l-10-4"/>',
    "gear-arrow": '<path d="M32 18a14 14 0 1 1 0 28 14 14 0 1 1 0-28zM32 8v6M32 50v6M14 32h6M44 32h6M19 19l4 4M41 41l4 4M19 45l4-4M41 23l4-4M28 32h12M36 28l4 4-4 4"/>',
    "blueprint": '<rect x="8" y="12" width="48" height="40" rx="2"/><path d="M16 20h12v12H16zM34 20h14M34 28h14M16 38h32M16 44h22"/>',

    # ─── EDUCAÇÃO ───
    "book": '<path d="M32 14v44M12 14c0-2 2-4 4-4h14c2 0 2 2 2 4M52 14c0-2-2-4-4-4H34c-2 0-2 2-2 4M12 14v40c0 2 2 4 4 4h14c2 0 2-2 2-4M52 14v40c0-2-2 4-4 4H34c-2 0-2-2-2-4"/>',
    "mortarboard": '<path d="M4 22l28-12 28 12-28 12zM14 28v14c0 4 8 8 18 8s18-4 18-8V28M56 22v16"/>',
    "chalkboard": '<rect x="6" y="8" width="52" height="36" rx="2"/><path d="M2 44h60M22 50l-4 8M42 50l4 8M14 16h20M14 24h24M14 32h16"/>',
    "certificate": '<path d="M10 8h44v36H10zM10 44l-2 12 12-4 12 4-2-12M18 18h28M18 24h28M18 30h20"/>',

    # ─── COMUNIDADE ───
    "handshake": '<path d="M4 32l8-8 8 4 12 12 4-4 8 8M60 32l-8-8-8 4-12 12M20 36l8 8M40 36l-8 8M32 24v-8"/>',
    "network": '<circle cx="32" cy="14" r="6"/><circle cx="12" cy="44" r="6"/><circle cx="52" cy="44" r="6"/><circle cx="32" cy="44" r="6"/><path d="M30 20l-14 18M34 20l14 18M32 20v18"/>',
    "megaphone": '<path d="M8 24v16l24 8V16zM32 16l16-8v48l-16-8M48 24c4 0 8 4 8 8s-4 8-8 8M12 40v8h10v-6"/>',
    "globe": '<circle cx="32" cy="32" r="22"/><path d="M10 32h44M32 10c8 8 8 36 0 44M32 10c-8 8-8 36 0 44M14 18c10 6 26 6 36 0M14 46c10-6 26-6 36 0"/>',

    # ─── MÍDIA ───
    "camera": '<rect x="6" y="16" width="52" height="36" rx="4"/><circle cx="32" cy="34" r="10"/><path d="M22 16l4-6h12l4 6"/>',
    "microphone": '<rect x="24" y="8" width="16" height="28" rx="8"/><path d="M16 32c0 8 8 16 16 16s16-8 16-16M32 48v8M20 56h24"/>',
    "broadcast": '<circle cx="32" cy="32" r="4"/><path d="M22 22a14 14 0 0 0 0 20M42 22a14 14 0 0 1 0 20M14 14a26 26 0 0 0 0 36M50 14a26 26 0 0 1 0 36M32 36v20"/>',
    "play-circle": '<circle cx="32" cy="32" r="26"/><path d="M26 22l16 10-16 10z"/>',

    # ─── WORKFLOW ───
    "kanban": '<rect x="6" y="8" width="52" height="48" rx="2"/><path d="M22 8v48M42 8v48M10 16h8M10 24h8M10 32h8M26 16h12M26 24h12M46 16h8"/>',
    "checklist": '<rect x="10" y="8" width="44" height="48" rx="2"/><path d="M18 18l4 4 8-8M18 30l4 4 8-8M18 42l4 4 8-8M38 20h12M38 32h12M38 44h12"/>',
    "calendar": '<rect x="8" y="14" width="48" height="42" rx="3"/><path d="M8 26h48M20 8v12M44 8v12M18 36h6M30 36h6M42 36h6M18 46h6M30 46h6M42 46h6"/>',
    "sync": '<path d="M12 32a20 20 0 0 1 36-12M52 32a20 20 0 0 1-36 12M48 12v10h-10M16 52v-10h10"/>',

    # ─── MÉTRICAS ───
    "chart-bar": '<path d="M8 56V36h10v20zM26 56V20h10v36zM44 56V28h10v28zM6 56h54"/>',
    "chart-line": '<path d="M8 48l12-12 8 6 12-18 16 12M8 56h48M14 14l2 4 4 2-4 2-2 4-2-4-4-2 4-2z"/>',
    "target": '<circle cx="32" cy="32" r="22"/><circle cx="32" cy="32" r="14"/><circle cx="32" cy="32" r="6"/><path d="M44 20l8-8M52 12h-6m6 0v6"/>',
    "pulse": '<path d="M4 32h12l4-12 8 24 6-18 4 6h22"/>',
}


def make_icon_outline(path_data, stroke_color=PRETO):
    """Ícone em outline (stroke only)."""
    content = f'<g stroke="{stroke_color}" stroke-width="2.5" fill="none">{path_data}</g>'
    return svg(content)


def make_icon_solid(path_data, fill_color=AMBAR):
    """Ícone em solid (fill only)."""
    # Para solid, usamos stroke + fill da mesma cor
    content = f'<g stroke="{fill_color}" stroke-width="2" fill="{fill_color}">{path_data}</g>'
    return svg(content)


def make_icon_duotone(path_data, fill_color=AMBAR, stroke_color=PRETO):
    """Ícone duotone: fundo âmbar + traço preto."""
    content = (
        f'<rect x="4" y="4" width="56" height="56" rx="12" fill="{fill_color}" opacity="0.18"/>'
        f'<g stroke="{stroke_color}" stroke-width="2.5" fill="none">{path_data}</g>'
    )
    return svg(content)


def make_icon_gradient(path_data):
    """Ícone com gradiente âmbar→laranja (premium)."""
    gradient = (
        f'<defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">'
        f'<stop offset="0%" stop-color="{AMBAR}"/>'
        f'<stop offset="100%" stop-color="{LARANJA}"/>'
        f'</linearGradient></defs>'
    )
    content = f'{gradient}<g stroke="url(#g)" stroke-width="3" fill="none">{path_data}</g>'
    return svg(content)


print(">>> Gerando ícones...")
total_icons = 0
for name, path_data in ICON_PATHS.items():
    save(OUT_ICONS / f"{name}-outline.svg", make_icon_outline(path_data))
    save(OUT_ICONS / f"{name}-solid.svg",   make_icon_solid(path_data, LARANJA))
    save(OUT_ICONS / f"{name}-duotone.svg", make_icon_duotone(path_data))
    save(OUT_ICONS / f"{name}-gradient.svg", make_icon_gradient(path_data))
    total_icons += 4
print(f"   {total_icons} SVGs de ícones gerados em {OUT_ICONS}")


# ════════════════════════════════════════════════
# CRIATIVOS ABSTRATOS — Mesh Gradients & Blobs
# ════════════════════════════════════════════════
def mesh_gradient(seed_name, color_a, color_b, color_c):
    """Gera um mesh gradient SVG complexo."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">
  <defs>
    <radialGradient id="g1" cx="20%" cy="30%" r="60%">
      <stop offset="0%" stop-color="{color_a}" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="{color_a}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="g2" cx="80%" cy="20%" r="55%">
      <stop offset="0%" stop-color="{color_b}" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="{color_b}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="g3" cx="60%" cy="90%" r="70%">
      <stop offset="0%" stop-color="{color_c}" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="{color_c}" stop-opacity="0"/>
    </radialGradient>
    <filter id="blur"><feGaussianBlur stdDeviation="40"/></filter>
  </defs>
  <rect width="800" height="600" fill="{PRETO}"/>
  <g filter="url(#blur)">
    <rect width="800" height="600" fill="url(#g1)"/>
    <rect width="800" height="600" fill="url(#g2)"/>
    <rect width="800" height="600" fill="url(#g3)"/>
  </g>
</svg>'''


def blob_organic(seed, color):
    """Blob orgânico animado."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <linearGradient id="bg{seed}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{color}"/>
      <stop offset="100%" stop-color="{LARANJA}"/>
    </linearGradient>
  </defs>
  <path fill="url(#bg{seed})" d="M{200 + seed*5},{60+seed*3} C{280+seed*4},{80+seed*2} {340-seed*3},{160+seed*5} {320+seed*2},{240-seed*4} C{300-seed*5},{320+seed*3} {220+seed*4},{350-seed*2} {140-seed*3},{320+seed*5} C{60+seed*2},{290-seed*4} {40+seed*5},{200+seed*3} {70-seed*2},{130-seed*5} C{100+seed*3},{60+seed*4} {140-seed*5},{50+seed*2} {200+seed*5},{60+seed*3} Z"/>
</svg>'''


print(">>> Gerando criativos abstratos...")
creatives = [
    ("mesh-amber-sunrise",   AMBAR,    LARANJA,  CREME),
    ("mesh-crimson-ember",   CARMESIM, LARANJA,  AMBAR),
    ("mesh-dark-glow",       LARANJA,  AMBAR,    PRETO),
    ("mesh-warm-haze",       CREME,    AMBAR,    LARANJA),
    ("mesh-ember-deep",      CARMESIM, AMBAR,    PRETO),
    ("mesh-golden-flare",    AMBAR,    AMBAR,    LARANJA),
    ("mesh-sunset-fold",     LARANJA,  CARMESIM, AMBAR),
    ("mesh-charcoal-bloom",  PRETO,    LARANJA,  CARMESIM),
    ("mesh-vanilla-dawn",    CREME,    AMBAR,    CREME),
    ("mesh-amber-storm",     AMBAR,    CARMESIM, PRETO),
    ("mesh-fire-pulse",      LARANJA,  LARANJA,  CARMESIM),
    ("mesh-soft-radiance",   AMBAR,    CREME,    LARANJA),
]
for i, (name, a, b, c) in enumerate(creatives):
    save(OUT_CREATIVES / f"{name}.svg", mesh_gradient(name, a, b, c))

# Blobs
blob_colors = [AMBAR, LARANJA, CARMESIM, AMBAR, LARANJA, CARMESIM, AMBAR, LARANJA]
for i, color in enumerate(blob_colors):
    save(OUT_CREATIVES / f"blob-{i+1:02d}.svg", blob_organic(i+1, color))

print(f"   {len(creatives)} mesh gradients + {len(blob_colors)} blobs gerados")


# ════════════════════════════════════════════════
# PADRÕES GEOMÉTRICOS
# ════════════════════════════════════════════════
PATTERNS = {
    "dot-amber": f'''<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40">
  <defs><pattern id="p" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
    <circle cx="10" cy="10" r="1.5" fill="{AMBAR}" opacity="0.6"/>
  </pattern></defs>
  <rect width="40" height="40" fill="{PRETO}"/>
  <rect width="40" height="40" fill="url(#p)"/>
</svg>''',

    "grid-warm": f'''<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 60 60">
  <defs><pattern id="p" x="0" y="0" width="30" height="30" patternUnits="userSpaceOnUse">
    <path d="M30 0V30M0 30H30" stroke="{LARANJA}" stroke-width="0.5" opacity="0.4"/>
  </pattern></defs>
  <rect width="60" height="60" fill="{CREME}"/>
  <rect width="60" height="60" fill="url(#p)"/>
</svg>''',

    "wave-ember": f'''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100" viewBox="0 0 200 100">
  <rect width="200" height="100" fill="{PRETO}"/>
  <path d="M0 50 Q 25 30, 50 50 T 100 50 T 150 50 T 200 50" stroke="{AMBAR}" stroke-width="2" fill="none" opacity="0.7"/>
  <path d="M0 60 Q 25 40, 50 60 T 100 60 T 150 60 T 200 60" stroke="{LARANJA}" stroke-width="2" fill="none" opacity="0.6"/>
  <path d="M0 70 Q 25 50, 50 70 T 100 70 T 150 70 T 200 70" stroke="{CARMESIM}" stroke-width="2" fill="none" opacity="0.5"/>
</svg>''',

    "hex-golden": f'''<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
  <defs><pattern id="hx" x="0" y="0" width="20" height="17.32" patternUnits="userSpaceOnUse">
    <polygon points="10,1 18,5.5 18,15 10,19 2,15 2,5.5" stroke="{AMBAR}" stroke-width="1" fill="none" opacity="0.5"/>
  </pattern></defs>
  <rect width="100" height="100" fill="{PRETO}"/>
  <rect width="100" height="100" fill="url(#hx)"/>
</svg>''',
}

print(">>> Gerando padrões...")
for name, content in PATTERNS.items():
    save(OUT_PATTERNS / f"{name}.svg", content)
print(f"   {len(PATTERNS)} padrões geométricos gerados")


# ════════════════════════════════════════════════
# CENAS 3D ISOMÉTRICAS
# ════════════════════════════════════════════════
def scene_iso_cube_stack():
    """Pilha de cubos isométricos."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <linearGradient id="top" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{AMBAR}"/><stop offset="1" stop-color="{LARANJA}"/></linearGradient>
    <linearGradient id="left" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{LARANJA}"/><stop offset="1" stop-color="{CARMESIM}"/></linearGradient>
    <linearGradient id="right" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CARMESIM}"/><stop offset="1" stop-color="{PRETO}"/></linearGradient>
  </defs>
  <rect width="400" height="400" fill="{PRETO}"/>
  <!-- Base cube -->
  <polygon points="200,280 280,240 360,280 280,320" fill="url(#top)"/>
  <polygon points="200,280 200,360 280,400 280,320" fill="url(#left)"/>
  <polygon points="280,320 360,280 360,360 280,400" fill="url(#right)"/>
  <!-- Mid cube -->
  <polygon points="160,200 240,160 320,200 240,240" fill="url(#top)" opacity="0.95"/>
  <polygon points="160,200 160,280 240,320 240,240" fill="url(#left)" opacity="0.95"/>
  <polygon points="240,240 320,200 320,280 240,320" fill="url(#right)" opacity="0.95"/>
  <!-- Top cube -->
  <polygon points="200,120 280,80 360,120 280,160" fill="url(#top)" opacity="0.9"/>
  <polygon points="200,120 200,200 280,240 280,160" fill="url(#left)" opacity="0.9"/>
  <polygon points="280,160 360,120 360,200 280,240" fill="url(#right)" opacity="0.9"/>
</svg>'''


def scene_iso_network():
    """Rede 3D de nós conectados."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <rect width="400" height="400" fill="{PRETO}"/>
  <g stroke="{AMBAR}" stroke-width="1.5" opacity="0.6">
    <line x1="100" y1="100" x2="200" y2="200"/>
    <line x1="300" y1="100" x2="200" y2="200"/>
    <line x1="100" y1="300" x2="200" y2="200"/>
    <line x1="300" y1="300" x2="200" y2="200"/>
    <line x1="100" y1="100" x2="300" y2="100"/>
    <line x1="100" y1="300" x2="300" y2="300"/>
    <line x1="200" y1="200" x2="200" y2="80"/>
    <line x1="200" y1="200" x2="200" y2="320"/>
  </g>
  <g fill="url(#sphereGrad)">
    <defs><radialGradient id="sphereGrad"><stop offset="0" stop-color="{AMBAR}"/><stop offset="1" stop-color="{LARANJA}"/></radialGradient></defs>
    <circle cx="100" cy="100" r="14"/>
    <circle cx="300" cy="100" r="14"/>
    <circle cx="100" cy="300" r="14"/>
    <circle cx="300" cy="300" r="14"/>
    <circle cx="200" cy="200" r="22"/>
    <circle cx="200" cy="80" r="10"/>
    <circle cx="200" cy="320" r="10"/>
  </g>
</svg>'''


def scene_iso_layers():
    """Camadas 3D empilhadas (arquitetura)."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <linearGradient id="lyr1"><stop offset="0" stop-color="{AMBAR}"/><stop offset="1" stop-color="{LARANJA}"/></linearGradient>
  </defs>
  <rect width="400" height="400" fill="{PRETO}"/>
  <g>
    <polygon points="60,310 200,240 340,310 200,380" fill="{AMBAR}" opacity="0.95"/>
    <polygon points="60,310 60,330 200,400 200,380" fill="{LARANJA}" opacity="0.85"/>
    <polygon points="200,380 340,310 340,330 200,400" fill="{CARMESIM}" opacity="0.85"/>
  </g>
  <g transform="translate(0,-60)">
    <polygon points="80,310 200,250 320,310 200,370" fill="{AMBAR}" opacity="0.85"/>
    <polygon points="80,310 80,325 200,385 200,370" fill="{LARANJA}" opacity="0.75"/>
    <polygon points="200,370 320,310 320,325 200,385" fill="{CARMESIM}" opacity="0.75"/>
  </g>
  <g transform="translate(0,-120)">
    <polygon points="100,310 200,260 300,310 200,360" fill="{AMBAR}" opacity="0.75"/>
    <polygon points="100,310 100,320 200,370 200,360" fill="{LARANJA}" opacity="0.65"/>
    <polygon points="200,360 300,310 300,320 200,370" fill="{CARMESIM}" opacity="0.65"/>
  </g>
</svg>'''


def scene_3d_sphere():
    """Esfera 3D com highlight."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <radialGradient id="sph" cx="35%" cy="35%">
      <stop offset="0%" stop-color="{CREME}"/>
      <stop offset="30%" stop-color="{AMBAR}"/>
      <stop offset="70%" stop-color="{LARANJA}"/>
      <stop offset="100%" stop-color="{CARMESIM}"/>
    </radialGradient>
    <radialGradient id="shadow" cx="50%" cy="50%">
      <stop offset="0%" stop-color="{PRETO}" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="{PRETO}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="400" height="400" fill="{PRETO}"/>
  <ellipse cx="200" cy="360" rx="100" ry="14" fill="url(#shadow)"/>
  <circle cx="200" cy="200" r="130" fill="url(#sph)"/>
</svg>'''


def scene_3d_torus():
    """Torus/anel 3D."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <linearGradient id="ring" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{AMBAR}"/>
      <stop offset="0.5" stop-color="{LARANJA}"/>
      <stop offset="1" stop-color="{CARMESIM}"/>
    </linearGradient>
  </defs>
  <rect width="400" height="400" fill="{PRETO}"/>
  <g transform="translate(200 200) rotate(-25)">
    <ellipse cx="0" cy="0" rx="140" ry="60" fill="none" stroke="url(#ring)" stroke-width="40"/>
    <ellipse cx="0" cy="0" rx="140" ry="60" fill="none" stroke="{PRETO}" stroke-width="2" opacity="0.3"/>
  </g>
</svg>'''


def scene_3d_pyramid():
    """Pirâmide 3D vista isométrica."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <rect width="400" height="400" fill="{PRETO}"/>
  <g>
    <polygon points="200,80 100,320 200,300" fill="{AMBAR}"/>
    <polygon points="200,80 200,300 300,320" fill="{LARANJA}"/>
    <polygon points="100,320 200,300 300,320 200,360" fill="{CARMESIM}"/>
  </g>
</svg>'''


print(">>> Gerando cenas 3D isométricas...")
scenes = {
    "iso-cube-stack":   scene_iso_cube_stack(),
    "iso-network":      scene_iso_network(),
    "iso-layers":       scene_iso_layers(),
    "3d-sphere":        scene_3d_sphere(),
    "3d-torus":         scene_3d_torus(),
    "3d-pyramid":       scene_3d_pyramid(),
}
for name, content in scenes.items():
    save(OUT_3D / f"{name}.svg", content)
print(f"   {len(scenes)} cenas 3D geradas")


# ════════════════════════════════════════════════
# DECORATIVES — Frames, dividers, badges, brackets
# ════════════════════════════════════════════════
DECORATIVES = {
    "bracket-corner-tl": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80">
  <path d="M10 30V10H30" stroke="{AMBAR}" stroke-width="4" fill="none"/>
  <circle cx="10" cy="10" r="4" fill="{LARANJA}"/>
</svg>''',

    "divider-flame": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 40" width="400" height="40">
  <line x1="0" y1="20" x2="160" y2="20" stroke="{AMBAR}" stroke-width="2"/>
  <line x1="240" y1="20" x2="400" y2="20" stroke="{AMBAR}" stroke-width="2"/>
  <g transform="translate(200 20)">
    <path d="M-12 0 L0 -16 L12 0 L0 16 Z" fill="{LARANJA}"/>
    <circle cx="0" cy="0" r="4" fill="{CREME}"/>
  </g>
</svg>''',

    "badge-circle": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{AMBAR}"/><stop offset="1" stop-color="{LARANJA}"/></linearGradient>
  </defs>
  <circle cx="60" cy="60" r="56" fill="url(#bg)"/>
  <circle cx="60" cy="60" r="48" fill="none" stroke="{PRETO}" stroke-width="2"/>
  <text x="60" y="68" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="22" fill="{PRETO}">iLab</text>
</svg>''',

    "arrow-stylized": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 60" width="200" height="60">
  <path d="M10 30 L160 30 M140 12 L160 30 L140 48" stroke="{AMBAR}" stroke-width="4" fill="none"/>
  <circle cx="10" cy="30" r="6" fill="{LARANJA}"/>
</svg>''',

    "spark-corner": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80">
  <g fill="{AMBAR}">
    <path d="M40 10 L44 36 L70 40 L44 44 L40 70 L36 44 L10 40 L36 36 Z"/>
  </g>
  <circle cx="40" cy="40" r="6" fill="{LARANJA}"/>
</svg>''',

    "tag-banner": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 60" width="200" height="60">
  <defs><linearGradient id="bn" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{AMBAR}"/><stop offset="1" stop-color="{LARANJA}"/></linearGradient></defs>
  <polygon points="10,10 170,10 190,30 170,50 10,50" fill="url(#bn)"/>
  <circle cx="22" cy="30" r="4" fill="{PRETO}"/>
  <text x="40" y="36" font-family="JetBrains Mono,monospace" font-size="14" font-weight="700" fill="{PRETO}">SANFRAN iLab</text>
</svg>''',

    "quote-marks": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 80" width="120" height="80">
  <g fill="{AMBAR}">
    <path d="M10 50 Q10 20 40 20 Q40 30 25 35 Q30 38 30 50 Q30 60 20 60 Q10 60 10 50 Z"/>
    <path d="M70 50 Q70 20 100 20 Q100 30 85 35 Q90 38 90 50 Q90 60 80 60 Q70 60 70 50 Z"/>
  </g>
</svg>''',

    "ribbon": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 60" width="240" height="60">
  <defs><linearGradient id="rb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CARMESIM}"/><stop offset="1" stop-color="{LARANJA}"/></linearGradient></defs>
  <polygon points="0,10 220,10 240,30 220,50 0,50 20,30" fill="url(#rb)"/>
  <text x="120" y="36" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="16" fill="{CREME}">DESTAQUE</text>
</svg>''',
}

print(">>> Gerando decoratives...")
for name, content in DECORATIVES.items():
    save(OUT_DECOR / f"{name}.svg", content)
print(f"   {len(DECORATIVES)} decoratives gerados")


# ════════════════════════════════════════════════
# FINAL REPORT
# ════════════════════════════════════════════════
total = total_icons + len(creatives) + len(blob_colors) + len(PATTERNS) + len(scenes) + len(DECORATIVES)
print()
print("=" * 60)
print(f"✅ TOTAL: {total} assets vetorizados gerados")
print(f"   Ícones:      {total_icons}")
print(f"   Mesh grads:  {len(creatives)}")
print(f"   Blobs:       {len(blob_colors)}")
print(f"   Padrões:     {len(PATTERNS)}")
print(f"   Cenas 3D:    {len(scenes)}")
print(f"   Decoratives: {len(DECORATIVES)}")
print("=" * 60)
