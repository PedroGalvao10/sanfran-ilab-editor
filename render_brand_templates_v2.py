"""
Renderiza PNG previews dos 6 templates v2 — estilos variados, mesma identidade.
540x675 (preview) · Pillow + fontes do sistema.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, math

OUT = Path(__file__).parent / "assets" / "templates"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 540, 675

YELLOW = (244, 196, 48)
ORANGE = (255, 107, 53)
RED = (196, 30, 58)
BLACK = (26, 26, 26)
BLACK_DEEP = (17, 17, 17)
WARM = (250, 243, 224)
WHITE = (245, 245, 245)


def font(weight: int, size: int):
    win = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
    cands = {
        900: ["Poppins-Black.ttf", "Poppins-ExtraBold.ttf", "arialbd.ttf"],
        700: ["Poppins-Bold.ttf", "arialbd.ttf"],
        400: ["Montserrat-Regular.ttf", "Poppins-Regular.ttf", "arial.ttf"],
    }
    for f in cands.get(weight, ["arial.ttf"]):
        p = win / f
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                pass
    return ImageFont.load_default()


def mono(weight: int, size: int):
    win = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
    name = "JetBrainsMono-Bold.ttf" if weight >= 700 else "JetBrainsMono-Regular.ttf"
    p = win / name
    if p.exists():
        return ImageFont.truetype(str(p), size)
    name = "consolab.ttf" if weight >= 700 else "consola.ttf"
    p = win / name
    if p.exists():
        return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def gradient(size, c1, c2, direction="diag"):
    """Gera gradiente em RGBA Image."""
    g = Image.new("RGB", size, c1)
    d = ImageDraw.Draw(g)
    w, h = size
    if direction == "diag":
        for i in range(w + h):
            t = i / (w + h)
            r = int(c1[0] + (c2[0] - c1[0]) * t)
            gr = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)
            d.line([(0, i), (i, 0)], fill=(r, gr, b))
    elif direction == "h":
        for x in range(w):
            t = x / w
            r = int(c1[0] + (c2[0] - c1[0]) * t)
            gr = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)
            d.line([(x, 0), (x, h)], fill=(r, gr, b))
    return g.convert("RGBA")


def paper_dots(img, color=BLACK, opacity=20):
    d = ImageDraw.Draw(img)
    for x in range(0, W, 18):
        for y in range(0, H, 18):
            d.point((x, y), fill=(*color, opacity))


def mesh_blob(img, cx, cy, r, color, alpha=200):
    """Gradiente radial soft."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for rr in range(r, 0, -2):
        a = int(alpha * (1 - rr / r) * 0.4)
        ld.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(*color, a))
    layer = layer.filter(ImageFilter.GaussianBlur(8))
    img.alpha_composite(layer)


def ilab_logo(img, x, y, ci=YELLOW, cl=ORANGE, csub=BLACK):
    d = ImageDraw.Draw(img)
    f = font(900, 14)
    d.text((x, y), "i", font=f, fill=ci)
    iw = d.textlength("i", font=f)
    d.text((x + iw, y), "Lab", font=f, fill=cl)
    d.text((x, y + 20), "SANFRAN · FD-USP", font=mono(700, 7), fill=(*csub, 140))


def handle(img, x, y, color=ORANGE):
    d = ImageDraw.Draw(img)
    d.text((x, y), "@SANFRANILAB", font=mono(700, 7), fill=color, anchor="rm")


def save(img, filename):
    img.convert("RGB").save(OUT / filename, "PNG", optimize=True)
    print(f"  OK {filename}")


