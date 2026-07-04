"""
Gera assets de Liquid Glass, Tech, Bolhas, Vidro e Holográficos.
Usa SVG filter primitives: feTurbulence, feDisplacementMap, feSpecularLighting, feGaussianBlur.
Mantém a paleta oficial SanFran iLab.
"""
import os
from pathlib import Path

AMBAR    = "#F4C430"
LARANJA  = "#FF6B35"
CARMESIM = "#C41E3A"
PRETO    = "#1A1A1A"
CREME    = "#FAF3E0"

ROOT = Path(__file__).parent
OUT_GLASS = ROOT / "assets" / "glass"
OUT_TECH  = ROOT / "assets" / "tech"
OUT_BUBBLE= ROOT / "assets" / "bubbles"
OUT_HOLO  = ROOT / "assets" / "holographic"
for d in [OUT_GLASS, OUT_TECH, OUT_BUBBLE, OUT_HOLO]:
    d.mkdir(parents=True, exist_ok=True)


def save(path, content):
    Path(path).write_text(content, encoding="utf-8")


# ══════════════════════════════════════════════════════
# LIQUID GLASS CARDS · 8
# Usa feTurbulence + feDisplacementMap + feSpecularLighting
# ══════════════════════════════════════════════════════
def glass_card_frosted(tint=AMBAR, seed=1):
    """Card frosted glass com tint amber."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300" width="480" height="300">
  <defs>
    <linearGradient id="bgg{seed}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{tint}"/>
      <stop offset="1" stop-color="{LARANJA}"/>
    </linearGradient>
    <filter id="frost{seed}" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="{seed}"/>
      <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.15 0"/>
      <feComposite in2="SourceGraphic" operator="in"/>
      <feMerge><feMergeNode in="SourceGraphic"/><feMergeNode/></feMerge>
    </filter>
    <filter id="shine{seed}">
      <feGaussianBlur stdDeviation="2"/>
      <feSpecularLighting surfaceScale="3" specularConstant="1.5" specularExponent="20" lighting-color="white">
        <feDistantLight azimuth="135" elevation="60"/>
      </feSpecularLighting>
      <feComposite in2="SourceGraphic" operator="in"/>
    </filter>
  </defs>
  <rect width="480" height="300" fill="url(#bgg{seed})"/>
  <g filter="url(#frost{seed})">
    <rect x="40" y="40" width="400" height="220" rx="24" fill="rgba(255,255,255,0.18)" stroke="rgba(255,255,255,0.35)" stroke-width="1"/>
  </g>
  <rect x="40" y="40" width="400" height="220" rx="24" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="1.5"/>
  <ellipse cx="120" cy="80" rx="80" ry="14" fill="rgba(255,255,255,0.3)" filter="url(#shine{seed})"/>
  <text x="64" y="148" font-family="Poppins,sans-serif" font-weight="900" font-size="32" fill="white">Glass</text>
  <text x="64" y="180" font-family="JetBrains Mono,monospace" font-size="11" fill="rgba(255,255,255,0.8)" letter-spacing="2">FROSTED · {tint.upper()}</text>
</svg>'''


def glass_card_refraction(seed=2):
    """Card com forte refração (distorção líquida)."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300" width="480" height="300">
  <defs>
    <linearGradient id="bgr{seed}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{AMBAR}"/>
      <stop offset="0.5" stop-color="{LARANJA}"/>
      <stop offset="1" stop-color="{CARMESIM}"/>
    </linearGradient>
    <filter id="distort{seed}" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="turbulence" baseFrequency="0.015 0.03" numOctaves="2" seed="{seed*3}"/>
      <feDisplacementMap in="SourceGraphic" scale="22"/>
    </filter>
    <filter id="refrSpec{seed}">
      <feGaussianBlur stdDeviation="1"/>
      <feSpecularLighting surfaceScale="6" specularConstant="2" specularExponent="25" lighting-color="white">
        <feDistantLight azimuth="120" elevation="55"/>
      </feSpecularLighting>
    </filter>
  </defs>
  <rect width="480" height="300" fill="url(#bgr{seed})"/>
  <g filter="url(#distort{seed})">
    <rect x="60" y="50" width="360" height="200" rx="30" fill="rgba(255,255,255,0.25)" stroke="rgba(255,255,255,0.45)" stroke-width="2"/>
  </g>
  <rect x="60" y="50" width="360" height="200" rx="30" fill="none" stroke="rgba(255,255,255,0.6)" stroke-width="1"/>
  <g opacity="0.6">
    <ellipse cx="160" cy="100" rx="70" ry="10" fill="white" filter="url(#refrSpec{seed})"/>
  </g>
