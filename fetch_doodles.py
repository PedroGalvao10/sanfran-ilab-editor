"""Tentar fontes alternativas de ilustrações: Open Doodles + Streamline + Iconscout."""
import urllib.request, urllib.parse
from pathlib import Path

AMBAR = "#F4C430"
ROOT = Path(__file__).parent
OUT = ROOT / "assets" / "illustrations"
OUT.mkdir(parents=True, exist_ok=True)

def fetch(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read()
            dest.write_bytes(data)
            return len(data)
    except Exception as e:
        return None

# ─────────────────────────────────────────────
# OPEN DOODLES (Pablo Stanley, CC0)
# https://github.com/timqian/open-doodles
# ─────────────────────────────────────────────
DOODLES = [
    "doogie", "sitting", "messy", "running", "loving", "lifting", "groovy",
    "victoryboard", "selfie", "rocket", "jumpingjoy", "iceCreamCone", "floating",
    "exercising", "dancing", "boxer", "balloon", "zombing", "unboxing", "swing"
]

BASES = [
    "https://raw.githubusercontent.com/timqian/open-doodles/master/public/svg",
    "https://raw.githubusercontent.com/timqian/open-doodles/master/svg",
    "https://raw.githubusercontent.com/pablostanley/opendoodles/main/svg",
]

print(">>> Open Doodles (CC0)...")
doodles_ok = []
for slug in DOODLES:
    got = False
    for base in BASES:
        url = f"{base}/{slug}.svg"
        dest = OUT / f"doodle-{slug}.svg"
        size = fetch(url, dest)
        if size and size > 500:
            # Recolorir
            try:
                c = dest.read_text(encoding="utf-8")
                # Open Doodles costuma usar #fff/#000 — pintar o "principal" não trivial
                # Apenas marcar para integração
                print(f"  doodle-{slug:18s} OK ({size//1024}KB) via {base.split('/')[-1]}")
                doodles_ok.append(slug)
                got = True
                break
            except: pass
    if not got:
        if (OUT / f"doodle-{slug}.svg").exists():
            (OUT / f"doodle-{slug}.svg").unlink()

print(f"   {len(doodles_ok)}/{len(DOODLES)} doodles\n")

# ─────────────────────────────────────────────
# Streamline 3D Emoji (alternative)
# https://github.com/streamlinehq/streamline-emojis
# ─────────────────────────────────────────────
print(">>> Tentando Streamline 3D Emoji repo público...")
STREAM_TRIES = [
    ("light-bulb", "stream-lightbulb"),
    ("graduation-cap", "stream-graduation"),
    ("rocket", "stream-rocket"),
]
for orig, dest_name in STREAM_TRIES:
    url = f"https://raw.githubusercontent.com/streamlinehq/streamline-emojis/main/3d/{orig}.svg"
    dest = OUT / f"{dest_name}.svg"
    size = fetch(url, dest)
    if size and size > 500:
        print(f"  {dest_name:25s} OK")
    elif (OUT / f"{dest_name}.svg").exists():
        (OUT / f"{dest_name}.svg").unlink()

print()
print("=" * 60)
print("Listagem final em assets/illustrations/")
for f in sorted(OUT.glob("*.svg")):
    print(f"  {f.name}  ({f.stat().st_size//1024}KB)")
print("=" * 60)
