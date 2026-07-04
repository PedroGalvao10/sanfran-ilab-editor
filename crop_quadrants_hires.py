"""Crop pages 2-11 do PDF de expressões em 600 DPI para máxima qualidade.
Substitui os arquivos em assets/foxes_quadrants/.
"""
import fitz
import os
from PIL import Image
import io

PDF = r"C:\Users\soare\Downloads\Mascot_Expression_Guide_Law_Innovation (2).pdf"
OUT = r"C:\Users\soare\.gemini\antigravity\scratch\sanfran-ilab-brand\assets\foxes_quadrants"
os.makedirs(OUT, exist_ok=True)

DPI = 600  # dobro da resolução anterior (300 DPI)

doc = fitz.open(PDF)
total = 0

# Pages 2-11 (1-indexed) → fitz usa 0-indexed → range(1, 11)
for page_num in range(1, 11):
    page = doc[page_num]

    # Renderizar em 600 DPI para máxima nitidez
    pix = page.get_pixmap(dpi=DPI, alpha=False)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    w, h = img.size
    mid_x, mid_y = w // 2, h // 2

    quads = [
        ("q1_topleft",     (0,     0,     mid_x, mid_y)),
        ("q2_topright",    (mid_x, 0,     w,     mid_y)),
        ("q3_bottomleft",  (0,     mid_y, mid_x, h)),
        ("q4_bottomright", (mid_x, mid_y, w,     h)),
    ]

    for name, box in quads:
        crop = img.crop(box)
        out_path = os.path.join(OUT, f"page_{page_num+1:02d}_{name}.png")
        # compress_level=1 = mínimo de compressão = arquivo maior, acesso mais rápido
        crop.save(out_path, "PNG", compress_level=1)
        print(f"  {out_path}  {crop.size}")
        total += 1

print(f"\nDONE — {total} quadrants em {DPI} DPI salvos em {OUT}")
