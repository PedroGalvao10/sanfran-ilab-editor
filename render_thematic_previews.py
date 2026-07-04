"""
Renderiza previews PNG dos 6 templates temáticos via Pillow.
Composição reproduzida em raster com fontes do sistema (Poppins/JetBrains).

Saída: assets/templates/*.png (540x675)
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os

OUT = Path(__file__).parent / "assets" / "templates"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 540, 675

BG = (15, 15, 15)
ORANGE = (255, 107, 53)
YELLOW = (244, 196, 48)
WHITE = (250, 250, 250)
GRAY = (136, 136, 136)


def load_font(weight: int, size: int):
    win_fonts = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
    name_map = {
        900: ["Poppins-Black.ttf", "Poppins-ExtraBold.ttf"],
        700: ["Poppins-Bold.ttf", "Poppins-SemiBold.ttf"],
        400: ["Poppins-Regular.ttf", "Montserrat-Regular.ttf"],
    }
    for fname in name_map.get(weight, ["Poppins-Regular.ttf"]):
        p = win_fonts / fname
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                pass
    for fb in ["arialbd.ttf", "arial.ttf"]:
        p = win_fonts / fb
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def load_mono(weight: int, size: int):
    win_fonts = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
    cands = [
        "JetBrainsMono-Bold.ttf" if weight >= 700 else "JetBrainsMono-Regular.ttf",
        "consolab.ttf" if weight >= 700 else "consola.ttf",
        "arialbd.ttf" if weight >= 700 else "arial.ttf",
    ]
    for fname in cands:
        p = win_fonts / fname
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                pass
    return ImageFont.load_default()


def base_background(globe_position="default"):
    img = Image.new("RGBA", (W, H), BG + (255,))
    # Padrão de pontos
    d = ImageDraw.Draw(img)
    for x in range(0, W, 18):
        for y in range(0, H, 18):
            d.point((x, y), fill=(255, 107, 53, 38))
    # Vinheta laranja inferior
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for r in range(W, 0, -8):
        alpha = int(40 * (1 - r / W))
        od.ellipse([W // 2 - r, H - r // 2, W // 2 + r, H + r // 2], fill=(255, 107, 53, alpha))
    img.alpha_composite(overlay)
    # Globos
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    if globe_position == "default":
        draw_globe(gd, W - 60, 60, 140)
        draw_globe(gd, 60, H - 60, 140)
    elif globe_position == "center":
        draw_globe(gd, W // 2, H // 2, 220, alpha=70)
    elif globe_position == "top":
        draw_globe(gd, 30, 30, 130)
        draw_globe(gd, W - 30, 30, 130)
    img.alpha_composite(g)
    return img


def draw_globe(d, cx, cy, r, alpha=100):
    color = (255, 107, 53, alpha)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=1)
    for ry in [r * 0.3, r * 0.6]:
        d.ellipse([cx - r, cy - ry, cx + r, cy + ry], outline=color, width=1)
    for rx in [r * 0.3, r * 0.6]:
        d.ellipse([cx - rx, cy - r, cx + rx, cy + r], outline=color, width=1)
    d.line([(cx - r, cy), (cx + r, cy)], fill=color, width=1)
    d.line([(cx, cy - r), (cx, cy + r)], fill=color, width=1)


def draw_section_tag(img, label, y=60):
    d = ImageDraw.Draw(img)
    f = load_mono(700, 8)
    bw, bh = 120, 22
    x = 40
    d.rounded_rectangle([x, y - bh, x + bw, y], radius=11, outline=ORANGE, width=2)
    d.text((x + bw // 2, y - bh // 2), label, font=f, fill=ORANGE, anchor="mm")


def draw_footer(img):
    d = ImageDraw.Draw(img)
    f_logo = load_font(900, 14)
    f_sub = load_mono(700, 7)
    d.text((40, H - 45), "i", font=f_logo, fill=YELLOW)
    iw = d.textlength("i", font=f_logo)
    d.text((40 + iw, H - 45), "Lab", font=f_logo, fill=ORANGE)
    d.text((40, H - 25), "SANFRAN · FD-USP", font=f_sub, fill=(180, 180, 180))
    d.text((W - 40, H - 30), "@SANFRANILAB", font=f_sub, fill=ORANGE, anchor="rm")


def save(img, filename):
    img.convert("RGB").save(OUT / filename, "PNG", optimize=True)
    print(f"  OK {filename}")


# ─────────────────────────────────────────
# 1) CITAÇÃO
# ─────────────────────────────────────────
def render_citacao():
    img = base_background("center")
    d = ImageDraw.Draw(img)
    draw_section_tag(img, "CITAÇÃO")
    # Aspas
    d.text((30, 90), '"', font=load_font(900, 200), fill=ORANGE + (220,))
    # Citação
    d.text((40, 260), "A inovação no", font=load_font(700, 32), fill=WHITE)
    d.text((40, 300), "Direito começa", font=load_font(700, 32), fill=WHITE)
    d.text((40, 340), "por dentro", font=load_font(700, 32), fill=ORANGE)
    d.text((40, 380), "das salas de aula.", font=load_font(700, 32), fill=ORANGE)
    # Linha + autoria
    d.line([(40, 460), (110, 460)], fill=ORANGE, width=2)
    d.text((40, 490), "NOME DO AUTOR", font=load_font(900, 18), fill=WHITE)
    d.text((40, 518), "CARGO · INSTITUIÇÃO", font=load_mono(400, 10), fill=(220, 220, 220))
    draw_footer(img)
    save(img, "ilab-citacao.png")


# ─────────────────────────────────────────
# 2) PESQUISA
# ─────────────────────────────────────────
def render_pesquisa():
    img = base_background("top")
    d = ImageDraw.Draw(img)
    draw_section_tag(img, "NOVA PESQUISA")
    # Título
    d.text((40, 120), "Direito", font=load_font(900, 50), fill=WHITE)
    d.text((40, 175), "+ IA", font=load_font(900, 50), fill=ORANGE)
    d.text((40, 230), "no Brasil", font=load_font(900, 50), fill=WHITE)
    d.text((40, 285), "RELATÓRIO ANUAL · 2026", font=load_mono(700, 9), fill=ORANGE)
    # Cards
    # Card 1
    d.rounded_rectangle([40, 320, 245, 410], radius=8, outline=ORANGE, width=2)
    d.text((54, 332), "87%", font=load_font(900, 42), fill=ORANGE)
    d.text((54, 380), "DOS ESCRITÓRIOS", font=load_mono(700, 8), fill=WHITE)
    d.text((54, 392), "USAM IA EM 2026", font=load_mono(700, 8), fill=WHITE)
    # Card 2
    d.rounded_rectangle([260, 320, 465, 410], radius=8, outline=YELLOW, width=2)
    d.text((274, 332), "3.2x", font=load_font(900, 42), fill=YELLOW)
    d.text((274, 380), "AUMENTO DE", font=load_mono(700, 8), fill=WHITE)
    d.text((274, 392), "PRODUTIVIDADE", font=load_mono(700, 8), fill=WHITE)
    # Autoria
    d.text((40, 450), "Estudo conduzido por:", font=load_font(700, 14), fill=WHITE)
    d.text((40, 475), "SanFran iLab", font=load_font(900, 22), fill=ORANGE)
    d.text((40, 510), "Faculdade de Direito da USP · 2026", font=load_mono(400, 10), fill=(200, 200, 200))
    # CTA
    d.rounded_rectangle([40, 550, 280, 590], radius=20, fill=ORANGE)
    d.text((160, 570), "BAIXE O RELATÓRIO ↓", font=load_mono(700, 10), fill=BG, anchor="mm")
    draw_footer(img)
    save(img, "ilab-pesquisa.png")


# ─────────────────────────────────────────
# 3) MANIFESTO
# ─────────────────────────────────────────
def render_manifesto():
    img = base_background("default")
    d = ImageDraw.Draw(img)
    draw_section_tag(img, "MANIFESTO")
    d.text((40, 110), "No que", font=load_font(900, 64), fill=WHITE)
    d.text((40, 178), "acreditamos.", font=load_font(900, 64), fill=ORANGE)
    # Princípios
    items = [
        ("01.", "Direito sem fronteiras com tecnologia."),
        ("02.", "Estudantes como agentes de mudança."),
        ("03.", "Pesquisa aplicada ao mundo real."),
        ("04.", "Diálogo entre Academia e mercado."),
        ("05.", "Conhecimento aberto e colaborativo."),
    ]
    y = 285
    d.line([(40, y - 8), (500, y - 8)], fill=ORANGE + (110,), width=1)
    for num, txt in items:
        d.text((40, y), num, font=load_font(900, 18), fill=ORANGE)
        d.text((90, y), txt, font=load_font(700, 14), fill=WHITE)
        y += 50
        d.line([(40, y - 8), (500, y - 8)], fill=ORANGE + (110,), width=1)
    draw_footer(img)
    save(img, "ilab-manifesto.png")


# ─────────────────────────────────────────
# 4) EDITAL
# ─────────────────────────────────────────
def render_edital():
    img = base_background("default")
    d = ImageDraw.Draw(img)
    draw_section_tag(img, "INSCRIÇÕES ABERTAS")
    # Título
    d.text((40, 110), "Faça", font=load_font(900, 56), fill=WHITE)
    d.text((40, 172), "parte do", font=load_font(900, 56), fill=WHITE)
    d.text((40, 234), "iLab 2026.", font=load_font(900, 56), fill=ORANGE)
    # Calendário block
    y = 320
    d.rounded_rectangle([40, y + 3, 70, y + 31], radius=4, outline=ORANGE, width=2)
    d.line([(40, y + 11), (70, y + 11)], fill=ORANGE, width=2)
    d.rectangle([47, y, 50, y + 6], fill=ORANGE)
    d.rectangle([60, y, 63, y + 6], fill=ORANGE)
    d.text((84, y + 8), "PRAZO · 15.JAN", font=load_font(900, 18), fill=WHITE)
    d.text((84, y + 32), "23:59 · BRASÍLIA", font=load_mono(700, 9), fill=(200, 200, 200))
    # Pessoa
    y = 390
    d.ellipse([40, y - 4, 64, y + 18], outline=ORANGE, width=2)
    d.arc([34, y + 10, 70, y + 50], 180, 360, fill=ORANGE, width=2)
    d.text((84, y), "PARA QUEM", font=load_font(900, 15), fill=WHITE)
    d.text((84, y + 22), "Estudantes da FD-USP", font=load_mono(400, 10), fill=(220, 220, 220))
    # Vagas
    d.text((40, 460), "40 VAGAS", font=load_font(900, 32), fill=ORANGE)
    d.text((220, 470), "PESQUISA + PROJETOS", font=load_mono(700, 9), fill=WHITE)
    d.text((220, 484), "APLICADOS", font=load_mono(700, 9), fill=WHITE)
    # CTA
    d.rounded_rectangle([40, 530, 320, 580], radius=25, fill=ORANGE)
    d.text((180, 555), "INSCREVA-SE → BIO", font=load_mono(700, 11), fill=BG, anchor="mm")
    draw_footer(img)
    save(img, "ilab-edital.png")


# ─────────────────────────────────────────
# 5) MARCO
# ─────────────────────────────────────────
def render_marco():
    img = base_background("default")
    d = ImageDraw.Draw(img)
    draw_section_tag(img, "MARCO 2026")
    # Número gigante com gradiente fake (degradê laranja-amarelo via 2 cores)
    d.text((30, 90), "500", font=load_font(900, 220), fill=ORANGE)
    # Linha
    d.line([(40, 320), (170, 320)], fill=ORANGE, width=3)
    # Descrição
    d.text((40, 350), "estudantes", font=load_font(900, 30), fill=WHITE)
    d.text((40, 388), "já passaram", font=load_font(900, 30), fill=WHITE)
    d.text((40, 426), "pelo iLab.", font=load_font(900, 30), fill=ORANGE)
    # Contexto
    d.text((40, 478), "DESDE 2020", font=load_mono(700, 9), fill=ORANGE)
    d.text((40, 500), "Construindo uma nova geração de juristas", font=load_font(400, 11), fill=(230, 230, 230))
    d.text((40, 516), "capazes de transformar o Direito brasileiro.", font=load_font(400, 11), fill=(230, 230, 230))
    # Stats
    y = 560
    d.text((40, y), "PROJETOS", font=load_mono(700, 8), fill=ORANGE)
    d.text((40, y + 16), "42+", font=load_font(900, 22), fill=WHITE)
    d.text((180, y), "PARCEIROS", font=load_mono(700, 8), fill=ORANGE)
    d.text((180, y + 16), "28", font=load_font(900, 22), fill=WHITE)
    d.text((320, y), "PUBLICAÇÕES", font=load_mono(700, 8), fill=ORANGE)
    d.text((320, y + 16), "15", font=load_font(900, 22), fill=WHITE)
    draw_footer(img)
    save(img, "ilab-marco.png")


# ─────────────────────────────────────────
# 6) EDUCA
# ─────────────────────────────────────────
def render_educa():
    img = base_background("default")
    d = ImageDraw.Draw(img)
    draw_section_tag(img, "CONCEITO")
    # Conceito gigante
    d.text((40, 100), "Legal", font=load_font(900, 78), fill=WHITE)
    d.text((40, 184), "Design", font=load_font(900, 78), fill=ORANGE)
    d.text((40, 270), "SUBSTANTIVO · MÉTODO", font=load_mono(700, 9), fill=(150, 150, 150))
    # Definição
    d.line([(40, 305), (75, 305)], fill=ORANGE, width=3)
    d.text((40, 320), "Aplicação de princípios", font=load_font(700, 15), fill=WHITE)
    d.text((40, 342), "do design ao Direito para", font=load_font(700, 15), fill=WHITE)
    d.text((40, 364), "tornar documentos jurídicos", font=load_font(700, 15), fill=ORANGE)
    d.text((40, 386), "mais claros e acessíveis.", font=load_font(700, 15), fill=ORANGE)
    # Pilares
    d.text((40, 432), "3 PILARES", font=load_mono(700, 9), fill=ORANGE)
    items = [
        ("1", "Empatia com o leitor"),
        ("2", "Visualização da informação"),
        ("3", "Iteração e teste"),
    ]
    y = 458
    for n, txt in items:
        d.ellipse([40, y, 64, y + 24], outline=ORANGE, width=2)
        d.text((52, y + 12), n, font=load_font(900, 10), fill=ORANGE, anchor="mm")
        d.text((74, y + 12), txt, font=load_font(700, 14), fill=WHITE, anchor="lm")
        y += 36
    # Fonte
    d.text((40, H - 90), "Fonte: Margaret Hagan, Stanford Legal Design Lab.", font=load_mono(400, 8), fill=(140, 140, 140))
    draw_footer(img)
    save(img, "ilab-educa.png")


if __name__ == "__main__":
    print("Renderizando 6 PNGs temáticos (540x675)...")
    render_citacao()
    render_pesquisa()
    render_manifesto()
    render_edital()
    render_marco()
    render_educa()
    print(f"\nTotal: 6 PNGs em {OUT}")