</svg>'''


def glass_card_neon(seed=3):
    """Card com borda neon glow."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300" width="480" height="300">
  <defs>
    <filter id="neon{seed}" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <rect width="480" height="300" fill="{PRETO}"/>
  <g filter="url(#neon{seed})">
    <rect x="50" y="40" width="380" height="220" rx="24" fill="none" stroke="{AMBAR}" stroke-width="2"/>
  </g>
  <rect x="50" y="40" width="380" height="220" rx="24" fill="rgba(244,196,48,0.05)" stroke="{AMBAR}" stroke-width="1"/>
  <g filter="url(#neon{seed})">
    <text x="240" y="160" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="36" fill="{AMBAR}">NEON</text>
  </g>
  <text x="240" y="200" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="11" letter-spacing="3" fill="{LARANJA}">CYBER · GLASS</text>
</svg>'''


def glass_card_chrome(seed=4):
    """Card com efeito chrome/metálico."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300" width="480" height="300">
  <defs>
    <linearGradient id="chrome{seed}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{CREME}"/>
      <stop offset="0.3" stop-color="{AMBAR}"/>
      <stop offset="0.5" stop-color="{LARANJA}"/>
      <stop offset="0.7" stop-color="{AMBAR}"/>
      <stop offset="1" stop-color="{CREME}"/>
    </linearGradient>
    <filter id="bevel{seed}">
      <feGaussianBlur stdDeviation="1.5"/>
      <feSpecularLighting surfaceScale="4" specularConstant="2.4" specularExponent="40" lighting-color="white">
        <feDistantLight azimuth="135" elevation="65"/>
      </feSpecularLighting>
      <feComposite in2="SourceGraphic" operator="in"/>
    </filter>
  </defs>
  <rect width="480" height="300" fill="{PRETO}"/>
  <rect x="40" y="40" width="400" height="220" rx="28" fill="url(#chrome{seed})"/>
  <rect x="40" y="40" width="400" height="220" rx="28" fill="rgba(255,255,255,0.4)" filter="url(#bevel{seed})"/>
  <text x="240" y="170" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="36" fill="{PRETO}">CHROME</text>
</svg>'''


def glass_card_iridescent(seed=5):
    """Card iridescente (foil/holográfico mantendo paleta)."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300" width="480" height="300">
  <defs>
    <linearGradient id="irid{seed}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{AMBAR}" stop-opacity="0.9"/>
      <stop offset="0.25" stop-color="{LARANJA}" stop-opacity="0.95"/>
      <stop offset="0.5" stop-color="{CARMESIM}" stop-opacity="0.9"/>
      <stop offset="0.75" stop-color="{LARANJA}" stop-opacity="0.95"/>
      <stop offset="1" stop-color="{AMBAR}" stop-opacity="0.9"/>
    </linearGradient>
    <filter id="noise{seed}">
      <feTurbulence type="fractalNoise" baseFrequency="2.5" numOctaves="1" seed="{seed*7}"/>
      <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.08 0"/>
      <feComposite in2="SourceGraphic" operator="in"/>
      <feMerge><feMergeNode in="SourceGraphic"/><feMergeNode/></feMerge>
    </filter>
  </defs>
  <rect width="480" height="300" fill="{PRETO}"/>
  <g filter="url(#noise{seed})">
    <rect x="40" y="40" width="400" height="220" rx="28" fill="url(#irid{seed})"/>
  </g>
  <rect x="40" y="40" width="400" height="220" rx="28" fill="none" stroke="rgba(255,255,255,0.45)" stroke-width="1.5"/>
  <text x="240" y="170" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="34" fill="{PRETO}">IRIDESCENT</text>
</svg>'''


def glass_card_aurora(seed=6):
    """Card aurora — gradiente fluido + blur."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300" width="480" height="300">
  <defs>
    <radialGradient id="a{seed}1" cx="20%" cy="30%" r="55%">
      <stop offset="0" stop-color="{AMBAR}" stop-opacity="0.95"/>
      <stop offset="1" stop-color="{AMBAR}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="a{seed}2" cx="80%" cy="40%" r="55%">
      <stop offset="0" stop-color="{LARANJA}" stop-opacity="0.95"/>
      <stop offset="1" stop-color="{LARANJA}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="a{seed}3" cx="50%" cy="90%" r="60%">
      <stop offset="0" stop-color="{CARMESIM}" stop-opacity="0.85"/>
      <stop offset="1" stop-color="{CARMESIM}" stop-opacity="0"/>
    </radialGradient>
    <filter id="auroraBlur{seed}"><feGaussianBlur stdDeviation="30"/></filter>
  </defs>
  <rect width="480" height="300" fill="{PRETO}"/>
  <g filter="url(#auroraBlur{seed})">
    <rect width="480" height="300" fill="url(#a{seed}1)"/>
    <rect width="480" height="300" fill="url(#a{seed}2)"/>
    <rect width="480" height="300" fill="url(#a{seed}3)"/>
  </g>
  <rect x="40" y="40" width="400" height="220" rx="28" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.4)" stroke-width="1.5"/>
  <text x="240" y="170" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="34" fill="white">AURORA</text>
</svg>'''