# ═══════════════════════════════════════════════
# 1) CITAÇÃO — warm-white editorial
# ═══════════════════════════════════════════════
def render_citacao():
    img = Image.new("RGBA", (W, H), WARM + (255,))
    paper_dots(img)

    # Círculo grande decorativo à direita
    d = ImageDraw.Draw(img)
    # Mesh suave atrás
    mesh_blob(img, W + 20, 100, 200, ORANGE, alpha=110)
    d.ellipse([W - 140, -40, W + 220, 320], outline=ORANGE, width=1)

    d.text((40, 70), "— CITAÇÃO", font=mono(700, 9), fill=ORANGE)
    # Aspas gigantes
    d.text((20, 100), '"', font=font(900, 180), fill=ORANGE)

    # Citação
    d.text((40, 280), "A inovação no", font=font(700, 32), fill=BLACK)
    d.text((40, 322), "Direito começa", font=font(700, 32), fill=BLACK)
    d.text((40, 364), "por dentro das", font=font(700, 32), fill=ORANGE)
    d.text((40, 406), "salas de aula.", font=font(700, 32), fill=ORANGE)

    # Autoria
    # avatar circle
    d.ellipse([40, 480, 105, 545], fill=YELLOW)
    d.ellipse([45, 485, 100, 540], fill=WARM)
    d.text((72, 513), "A", font=font(900, 22), fill=(*BLACK, 100), anchor="mm")
    d.text((125, 495), "NOME DO AUTOR", font=font(900, 16), fill=BLACK)
    d.text((125, 514), "Cargo · Instituição", font=font(400, 11), fill=(*BLACK, 180))
    d.line([(125, 530), (220, 530)], fill=ORANGE, width=2)

    ilab_logo(img, 40, H - 45, ci=YELLOW, cl=ORANGE, csub=BLACK)
    handle(img, W - 40, H - 30, color=ORANGE)
    save(img, "ilab-citacao.png")


# ═══════════════════════════════════════════════
# 2) PESQUISA — gradient bg + cards
# ═══════════════════════════════════════════════
def render_pesquisa():
    img = gradient((W, H), YELLOW, ORANGE, direction="diag")
    # Mesh holo overlays
    mesh_blob(img, 100, 50, 280, (255, 183, 168), alpha=180)
    mesh_blob(img, W - 80, H - 100, 240, (255, 213, 128), alpha=180)
    d = ImageDraw.Draw(img)

    d.text((40, 70), "PESQUISA · RELATÓRIO 2026", font=mono(700, 9), fill=BLACK)

    d.text((40, 130), "Direito", font=font(900, 56), fill=BLACK)
    d.text((40, 190), "+ IA", font=font(900, 56), fill=BLACK)
    d.text((40, 250), "no Brasil", font=font(900, 56), fill=WARM)

    # Card 1 (warm-white)
    d.rounded_rectangle([40, 330, 255, 425], radius=10, fill=WARM)
    d.text((52, 340), "87%", font=font(900, 48), fill=ORANGE)
    d.line([(52, 388), (78, 388)], fill=BLACK, width=2)
    d.text((52, 395), "dos escritórios", font=font(700, 10), fill=BLACK)
    d.text((52, 408), "usam IA em 2026", font=font(700, 10), fill=BLACK)

    # Card 2 (dark)
    d.rounded_rectangle([265, 330, 480, 425], radius=10, fill=BLACK)
    d.text((277, 340), "3.2x", font=font(900, 48), fill=YELLOW)
    d.line([(277, 388), (303, 388)], fill=ORANGE, width=2)
    d.text((277, 395), "aumento na", font=font(700, 10), fill=WARM)
    d.text((277, 408), "produtividade", font=font(700, 10), fill=WARM)

    d.text((40, 460), "Estudo conduzido pelo SanFran iLab", font=font(700, 13), fill=BLACK)
    d.text((40, 480), "com 1.200 escritórios em todo o país.", font=font(400, 11), fill=(*BLACK, 200))

    # CTA pretinha
    d.rounded_rectangle([40, 520, 290, 562], radius=21, fill=BLACK)
    d.text((165, 541), "BAIXAR RELATÓRIO ↓", font=mono(700, 10), fill=YELLOW, anchor="mm")

    # Detalhe geométrico canto
    d.ellipse([W - 120, H - 110, W - 40, H - 30], outline=BLACK, width=2)
    d.ellipse([W - 100, H - 90, W - 60, H - 50], outline=BLACK, width=2)
    d.ellipse([W - 86, H - 76, W - 74, H - 64], fill=BLACK)

    ilab_logo(img, 40, H - 45, ci=BLACK, cl=BLACK, csub=BLACK)
    handle(img, W - 40, H - 30, color=BLACK)
    save(img, "ilab-pesquisa.png")


