"""
Renderiza previews PNG dos 4 templates de evento (sem cairo).
Usa Pillow para desenhar a mesma composição em raster — fontes do sistema/Google.
Saída: assets/templates/*.png (540x675 preview)
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
import os

OUT = Path(__file__).parent / "assets" / "templates"
OUT.mkdir(parents=True, exist_ok=True)

# Tamanho preview
W, H = 540, 675

BG = (15, 15, 15)
ORANGE = (255, 107, 53)
YELLOW = (244, 196, 48)
WHITE = (250, 250, 250)
GRAY = (136, 136, 136)
DARK_ACCENT = (42, 26, 10)


# ─────────────────────────────────────────
# Carregar fontes (Poppins do Windows)
# ─────────────────────────────────────────
def load_font(weight: int, size: int):
    candidates = []
    win_fonts = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
    name_map = {
        900: ["Poppins-Black.ttf", "Poppins-ExtraBold.ttf"],
        700: ["Poppins-Bold.ttf", "Poppins-SemiBold.ttf"],
        400: ["Poppins-Regular.ttf"],
    }
    for fname in name_map.get(weight, ["Poppins-Regular.ttf"]):
        candidates.append(win_fonts / fname)
    # JetBrains Mono / fallback
    candidates += [
        win_fonts / "JetBrainsMono-Bold.ttf",
        win_fonts / "consolab.ttf",
        win_fonts / "arialbd.ttf",
        win_fonts / "arial.ttf",
    ]
    for p in candidates:
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                pass
    return ImageFont.load_default()


def load_mono(weight: int, size: int):
    win_fonts = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
    candidates = [
        win_fonts / ("JetBrainsMono-Bold.ttf" if weight >= 700 else "JetBrainsMono-Regular.ttf"),
        win_fonts / "consolab.ttf",
        win_fonts / "consola.ttf",
        win_fonts / "arial.ttf",
    ]
    for p in candidates:
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                pass
    return ImageFont.load_default()


# ─────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────
def draw_background(draw, img):
    # Fundo dark com gradiente radial sutil
    img.paste(BG, (0, 0, W, H))
    # Vinheta orange no canto inferior
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    for r in range(W, 0, -8):
        alpha = int(40 * (1 - r / W))
        odraw.ellipse([W // 2 - r, H - r // 2, W // 2 + r, H + r // 2], fill=(255, 107, 53, alpha))
    img.alpha_composite(overlay) if img.mode == "RGBA" else img.paste(overlay, (0, 0), overlay)
    # Padrão de pontos
    d = ImageDraw.Draw(img)
    for x in range(0, W, 18):
        for y in range(0, H, 18):
            d.point((x, y), fill=(255, 107, 53, 40))


def draw_globe(draw, cx, cy, r, alpha=90):
    """Globe wireframe decorativo."""
    color = (255, 107, 53, alpha)
    # círculo principal
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=1)
    # elipses (paralelos)
    for ry in [r * 0.3, r * 0.6]:
        draw.ellipse([cx - r, cy - ry, cx + r, cy + ry], outline=color, width=1)
    # elipses (meridianos)
    for rx in [r * 0.3, r * 0.6]:
        draw.ellipse([cx - rx, cy - r, cx + rx, cy + r], outline=color, width=1)
    # linhas eixos
    draw.line([(cx - r, cy), (cx + r, cy)], fill=color, width=1)
    draw.line([(cx, cy - r), (cx, cy + r)], fill=color, width=1)


def draw_photo_placeholder(img):
    """Oval com foto silhueta placeholder."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # Oval mais à direita
    cx, cy = W - 140, 380
    rx, ry = 180, 250
    od.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(58, 58, 58, 180))
    # Silhueta interna
    od.ellipse([cx - 60, cy - 90, cx + 60, cy + 30], fill=(35, 35, 35, 200))  # cabeça
    od.ellipse([cx - 120, cy + 30, cx + 120, cy + 280], fill=(35, 35, 35, 200))  # corpo
    img.alpha_composite(overlay)
    # Label
    d = ImageDraw.Draw(img)
    f = load_mono(700, 9)
    d.text((cx, cy + 5), "[ FOTO DO ]", font=f, fill=GRAY, anchor="mm")
    d.text((cx, cy + 20), "[ PALESTRANTE ]", font=f, fill=GRAY, anchor="mm")


def draw_title(img, line1: str, line2: str, tagline: list):
    d = ImageDraw.Draw(img)
    f_title = load_font(900, 70)
    d.text((40, 50), line1, font=f_title, fill=WHITE)
    d.text((40, 125), line2, font=f_title, fill=ORANGE)
    # Tagline à direita
    f_tag = load_font(700, 11)
    for i, line in enumerate(tagline):
        is_orange = line.startswith("#")
        txt = line.lstrip("#")
        color = ORANGE if is_orange else WHITE
        d.text((W - 40, 65 + i * 16), txt, font=f_tag, fill=color, anchor="rm")


