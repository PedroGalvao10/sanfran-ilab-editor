"""
Baixa ícones profissionais da Iconify API (Lucide + Phosphor).
Substitui os ícones gerados por código por SVGs feitos por humanos (padrão da indústria).
Aplica a paleta SanFran iLab nos 4 estilos:
  outline → Lucide (stroke #1A1A1A)
  solid   → Phosphor-fill (fill #FF6B35)
  duotone → Phosphor-duotone (fill #FF6B35 + #F4C430)
  gradient→ Lucide com gradient stroke
"""
import os
import re
import shutil
import urllib.request
from pathlib import Path

AMBAR    = "#F4C430"
LARANJA  = "#FF6B35"
CARMESIM = "#C41E3A"
PRETO    = "#1A1A1A"

ROOT = Path(__file__).parent
OUT = ROOT / "assets" / "icons_v2"

# Limpar a pasta primeiro
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True, exist_ok=True)

# Mapeamento: nosso nome → ícone Iconify (formato pack:name)
ICON_MAP = {
    # Jurídico
    "scales":      ("lucide:scale",          "ph:scales-fill",          "ph:scales-duotone"),
    "gavel":       ("lucide:gavel",          "ph:gavel-fill",           "ph:gavel-duotone"),
    "contract":    ("lucide:scroll-text",    "ph:scroll-fill",          "ph:scroll-duotone"),
    "courthouse":  ("lucide:landmark",       "ph:bank-fill",            "ph:bank-duotone"),
    # Tech
    "cpu":         ("lucide:cpu",            "ph:cpu-fill",             "ph:cpu-duotone"),
    "code":        ("lucide:code-2",         "ph:code-fill",            "ph:code-duotone"),
    "cloud":       ("lucide:cloud",          "ph:cloud-fill",           "ph:cloud-duotone"),
    "api":         ("lucide:webhook",        "ph:plugs-fill",           "ph:plugs-duotone"),
    # Inovação
    "lightbulb":   ("lucide:lightbulb",      "ph:lightbulb-filament-fill",  "ph:lightbulb-filament-duotone"),
    "rocket":      ("lucide:rocket",         "ph:rocket-launch-fill",   "ph:rocket-launch-duotone"),
    "gear-arrow":  ("lucide:settings-2",     "ph:gear-six-fill",        "ph:gear-six-duotone"),
    "blueprint":   ("lucide:layout-template","ph:blueprint-fill",       "ph:blueprint-duotone"),
    # Educação
    "book":        ("lucide:book-open",      "ph:book-open-fill",       "ph:book-open-duotone"),
    "mortarboard": ("lucide:graduation-cap", "ph:graduation-cap-fill",  "ph:graduation-cap-duotone"),
    "chalkboard":  ("lucide:presentation",   "ph:chalkboard-fill",      "ph:chalkboard-duotone"),
    "certificate": ("lucide:award",          "ph:certificate-fill",     "ph:certificate-duotone"),
    # Comunidade
    "handshake":   ("lucide:handshake",      "ph:handshake-fill",       "ph:handshake-duotone"),
    "network":     ("lucide:share-2",        "ph:share-network-fill",   "ph:share-network-duotone"),
    "megaphone":   ("lucide:megaphone",      "ph:megaphone-fill",       "ph:megaphone-duotone"),
    "globe":       ("lucide:globe-2",        "ph:globe-fill",           "ph:globe-duotone"),
    # Mídia
    "camera":      ("lucide:camera",         "ph:camera-fill",          "ph:camera-duotone"),
    "microphone":  ("lucide:mic",            "ph:microphone-fill",      "ph:microphone-duotone"),
    "broadcast":   ("lucide:radio-tower",    "ph:broadcast-fill",       "ph:broadcast-duotone"),
    "play-circle": ("lucide:play-circle",    "ph:play-circle-fill",     "ph:play-circle-duotone"),
    # Workflow
    "kanban":      ("lucide:kanban",         "ph:kanban-fill",          "ph:kanban-duotone"),
    "checklist":   ("lucide:list-checks",    "ph:check-square-fill",    "ph:check-square-duotone"),
    "calendar":    ("lucide:calendar-days",  "ph:calendar-dots-fill",   "ph:calendar-dots-duotone"),
    "sync":        ("lucide:refresh-ccw",    "ph:arrows-clockwise-fill","ph:arrows-clockwise-duotone"),
    # Dados
    "chart-bar":   ("lucide:bar-chart-3",    "ph:chart-bar-fill",       "ph:chart-bar-duotone"),
    "chart-line":  ("lucide:line-chart",     "ph:chart-line-up-fill",   "ph:chart-line-up-duotone"),
    "target":      ("lucide:target",         "ph:target-fill",          "ph:target-duotone"),
    "pulse":       ("lucide:activity",       "ph:pulse-fill",           "ph:pulse-duotone"),
}