# ═══════════════════════════════════════════════
# 3) MANIFESTO — split duotone
# ═══════════════════════════════════════════════
def render_manifesto():
    img = Image.new("RGBA", (W, H), WARM + (255,))
    d = ImageDraw.Draw(img)
    # Polígono preto diagonal
    d.polygon([(0, H), (W, H), (W, 260), (0, 360)], fill=BLACK)
    d.line([(0, 360), (W, 260)], fill=ORANGE, width=3)

    d.text((40, 70), "— MANIFESTO 2026", font=mono(700, 9), fill=ORANGE)

    d.text((40, 130), "No que", font=font(900, 60), fill=BLACK)
    d.text((40, 195), "acreditamos.", font=font(900, 60), fill=ORANGE)
    d.line([(40, 250), (170, 250)], fill=ORANGE, width=2)

    # Bottom: princípios
    items = [
        ("01", "Direito sem fronteiras com tecnologia."),
        ("02", "Estudantes como agentes de mudança."),
        ("03", "Pesquisa aplicada ao mundo real."),
        ("04", "Conhecimento aberto e colaborativo."),
    ]
    y = 400
    for num, txt in items:
        d.text((40, y), num, font=font(900, 24), fill=YELLOW)
        d.text((90, y - 4), "PRINCÍPIO", font=mono(700, 7), fill=ORANGE)
        d.text((90, y + 12), txt, font=font(700, 13), fill=WARM)
        y += 50

    ilab_logo(img, 40, H - 45, ci=YELLOW, cl=ORANGE, csub=WARM)
    handle(img, W - 40, H - 30, color=YELLOW)
    save(img, "ilab-manifesto.png")


# ═══════════════════════════════════════════════
# 4) EDITAL — bold red-orange gradient
# ═══════════════════════════════════════════════
def render_edital():
    img = gradient((W, H), ORANGE, RED, direction="diag")
    mesh_blob(img, 100, 60, 260, (255, 183, 168), alpha=160)
    d = ImageDraw.Draw(img)

    # Tarja
    d.rectangle([0, 0, W, 38], fill=BLACK)
    d.text((40, 20), "INSCRIÇÕES ABERTAS · 2026", font=mono(700, 10), fill=YELLOW, anchor="lm")

    # Estrela decorativa
    cx, cy = W - 80, 100
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        r = 28 if i % 2 == 0 else 12
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=(*WARM, 140))

    # Título
    d.text((40, 130), "Faça parte", font=font(900, 56), fill=WARM)
    d.text((40, 195), "do", font=font(900, 56), fill=WARM)
    d.text((40, 260), "iLab 2026.", font=font(900, 56), fill=BLACK)

    # Card branco
    d.rounded_rectangle([40, 330, 500, 530], radius=14, fill=WARM)
    d.rectangle([40, 330, 100, 336], fill=ORANGE)
    d.text((58, 360), "Prazo · 15 de janeiro", font=font(900, 18), fill=BLACK)
    d.text((58, 384), "23:59 · BRASÍLIA", font=mono(700, 9), fill=ORANGE)
    d.line([(58, 408), (482, 408)], fill=(*ORANGE, 110), width=1)
    d.text((58, 425), "Para quem", font=font(900, 13), fill=BLACK)
    d.text((58, 442), "Estudantes da FD-USP", font=font(400, 11), fill=(*BLACK, 200))
    d.text((58, 472), "40 vagas", font=font(900, 30), fill=ORANGE)
    d.text((220, 482), "Pesquisa + Projetos", font=font(700, 10), fill=BLACK)
    d.text((220, 498), "aplicados em legaltech", font=font(700, 10), fill=BLACK)

    # CTA
    d.rounded_rectangle([40, 550, 360, 596], radius=23, fill=BLACK)
    d.text((200, 573), "INSCREVA-SE — LINK NA BIO →", font=mono(700, 11), fill=YELLOW, anchor="mm")

    ilab_logo(img, 40, H - 45, ci=BLACK, cl=BLACK, csub=BLACK)
    handle(img, W - 40, H - 30, color=BLACK)
    save(img, "ilab-edital.png")