def glass_card_prism(seed=7):
    """Card prism — facetas geométricas com blur."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300" width="480" height="300">
  <defs>
    <linearGradient id="p1{seed}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{AMBAR}"/><stop offset="1" stop-color="{LARANJA}"/></linearGradient>
    <linearGradient id="p2{seed}" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{LARANJA}"/><stop offset="1" stop-color="{CARMESIM}"/></linearGradient>
    <linearGradient id="p3{seed}" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="{CARMESIM}"/><stop offset="1" stop-color="{AMBAR}"/></linearGradient>
    <filter id="prBlur{seed}"><feGaussianBlur stdDeviation="0.8"/></filter>
  </defs>
  <rect width="480" height="300" fill="{PRETO}"/>
  <g filter="url(#prBlur{seed})">
    <polygon points="40,40 280,40 200,150 40,150" fill="url(#p1{seed})" opacity="0.95"/>
    <polygon points="280,40 440,40 440,150 200,150" fill="url(#p2{seed})" opacity="0.95"/>
    <polygon points="40,150 440,150 440,260 40,260" fill="url(#p3{seed})" opacity="0.95"/>
  </g>
  <rect x="40" y="40" width="400" height="220" rx="28" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="1.5"/>
  <text x="240" y="180" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="34" fill="white">PRISM</text>
</svg>'''


def glass_card_holographic(seed=8):
    """Card holográfico — gradiente cônico + grid + noise."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300" width="480" height="300">
  <defs>
    <linearGradient id="ho{seed}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{AMBAR}"/>
      <stop offset="0.33" stop-color="{LARANJA}"/>
      <stop offset="0.66" stop-color="{CARMESIM}"/>
      <stop offset="1" stop-color="{AMBAR}"/>
    </linearGradient>
    <pattern id="hgrid{seed}" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M20 0H0v20" fill="none" stroke="rgba(255,255,255,0.18)" stroke-width="0.5"/>
    </pattern>
    <filter id="hnoise{seed}">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="{seed*4}"/>
      <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.1 0"/>
      <feComposite in2="SourceGraphic" operator="in"/>
      <feMerge><feMergeNode in="SourceGraphic"/><feMergeNode/></feMerge>
    </filter>
  </defs>
  <rect width="480" height="300" fill="{PRETO}"/>
  <g filter="url(#hnoise{seed})">
    <rect x="40" y="40" width="400" height="220" rx="28" fill="url(#ho{seed})"/>
    <rect x="40" y="40" width="400" height="220" rx="28" fill="url(#hgrid{seed})"/>
  </g>
  <rect x="40" y="40" width="400" height="220" rx="28" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="1.5"/>
  <text x="240" y="170" text-anchor="middle" font-family="Poppins,sans-serif" font-weight="900" font-size="32" fill="{PRETO}">HOLOGRAPHIC</text>
