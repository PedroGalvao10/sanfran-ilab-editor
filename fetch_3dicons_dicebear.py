"""
1) 3dicons.co — repo público com 3D icons (estilo 'dynamic clay', 'fluency', etc.)
2) DiceBear API — gera avatares estilo Notion (notionists style)
"""
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent
OUT_3DICONS = ROOT / "assets" / "3dicons"
OUT_AVATARS = ROOT / "assets" / "avatars"
OUT_3DICONS.mkdir(parents=True, exist_ok=True)
OUT_AVATARS.mkdir(parents=True, exist_ok=True)

def fetch(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
            dest.write_bytes(data)
            return len(data)
    except Exception as e:
        return None

# ══════════════════════════════════════════════
# 3dicons.co (estilo dynamic clay - bem orgânico, parece argila)
# Repo: github.com/3dicons/3dicons-png
# ══════════════════════════════════════════════
ICONS_3D = [
    "light-bulb", "books", "graduation-cap", "rocket", "brain",
    "gear", "trophy", "briefcase", "handshake", "globe",
    "target", "chart-up", "book-open", "lock", "key",
    "magnifier", "hourglass", "memo", "scroll", "scale",
    "crystal-ball", "sparkles", "telescope", "gem", "crown",
    "newspaper", "coin", "floppy-disk", "pushpin", "megaphone",
    "computer", "phone", "robot", "calendar", "printer"
]

STYLES = ["dynamic-clay", "dynamic-color", "front-color"]

print(">>> 3dicons.co (tentando vários estilos)\n")
icons_ok = []
for icon in ICONS_3D[:25]:  # limitar a 25 para não estourar
    got = False
    for style in STYLES:
        # jsDelivr CDN do repo público
        url = f"https://cdn.jsdelivr.net/gh/3dicons/3dicons-png@v1.0.0/icons/{style}/{icon}.png"
        dest = OUT_3DICONS / f"{icon}-{style}.png"
        size = fetch(url, dest)
        if size and size > 5000:  # PNG real tem pelo menos 5KB
            icons_ok.append((icon, style))
            print(f"  {icon:18s} OK ({style})")
            got = True
            break
        elif dest.exists():
            dest.unlink()
    if not got:
        print(f"  {icon:18s} -- nenhum estilo disponível")

print(f"\n3dicons: {len(icons_ok)} baixados")


# ══════════════════════════════════════════════
# DiceBear Notionists (avatares estilo Notion)
# API pública e gratuita
# ══════════════════════════════════════════════
print("\n>>> DiceBear Notionists Avatars (estilo Notion)\n")

# Seeds + papéis para diversidade
PERSONAS = [
    ("alex",     "Alex"),
    ("maria",    "Maria"),
    ("joao",     "João"),
    ("camila",   "Camila"),
    ("rafael",   "Rafael"),
    ("beatriz",  "Beatriz"),
    ("lucas",    "Lucas"),
    ("ana",      "Ana"),
    ("pedro",    "Pedro"),
    ("fernanda", "Fernanda"),
    ("gustavo",  "Gustavo"),
    ("juliana",  "Juliana"),
]

avatars_ok = []
for seed, name in PERSONAS:
    # backgroundColor=fff8e1 (creme da marca) — combina com paleta
    url = (
        f"https://api.dicebear.com/7.x/notionists/svg"
        f"?seed={seed}&backgroundColor=fff8e1,fef3c7,ffe4b5"
        f"&radius=50"
    )
    dest = OUT_AVATARS / f"{seed}.svg"
    size = fetch(url, dest)
    if size and size > 500:
        avatars_ok.append((seed, name))
        print(f"  notionists-{seed:12s} OK ({size//1024}KB)")
    else:
        print(f"  notionists-{seed:12s} ERRO")

# Adicionar variação: big-smile (estilo personagem mais lúdico)
print()
for seed, name in PERSONAS[:6]:
    url = (
        f"https://api.dicebear.com/7.x/big-smile/svg"
        f"?seed={seed}&backgroundColor=fff8e1,fef3c7"
        f"&accessoriesProbability=50"
    )
    dest = OUT_AVATARS / f"smile-{seed}.svg"
    size = fetch(url, dest)
    if size and size > 500:
        avatars_ok.append((f"smile-{seed}", f"{name} 😀"))
        print(f"  big-smile-{seed:12s} OK ({size//1024}KB)")

print(f"\nAvatars DiceBear: {len(avatars_ok)} baixados")

print()
print("=" * 60)
print(f"TOTAL: {len(icons_ok)} 3dicons + {len(avatars_ok)} avatars")
print("=" * 60)