def fetch(iconify_id):
    """Baixa SVG da Iconify API com User-Agent."""
    url = f"https://api.iconify.design/{iconify_id}.svg"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (SanFran iLab Brand Tool)"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8")
            if "<svg" not in content:
                return None
            return content
    except Exception as e:
        print(f"   ERRO {iconify_id}: {e}")
        return None


def apply_color(svg, color, ensure_viewbox=True):
    """Substitui currentColor por uma cor específica."""
    # Iconify retorna SVG com fill/stroke=currentColor
    svg = svg.replace("currentColor", color)
    # Garantir viewBox 24x24 se ausente
    if 'viewBox' not in svg and ensure_viewbox:
        svg = svg.replace('<svg', '<svg viewBox="0 0 24 24"', 1)
    return svg


def make_outline(svg):
    """Estilo outline: stroke preto."""
    return apply_color(svg, PRETO)


def make_solid(svg):
    """Estilo solid: fill laranja."""
    return apply_color(svg, LARANJA)


def make_duotone(svg):
    """Estilo duotone: cores Phosphor (já vem com 2 opacidades)."""
    # Phosphor duotone tem fill com opacidade .2 + fill principal
    # currentColor já está nos 2 níveis — só substituir
    return apply_color(svg, LARANJA)


def make_gradient(outline_svg, sid):
    """Adiciona um gradient ao SVG outline (âmbar → laranja)."""
    # Inserir <defs> com gradient + substituir cor pelo url(#grad)
    gradient_def = (
        f'<defs><linearGradient id="g{sid}" x1="0%" y1="0%" x2="100%" y2="100%">'
        f'<stop offset="0%" stop-color="{AMBAR}"/>'
        f'<stop offset="100%" stop-color="{LARANJA}"/>'
        f'</linearGradient></defs>'
    )
    # Inserir defs logo após <svg ...>
    svg = re.sub(r'(<svg[^>]*>)', r'\1' + gradient_def, outline_svg, count=1)
    # Substituir #1A1A1A pelo gradient url
    svg = svg.replace(PRETO, f"url(#g{sid})")
    return svg


print(">>> Baixando ícones profissionais da Iconify API...")
print(f"    {len(ICON_MAP)} ícones × 4 estilos = {len(ICON_MAP)*4} SVGs\n")

success = 0
errors = []
for idx, (our_name, (outline_id, solid_id, duotone_id)) in enumerate(ICON_MAP.items(), 1):
    print(f"  [{idx:2d}/32] {our_name}", end=" ")

    # 1) OUTLINE — Lucide
    raw_outline = fetch(outline_id)
    if raw_outline:
        (OUT / f"{our_name}-outline.svg").write_text(make_outline(raw_outline), encoding="utf-8")
        success += 1
        print("[ok]outline", end="")
    else:
        errors.append((our_name, "outline", outline_id))
        print("[X]outline", end="")

    # 2) SOLID — Phosphor fill
    raw_solid = fetch(solid_id)
    if raw_solid:
        (OUT / f"{our_name}-solid.svg").write_text(make_solid(raw_solid), encoding="utf-8")
        success += 1
        print(" [ok]solid", end="")
    else:
        errors.append((our_name, "solid", solid_id))
        print(" [X]solid", end="")

    # 3) DUOTONE — Phosphor duotone
    raw_duotone = fetch(duotone_id)
    if raw_duotone:
        (OUT / f"{our_name}-duotone.svg").write_text(make_duotone(raw_duotone), encoding="utf-8")
        success += 1
        print(" [ok]duotone", end="")
    else:
        errors.append((our_name, "duotone", duotone_id))
        print(" [X]duotone", end="")

    # 4) GRADIENT — Lucide com gradient âmbar→laranja
    if raw_outline:
        gradient_svg = make_gradient(make_outline(raw_outline), idx)
        (OUT / f"{our_name}-gradient.svg").write_text(gradient_svg, encoding="utf-8")
        success += 1
        print(" [ok]gradient", end="")
    else:
        errors.append((our_name, "gradient", outline_id))
        print(" [X]gradient", end="")

    print()

print()
print(f"=" * 60)
print(f"OK: {success}/{len(ICON_MAP)*4} SVGs baixados")
if errors:
    print(f"ERROS ({len(errors)}):")
    for n, s, i in errors:
        print(f"   {n}/{s} -> {i}")
print(f"=" * 60)