</svg>'''


print(">>> Liquid Glass Cards...")
glass_cards = {
    "glass-frosted-amber":  glass_card_frosted(AMBAR, 1),
    "glass-refraction":     glass_card_refraction(2),
    "glass-neon":           glass_card_neon(3),
    "glass-chrome":         glass_card_chrome(4),
    "glass-iridescent":     glass_card_iridescent(5),
    "glass-aurora":         glass_card_aurora(6),
    "glass-prism":          glass_card_prism(7),
    "glass-holographic":    glass_card_holographic(8),
}
for name, c in glass_cards.items():
    save(OUT_GLASS / f"{name}.svg", c)
print(f"   {len(glass_cards)} glass cards gerados")


# ══════════════════════════════════════════════════════
# GLASS BUBBLES / ORBS · 10
# ══════════════════════════════════════════════════════
def bubble_single(cx, cy, r, color, sid):
    """Bolha individual com highlight + shadow."""
    return f'''<radialGradient id="b{sid}" cx="35%" cy="30%">
      <stop offset="0" stop-color="white" stop-opacity="0.95"/>
      <stop offset="0.2" stop-color="white" stop-opacity="0.4"/>
      <stop offset="0.5" stop-color="{color}" stop-opacity="0.3"/>
      <stop offset="0.85" stop-color="{color}" stop-opacity="0.7"/>
      <stop offset="1" stop-color="{color}" stop-opacity="0.95"/>
    </radialGradient>
    <radialGradient id="bs{sid}" cx="50%" cy="50%">
      <stop offset="0" stop-color="{PRETO}" stop-opacity="0.45"/>
      <stop offset="1" stop-color="{PRETO}" stop-opacity="0"/>
    </radialGradient>'''


def bubble_cluster():
    """Cluster de bolhas em diversos tamanhos."""
    bubbles = [
        (130, 220, 60, AMBAR, 1),
        (260, 180, 80, LARANJA, 2),
        (380, 230, 50, CARMESIM, 3),
        (90, 110, 35, LARANJA, 4),
        (190, 90, 28, AMBAR, 5),
        (320, 100, 42, AMBAR, 6),
        (440, 130, 25, LARANJA, 7),
    ]
    defs = ''.join(bubble_single(b[0], b[1], b[2], b[3], b[4]) for b in bubbles)
    circles = ''
    for cx, cy, r, color, sid in bubbles:
        circles += f'<ellipse cx="{cx}" cy="{cy+r*0.95}" rx="{r*0.8}" ry="{r*0.1}" fill="url(#bs{sid})"/>'
        circles += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#b{sid})"/>'
        # Highlight extra
        circles += f'<ellipse cx="{cx-r*0.3}" cy="{cy-r*0.4}" rx="{r*0.25}" ry="{r*0.18}" fill="white" opacity="0.55"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 320" width="500" height="320"><defs>{defs}</defs><rect width="500" height="320" fill="{PRETO}"/>{circles}</svg>'


def bubble_giant(color=AMBAR, sid=99):
    """Esfera gigante de vidro com refração total."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <radialGradient id="bg{sid}" cx="35%" cy="30%">
      <stop offset="0" stop-color="white" stop-opacity="1"/>
      <stop offset="0.15" stop-color="white" stop-opacity="0.55"/>
      <stop offset="0.5" stop-color="{color}" stop-opacity="0.35"/>
      <stop offset="0.85" stop-color="{color}" stop-opacity="0.8"/>
      <stop offset="1" stop-color="{color}" stop-opacity="1"/>
    </radialGradient>
    <radialGradient id="rim{sid}" cx="50%" cy="50%">
      <stop offset="0.85" stop-color="white" stop-opacity="0"/>
      <stop offset="0.95" stop-color="white" stop-opacity="0.7"/>
      <stop offset="1" stop-color="white" stop-opacity="0"/>
    </radialGradient>
    <filter id="rb{sid}"><feGaussianBlur stdDeviation="0.8"/></filter>
    <radialGradient id="sh{sid}" cx="50%" cy="50%"><stop offset="0" stop-color="{PRETO}" stop-opacity="0.55"/><stop offset="1" stop-color="{PRETO}" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="400" height="400" fill="{PRETO}"/>
  <ellipse cx="200" cy="370" rx="150" ry="15" fill="url(#sh{sid})"/>
  <circle cx="200" cy="200" r="160" fill="url(#bg{sid})" filter="url(#rb{sid})"/>
  <circle cx="200" cy="200" r="160" fill="url(#rim{sid})"/>
  <ellipse cx="150" cy="130" rx="55" ry="32" fill="white" opacity="0.75"/>
  <ellipse cx="260" cy="280" rx="20" ry="10" fill="white" opacity="0.35"/>
</svg>'''


def bubble_droplet():
    """Gota d'água / droplet."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 400" width="300" height="400">
  <defs>
    <radialGradient id="dr" cx="40%" cy="55%">
      <stop offset="0" stop-color="white" stop-opacity="0.9"/>
      <stop offset="0.3" stop-color="{AMBAR}" stop-opacity="0.4"/>
      <stop offset="0.8" stop-color="{LARANJA}" stop-opacity="0.85"/>
      <stop offset="1" stop-color="{CARMESIM}" stop-opacity="0.95"/>
    </radialGradient>
    <radialGradient id="dsh"><stop offset="0" stop-color="{PRETO}" stop-opacity="0.5"/><stop offset="1" stop-color="{PRETO}" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="300" height="400" fill="{PRETO}"/>
  <ellipse cx="150" cy="370" rx="80" ry="10" fill="url(#dsh)"/>
  <path d="M150 60 C 90 200 60 270 60 320 a 90 60 0 0 0 180 0 c 0 -50 -30 -120 -90 -260 Z" fill="url(#dr)"/>
  <ellipse cx="115" cy="240" rx="22" ry="40" fill="white" opacity="0.6" transform="rotate(-15 115 240)"/>
  <ellipse cx="180" cy="320" rx="14" ry="8" fill="white" opacity="0.45"/>
</svg>'''


def bubble_floating_column():
    """Coluna de bolhas flutuantes."""
    bubbles_data = [
        (60,  340, 38, AMBAR),    (140, 280, 55, LARANJA),
        (60,  200, 45, CARMESIM), (160, 130, 32, AMBAR),
        (90,   60, 24, LARANJA),  (200, 230, 18, AMBAR),
        (40,  120, 14, CARMESIM),
    ]
    defs = ''
    circles = ''
    for i, (cx, cy, r, c) in enumerate(bubbles_data):
        defs += bubble_single(cx, cy, r, c, 200+i)
        circles += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#b{200+i})"/><ellipse cx="{cx-r*0.3}" cy="{cy-r*0.4}" rx="{r*0.22}" ry="{r*0.15}" fill="white" opacity="0.6"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 400" width="240" height="400"><defs>{defs}</defs><rect width="240" height="400" fill="{PRETO}"/>{circles}</svg>'


def bubble_metaball():
    """Bolhas que se fundem (metaballs) usando feGaussianBlur + feColorMatrix threshold."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 320" width="500" height="320">
  <defs>
    <filter id="meta">
      <feGaussianBlur stdDeviation="14"/>
      <feColorMatrix values="1 0 0 0 0
                              0 1 0 0 0
                              0 0 1 0 0
                              0 0 0 22 -9"/>
    </filter>
    <linearGradient id="mg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{AMBAR}"/>
      <stop offset="0.5" stop-color="{LARANJA}"/>
      <stop offset="1" stop-color="{CARMESIM}"/>
    </linearGradient>
  </defs>
  <rect width="500" height="320" fill="{PRETO}"/>
  <g filter="url(#meta)" fill="url(#mg)">
    <circle cx="150" cy="160" r="60"/>
    <circle cx="230" cy="120" r="50"/>
    <circle cx="290" cy="180" r="70"/>
    <circle cx="360" cy="140" r="45"/>
    <circle cx="100" cy="220" r="35"/>
  </g>