def draw_meta(img, date_text, time_text, location_text, y=240):
    d = ImageDraw.Draw(img)
    # Calendário icon
    d.rounded_rectangle([40, y + 3, 68, y + 31], radius=4, outline=ORANGE, width=2)
    d.line([(40, y + 11), (68, y + 11)], fill=ORANGE, width=2)
    d.rectangle([47, y, 50, y + 6], fill=ORANGE)
    d.rectangle([58, y, 61, y + 6], fill=ORANGE)
    # Date
    f_date = load_font(900, 22)
    f_time = load_mono(700, 11)
    d.text((80, y + 16), date_text, font=f_date, fill=WHITE, anchor="lm")
    d.text((80, y + 38), time_text, font=f_time, fill=WHITE, anchor="lm")
    # Divisória
    d.line([(40, y + 60), (190, y + 60)], fill=ORANGE, width=1)
    # Pin
    y2 = y + 76
    # gota pin (path approximation)
    d.ellipse([46, y2, 64, y2 + 18], outline=ORANGE, width=2)
    d.polygon([(46, y2 + 10), (64, y2 + 10), (55, y2 + 28)], outline=ORANGE)
    d.ellipse([51, y2 + 4, 59, y2 + 12], fill=ORANGE)
    d.text((80, y2 + 14), location_text.upper(), font=load_font(900, 16), fill=WHITE, anchor="lm")


def draw_speaker(img, first, last, company, role_lines, y=420):
    d = ImageDraw.Draw(img)
    f_name = load_font(900, 28)
    d.text((40, y), first.upper(), font=f_name, fill=WHITE)
    d.text((40, y + 30), last.upper(), font=f_name, fill=ORANGE)
    # Company logo placeholder
    y2 = y + 68
    d.ellipse([42, y2, 70, y2 + 28], outline=ORANGE, width=2)
    d.ellipse([50, y2 + 8, 62, y2 + 20], outline=YELLOW, width=2)
    d.text((80, y2 + 14), company.upper(), font=load_font(900, 18), fill=WHITE, anchor="lm")
    # Barra cargo
    d.line([(40, y + 110), (40, y + 152)], fill=ORANGE, width=2)
    f_role = load_mono(400, 9)
    for i, line in enumerate(role_lines):
        d.text((50, y + 116 + i * 14), line.upper(), font=f_role, fill=WHITE)


def draw_footer(img):
    d = ImageDraw.Draw(img)
    f_logo = load_font(900, 14)
    f_sub = load_mono(700, 7)
    # logo
    d.text((40, H - 45), "i", font=f_logo, fill=YELLOW)
    iw = d.textlength("i", font=f_logo)
    d.text((40 + iw, H - 45), "Lab", font=f_logo, fill=ORANGE)
    d.text((40, H - 25), "SANFRAN · FD-USP", font=f_sub, fill=(180, 180, 180))
    # handle
    d.text((W - 40, H - 30), "@SANFRANILAB", font=f_sub, fill=ORANGE, anchor="rm")


# ─────────────────────────────────────────
# Templates
# ─────────────────────────────────────────
def render_template(name, line1, line2, tagline, date, time, location, sname, slast, company, role, filename):
    img = Image.new("RGBA", (W, H), BG + (255,))
    draw_background(None, img)
    # Globe corners
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    draw_globe(od, W - 60, 60, 140, alpha=120)
    draw_globe(od, 60, H - 60, 140, alpha=100)
    img.alpha_composite(overlay)
    # Photo
    draw_photo_placeholder(img)
    # Content
    draw_title(img, line1, line2, tagline)
    draw_meta(img, date, time, location)
    draw_speaker(img, sname, slast, company, role)
    draw_footer(img)
    # Save
    img.convert("RGB").save(OUT / filename, "PNG", optimize=True)
    print(f"  OK {filename}")


if __name__ == "__main__":
    print("Renderizando previews PNG (540x675)...")
    render_template(
        "Conecta",
        "iLab", "conecta",
        ["IDEIAS QUE", "#CONECTAM,", "FUTUROS QUE", "#TRANSFORMAM."],
        "DD.MM", "HH:MMPM", "Sanfran iLab",
        "Nome", "Sobrenome", "Empresa",
        ["Cargo e função do", "palestrante na empresa"],
        "ilab-conecta-palestrante.png",
    )
    render_template(
        "Talks",
        "iLab", "talks",
        ["BATE-PAPO", "#ABERTO", "SOBRE DIREITO", "#E INOVAÇÃO."],
        "DD.MM", "HH:MMPM", "Sanfran iLab",
        "Nome", "Sobrenome", "Empresa",
        ["Cargo · Empresa", "Tema da conversa"],
        "ilab-talks-batepapo.png",
    )
    render_template(
        "Workshop",
        "iLab", "workshop",
        ["MÃO NA MASSA.", "#RESULTADO", "REAL EM", "#90 MIN."],
        "DD.MM", "HH:MMPM", "Sanfran iLab",
        "Facilitador", "Sobrenome", "Empresa",
        ["Workshop prático", "Vagas limitadas"],
        "ilab-workshop.png",
    )
    render_template(
        "Pitch",
        "iLab", "pitch",
        ["APRESENTE", "#SUA IDEIA.", "CONECTE COM", "#INVESTIDORES."],
        "DD.MM", "HH:MMPM", "Sanfran iLab",
        "Pitch", "Day", "iLab",
        ["Apresentação de startups", "5 min por time"],
        "ilab-pitch-day.png",
    )
    print(f"\nTotal: 4 PNGs em {OUT}")