# ═══════════════════════════════════════════════
# 5) MARCO — dark + holographic explosion
# ═══════════════════════════════════════════════
def render_marco():
    img = Image.new("RGBA", (W, H), BLACK_DEEP + (255,))
    # Mesh quente
    mesh_blob(img, W // 2, H // 2 - 50, 320, YELLOW, alpha=200)
    mesh_blob(img, W // 2 + 100, H // 2 + 40, 220, ORANGE, alpha=220)
    d = ImageDraw.Draw(img)

    # Anéis concêntricos
    for r in [160, 120, 80]:
        d.ellipse([W // 2 - r, H // 2 - 40 - r, W // 2 + r, H // 2 - 40 + r], outline=(*ORANGE, 80), width=1)

    d.text((40, 70), "— MARCO HISTÓRICO", font=mono(700, 9), fill=YELLOW)

    # Número gigante — render two colors faking gradient
    f_huge = font(900, 220)
    txt = "500"
    tw = d.textlength(txt, font=f_huge)
    d.text((W // 2, 300), txt, font=f_huge, fill=ORANGE, anchor="mm")

    # Linha
    d.line([(W // 2 - 90, 410), (W // 2 + 90, 410)], fill=YELLOW, width=2)

    d.text((W // 2, 445), "estudantes formados", font=font(900, 28), fill=WARM, anchor="mm")
    d.text((W // 2, 475), "desde 2020", font=font(700, 16), fill=ORANGE, anchor="mm")

    # Stats grid centralizado
    base_y = 540
    cols = [
        ("PROJETOS", "42+"),
        ("PARCEIROS", "28"),
        ("PUBLICAÇÕES", "15"),
    ]
    col_w = 130
    start_x = (W - col_w * 3) // 2
    for i, (label, val) in enumerate(cols):
        x = start_x + i * col_w + col_w // 2
        d.text((x, base_y), label, font=mono(700, 8), fill=YELLOW, anchor="mm")
        d.text((x, base_y + 30), val, font=font(900, 28), fill=WARM, anchor="mm")

    ilab_logo(img, 40, H - 45, ci=YELLOW, cl=ORANGE, csub=WARM)
    handle(img, W - 40, H - 30, color=YELLOW)
    save(img, "ilab-marco.png")


# ═══════════════════════════════════════════════
# 6) EDUCA — academic two-column
# ═══════════════════════════════════════════════
def render_educa():
    img = Image.new("RGBA", (W, H), WARM + (255,))
    paper_dots(img)
    d = ImageDraw.Draw(img)

    # Barra lateral gradient
    bar = gradient((7, H), YELLOW, ORANGE, direction="diag")
    img.alpha_composite(bar, (0, 0))

    d.text((40, 70), "— CONCEITO · LEGALTECH", font=mono(700, 9), fill=ORANGE)
    d.text((40, 130), "Legal", font=font(900, 64), fill=BLACK)
    d.text((40, 200), "Design.", font=font(900, 64), fill=ORANGE)

    d.text((40, 272), "SUBSTANTIVO · MÉTODO · M.", font=mono(700, 8), fill=(*BLACK, 150))

    # Definição
    d.line([(40, 310), (75, 310)], fill=ORANGE, width=3)
    d.text((40, 322), "Aplicação de princípios do", font=font(700, 15), fill=BLACK)
    d.text((40, 344), "design ao Direito para", font=font(700, 15), fill=BLACK)
    d.text((40, 366), "tornar documentos jurídicos", font=font(700, 15), fill=ORANGE)
    d.text((40, 388), "claros e acessíveis.", font=font(700, 15), fill=ORANGE)

    # 3 cards pilares
    d.text((40, 430), "3 PILARES", font=mono(700, 9), fill=ORANGE)
    cards = [
        (YELLOW, "01", "Empatia com", "o leitor"),
        (ORANGE, "02", "Visualização", "da informação"),
        (RED, "03", "Iteração e", "teste contínuo"),
    ]
    card_w = 155
    for i, (col, num, l1, l2) in enumerate(cards):
        x = 40 + i * (card_w + 8)
        d.rounded_rectangle([x, 450, x + card_w, 560], radius=10, fill=BLACK)
        d.text((x + 12, 460), num, font=font(900, 22), fill=col)
        d.text((x + 12, 500), l1, font=font(700, 12), fill=WARM)
        d.text((x + 12, 518), l2, font=font(700, 12), fill=WARM)

    d.text((40, H - 80), "Fonte: Margaret Hagan · Stanford Legal Design Lab.", font=mono(400, 7), fill=(*BLACK, 130))

    ilab_logo(img, 40, H - 45, ci=YELLOW, cl=ORANGE, csub=BLACK)
    handle(img, W - 40, H - 30, color=ORANGE)
    save(img, "ilab-educa.png")


if __name__ == "__main__":
    print("Renderizando 6 PNGs (estilos variados)...")
    render_citacao()
    render_pesquisa()
    render_manifesto()
    render_edital()
    render_marco()
    render_educa()