</svg>'''


print(">>> Glass Bubbles & Orbs...")
bubbles = {
    "bubble-cluster":          bubble_cluster(),
    "bubble-giant-amber":      bubble_giant(AMBAR, 11),
    "bubble-giant-orange":     bubble_giant(LARANJA, 12),
    "bubble-giant-crimson":    bubble_giant(CARMESIM, 13),
    "bubble-droplet":          bubble_droplet(),
    "bubble-floating-column":  bubble_floating_column(),
    "bubble-metaball":         bubble_metaball(),
    "bubble-trio-amber":       bubble_giant(AMBAR, 14).replace('width="400" height="400"', 'width="200" height="200"').replace('viewBox="0 0 400 400"', 'viewBox="0 0 400 400"'),
}
for name, c in bubbles.items():
    save(OUT_BUBBLE / f"{name}.svg", c)
print(f"   {len(bubbles)} bubbles gerados")


# ══════════════════════════════════════════════════════
# TECH ELEMENTS · 10
# ══════════════════════════════════════════════════════
def tech_circuit():
    """Circuito tech com nós e linhas."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300" width="480" height="300">
  <defs>
    <filter id="tcg"><feGaussianBlur stdDeviation="2"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="480" height="300" fill="{PRETO}"/>
  <g stroke="{AMBAR}" stroke-width="1.5" fill="none" filter="url(#tcg)">
    <path d="M40 60 H 120 V 100 H 200 V 60 H 280 V 140 H 360 V 100 H 440"/>
    <path d="M40 180 H 100 V 220 H 200 V 180 H 320 V 240 H 440"/>
    <path d="M120 100 V 180"/>
    <path d="M280 140 V 220"/>
  </g>
  <g fill="{LARANJA}">
    <circle cx="40" cy="60" r="4"/><circle cx="120" cy="100" r="5"/>
    <circle cx="200" cy="60" r="4"/><circle cx="280" cy="140" r="6"/>
    <circle cx="360" cy="100" r="4"/><circle cx="440" cy="60" r="4"/>
    <circle cx="100" cy="220" r="5"/><circle cx="200" cy="180" r="4"/>
    <circle cx="320" cy="240" r="5"/><circle cx="440" cy="240" r="4"/>
  </g>
  <g fill="{AMBAR}" opacity="0.4">
    <rect x="115" y="95" width="10" height="10"/>
    <rect x="275" y="135" width="10" height="10"/>
    <rect x="95" y="215" width="10" height="10"/>
  </g>
</svg>'''


def tech_hex_grid():
    """Grid hexagonal estilo HUD."""
    hexes = ''
    for row in range(5):
        for col in range(8):
            x = 60 + col*55 + (row%2)*27
            y = 50 + row*48
            op = 0.3 + (col+row)%3 * 0.15
            color = AMBAR if (col+row)%3 == 0 else (LARANJA if (col+row)%3 == 1 else CARMESIM)
            hexes += f'<polygon points="{x},{y-22} {x+19},{y-11} {x+19},{y+11} {x},{y+22} {x-19},{y+11} {x-19},{y-11}" fill="none" stroke="{color}" stroke-width="1" opacity="{op}"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300" width="480" height="300"><rect width="480" height="300" fill="{PRETO}"/>{hexes}</svg>'


def tech_neon_frame():
    """Frame neon com cantos chanfrados estilo cyberpunk."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300" width="480" height="300">
  <defs>
    <filter id="ng" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="480" height="300" fill="{PRETO}"/>
  <g stroke="{AMBAR}" stroke-width="2" fill="none" filter="url(#ng)">
    <path d="M50 30 H 380 L 430 80 V 270 H 100 L 50 220 Z"/>
  </g>
  <g stroke="{LARANJA}" stroke-width="1" fill="none">
    <path d="M50 30 H 380 L 430 80 V 270 H 100 L 50 220 Z"/>
  </g>
  <g fill="{AMBAR}" filter="url(#ng)">
    <circle cx="50" cy="30" r="4"/><circle cx="430" cy="270" r="4"/>
  </g>
  <text x="240" y="170" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="14" letter-spacing="4" fill="{AMBAR}" filter="url(#ng)">// iLab</text>
</svg>'''


def tech_data_flow():
    """Linhas de fluxo de dados animadas."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300" width="480" height="300">
  <rect width="480" height="300" fill="{PRETO}"/>
  <g fill="none" stroke-width="1.5">
    <path d="M0 80 Q 120 60, 240 80 T 480 80" stroke="{AMBAR}" opacity="0.7"/>
    <path d="M0 120 Q 120 100, 240 120 T 480 120" stroke="{LARANJA}" opacity="0.6"/>
    <path d="M0 160 Q 120 140, 240 160 T 480 160" stroke="{CARMESIM}" opacity="0.5"/>
    <path d="M0 200 Q 120 180, 240 200 T 480 200" stroke="{LARANJA}" opacity="0.4"/>
    <path d="M0 240 Q 120 220, 240 240 T 480 240" stroke="{AMBAR}" opacity="0.3"/>
  </g>
  <g fill="{AMBAR}">
    <circle cx="100" cy="73" r="3"/><circle cx="250" cy="80" r="4"/><circle cx="400" cy="74" r="3"/>
    <circle cx="80" cy="115" r="3"/><circle cx="260" cy="120" r="4"/>
    <circle cx="150" cy="158" r="3"/><circle cx="380" cy="158" r="3"/>
  </g>
</svg>'''


def tech_hud_corner():
    """HUD ornamento de canto."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs><filter id="hg"><feGaussianBlur stdDeviation="1.5"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
  <rect width="200" height="200" fill="{PRETO}"/>
  <g stroke="{AMBAR}" stroke-width="1.5" fill="none" filter="url(#hg)">
    <path d="M20 70 V 30 H 60"/>
    <path d="M30 50 H 50"/>
    <circle cx="30" cy="30" r="3"/>
    <path d="M80 30 H 110"/>
    <rect x="115" y="25" width="40" height="10"/>
  </g>
  <g fill="{LARANJA}">
    <rect x="118" y="28" width="8" height="4"/>
    <rect x="130" y="28" width="12" height="4"/>
    <rect x="146" y="28" width="6" height="4"/>
  </g>
  <text x="30" y="100" font-family="JetBrains Mono,monospace" font-size="9" fill="{AMBAR}" letter-spacing="1">SYS::ONLINE</text>
  <text x="30" y="115" font-family="JetBrains Mono,monospace" font-size="9" fill="{LARANJA}" letter-spacing="1">v2.6.1</text>
</svg>'''


def tech_perspective_grid():
    """Grid em perspectiva — chão estilo synthwave."""
    lines = ''
    for i in range(10):
        offset = i * 25
        lines += f'<line x1="0" y1="{150+offset}" x2="480" y2="{150+offset}" stroke="{AMBAR}" stroke-width="1" opacity="{0.8 - i*0.07}"/>'
    for i in range(-12, 13):
        x_top = 240 + i*15
        x_bot = 240 + i*60
        lines += f'<line x1="{x_top}" y1="150" x2="{x_bot}" y2="300" stroke="{LARANJA}" stroke-width="1" opacity="0.4"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300" width="480" height="300">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{PRETO}"/><stop offset="1" stop-color="{CARMESIM}"/></linearGradient>
  </defs>
  <rect width="480" height="150" fill="url(#sky)"/>
  <circle cx="240" cy="150" r="55" fill="{AMBAR}"/>
  <rect y="150" width="480" height="150" fill="{PRETO}"/>
  {lines}
</svg>'''


def tech_terminal_window():
    """Janela de terminal estilizada."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300" width="480" height="300">
  <rect width="480" height="300" fill="{PRETO}"/>
  <rect x="40" y="40" width="400" height="220" rx="8" fill="#0E0E0E" stroke="{AMBAR}" stroke-width="1"/>
  <rect x="40" y="40" width="400" height="28" rx="8" fill="#1F1F1F"/>
  <circle cx="58" cy="54" r="5" fill="{CARMESIM}"/>
  <circle cx="74" cy="54" r="5" fill="{AMBAR}"/>
  <circle cx="90" cy="54" r="5" fill="{LARANJA}"/>
  <text x="240" y="58" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="11" fill="rgba(250,243,224,0.5)">ilab@sanfran ~ %</text>
  <g font-family="JetBrains Mono,monospace" font-size="13" fill="{AMBAR}">
    <text x="60" y="100">$ npm run create-design</text>
    <text x="60" y="125" fill="{LARANJA}">✓ Loading brand assets...</text>
    <text x="60" y="148" fill="{CREME}">  → identidade.svg</text>
    <text x="60" y="168" fill="{CREME}">  → paleta.svg</text>
    <text x="60" y="188" fill="{LARANJA}">✓ Done. 166 assets ready.</text>
    <text x="60" y="220" fill="{AMBAR}">$ _<tspan opacity="0">|</tspan></text>
  </g>
</svg>'''


def tech_chip():
    """Chip / processador tech."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300" width="300" height="300">
  <defs>
    <linearGradient id="chip" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{AMBAR}"/><stop offset="1" stop-color="{LARANJA}"/></linearGradient>
    <filter id="cg"><feGaussianBlur stdDeviation="2"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="300" height="300" fill="{PRETO}"/>
  <rect x="80" y="80" width="140" height="140" rx="10" fill="none" stroke="url(#chip)" stroke-width="2"/>
  <rect x="105" y="105" width="90" height="90" rx="5" fill="rgba(244,196,48,0.08)" stroke="{LARANJA}" stroke-width="1.5"/>
  <g stroke="{AMBAR}" stroke-width="1.5" filter="url(#cg)">
    <line x1="120" y1="80" x2="120" y2="60"/>
    <line x1="150" y1="80" x2="150" y2="60"/>
    <line x1="180" y1="80" x2="180" y2="60"/>
    <line x1="120" y1="220" x2="120" y2="240"/>
    <line x1="150" y1="220" x2="150" y2="240"/>
    <line x1="180" y1="220" x2="180" y2="240"/>
    <line x1="80" y1="120" x2="60" y2="120"/>
    <line x1="80" y1="150" x2="60" y2="150"/>
    <line x1="80" y1="180" x2="60" y2="180"/>
    <line x1="220" y1="120" x2="240" y2="120"/>
    <line x1="220" y1="150" x2="240" y2="150"/>
    <line x1="220" y1="180" x2="240" y2="180"/>
  </g>
  <text x="150" y="156" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="11" font-weight="700" fill="{AMBAR}">iLab</text>
</svg>'''


def tech_radar():
    """Radar circular tech."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300" width="300" height="300">
  <defs>
    <radialGradient id="radarBg" cx="50%" cy="50%"><stop offset="0" stop-color="{AMBAR}" stop-opacity="0.15"/><stop offset="1" stop-color="{PRETO}" stop-opacity="0"/></radialGradient>
    <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{AMBAR}" stop-opacity="0"/><stop offset="1" stop-color="{AMBAR}" stop-opacity="0.6"/></linearGradient>
  </defs>
  <rect width="300" height="300" fill="{PRETO}"/>
  <circle cx="150" cy="150" r="120" fill="url(#radarBg)"/>
  <g stroke="{AMBAR}" stroke-width="1" fill="none" opacity="0.4">
    <circle cx="150" cy="150" r="40"/>
    <circle cx="150" cy="150" r="80"/>
    <circle cx="150" cy="150" r="120"/>
    <line x1="30" y1="150" x2="270" y2="150"/>
    <line x1="150" y1="30" x2="150" y2="270"/>
  </g>
  <path d="M150 150 L 270 90 A 134 134 0 0 0 270 150 Z" fill="url(#sweep)"/>
  <g fill="{LARANJA}">
    <circle cx="180" cy="120" r="3"/>
    <circle cx="100" cy="180" r="3"/>
    <circle cx="200" cy="200" r="3"/>
    <circle cx="80" cy="120" r="2"/>
  </g>
  <circle cx="150" cy="150" r="6" fill="{AMBAR}"/>
</svg>'''


def tech_binary_rain():
    """Chuva binária estilo Matrix."""
    cols = ''
    import random
    random.seed(42)
    for i in range(20):
        x = i * 25 + 5
        text = ''
        for j in range(12):
            char = '1' if random.random() > 0.5 else '0'
            op = max(0.1, 1 - j*0.08)
            text += f'<tspan x="{x}" dy="20" opacity="{op}">{char}</tspan>'
        cols += f'<text font-family="JetBrains Mono,monospace" font-size="14" fill="{AMBAR}">{text}</text>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300" width="480" height="300"><rect width="480" height="300" fill="{PRETO}"/>{cols}</svg>'


print(">>> Tech Elements...")
tech = {
    "tech-circuit":         tech_circuit(),
    "tech-hex-grid":        tech_hex_grid(),
    "tech-neon-frame":      tech_neon_frame(),
    "tech-data-flow":       tech_data_flow(),
    "tech-hud-corner":      tech_hud_corner(),
    "tech-perspective":     tech_perspective_grid(),
    "tech-terminal":        tech_terminal_window(),
    "tech-chip":            tech_chip(),
    "tech-radar":           tech_radar(),
    "tech-binary":          tech_binary_rain(),
}
for name, c in tech.items():
    save(OUT_TECH / f"{name}.svg", c)
print(f"   {len(tech)} tech elements gerados")


# ══════════════════════════════════════════════════════
# HOLOGRAPHIC SURFACES · 6
# ══════════════════════════════════════════════════════
def holo_foil(seed=1):
    """Superfície holográfica metálica/foil."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <linearGradient id="hf{seed}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{CREME}"/>
      <stop offset="0.2" stop-color="{AMBAR}"/>
      <stop offset="0.4" stop-color="{LARANJA}"/>
      <stop offset="0.6" stop-color="{CARMESIM}"/>
      <stop offset="0.8" stop-color="{LARANJA}"/>
      <stop offset="1" stop-color="{AMBAR}"/>
    </linearGradient>
    <filter id="foilNoise{seed}">
      <feTurbulence type="fractalNoise" baseFrequency="3" numOctaves="1" seed="{seed*5}"/>
      <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.12 0"/>
      <feComposite in2="SourceGraphic" operator="in"/>
      <feMerge><feMergeNode in="SourceGraphic"/><feMergeNode/></feMerge>
    </filter>
  </defs>
  <rect width="400" height="400" fill="{PRETO}"/>
  <g filter="url(#foilNoise{seed})">
    <rect x="20" y="20" width="360" height="360" rx="24" fill="url(#hf{seed})"/>
  </g>
</svg>'''


def holo_wave():
    """Onda holográfica fluida."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300" width="480" height="300">
  <defs>
    <linearGradient id="hwg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{AMBAR}"/>
      <stop offset="0.5" stop-color="{LARANJA}"/>
      <stop offset="1" stop-color="{CARMESIM}"/>
    </linearGradient>
    <filter id="bw"><feGaussianBlur stdDeviation="1"/></filter>
  </defs>
  <rect width="480" height="300" fill="{PRETO}"/>
  <g fill="none" stroke-width="2" filter="url(#bw)">
    <path d="M0 150 C 120 80, 240 220, 360 150 S 480 150, 480 150" stroke="url(#hwg)" opacity="0.95"/>
    <path d="M0 170 C 120 100, 240 240, 360 170 S 480 170, 480 170" stroke="url(#hwg)" opacity="0.75"/>
    <path d="M0 190 C 120 120, 240 260, 360 190 S 480 190, 480 190" stroke="url(#hwg)" opacity="0.55"/>
    <path d="M0 130 C 120 60, 240 200, 360 130 S 480 130, 480 130" stroke="url(#hwg)" opacity="0.75"/>
    <path d="M0 110 C 120 40, 240 180, 360 110 S 480 110, 480 110" stroke="url(#hwg)" opacity="0.55"/>
  </g>
</svg>'''


def holo_prism():
    """Prisma holográfico vertical."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <linearGradient id="hpg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{CARMESIM}"/>
      <stop offset="0.5" stop-color="{LARANJA}"/>
      <stop offset="1" stop-color="{AMBAR}"/>
    </linearGradient>
  </defs>
  <rect width="400" height="400" fill="{PRETO}"/>
  <polygon points="200,40 280,200 200,360 120,200" fill="url(#hpg)"/>
  <polygon points="200,40 280,200 200,360 120,200" fill="none" stroke="rgba(255,255,255,0.55)" stroke-width="1.5"/>
  <line x1="200" y1="40" x2="200" y2="360" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
</svg>'''


def holo_disc():
    """Disco/CD holográfico."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <radialGradient id="hd" cx="50%" cy="50%">
      <stop offset="0" stop-color="{PRETO}"/>
      <stop offset="0.2" stop-color="{CARMESIM}"/>
      <stop offset="0.4" stop-color="{LARANJA}"/>
      <stop offset="0.6" stop-color="{AMBAR}"/>
      <stop offset="0.8" stop-color="{LARANJA}"/>
      <stop offset="1" stop-color="{CARMESIM}"/>
    </radialGradient>
  </defs>
  <rect width="400" height="400" fill="{PRETO}"/>
  <circle cx="200" cy="200" r="160" fill="url(#hd)"/>
  <circle cx="200" cy="200" r="160" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
  <circle cx="200" cy="200" r="40" fill="{PRETO}"/>
  <circle cx="200" cy="200" r="12" fill="{AMBAR}"/>
</svg>'''


print(">>> Holographic Surfaces...")
holo = {
    "holo-foil-amber":  holo_foil(1),
    "holo-foil-warm":   holo_foil(2),
    "holo-wave":        holo_wave(),
    "holo-prism":       holo_prism(),
    "holo-disc":        holo_disc(),
}
for name, c in holo.items():
    save(OUT_HOLO / f"{name}.svg", c)
print(f"   {len(holo)} holographic gerados")


total = len(glass_cards) + len(bubbles) + len(tech) + len(holo)
print()
print("=" * 60)
print(f"TOTAL NOVOS ASSETS: {total}")
print(f"  Glass Cards:   {len(glass_cards)}")
print(f"  Bubbles/Orbs:  {len(bubbles)}")
print(f"  Tech Elements: {len(tech)}")
print(f"  Holographic:   {len(holo)}")
print("=" * 60)
