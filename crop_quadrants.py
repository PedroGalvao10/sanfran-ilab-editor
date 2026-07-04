"""Crop pages 2-11 of the mascot PDF into 4 quadrants each.
Each quadrant contains 1 fox + label below.
"""
import fitz
import os
from PIL import Image
import io

PDF = r"C:\Users\soare\Downloads\Mascot_Expression_Guide_Law_Innovation (2).pdf"
OUT = r"C:\Users\soare\.gemini\antigravity\scratch\sanfran-ilab-brand\assets\foxes_quadrants"
os.makedirs(OUT, exist_ok=True)

doc = fitz.open(PDF)

# Pages 2-11 (1-indexed) → fitz uses 0-indexed
for page_num in range(1, 11):  # pages 2 through 11
    page = doc[page_num]
    # render high res
    pix = page.get_pixmap(dpi=300, alpha=False)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    w, h = img.size
    mid_x, mid_y = w // 2, h // 2

    quads = [
        ("q1_topleft", (0, 0, mid_x, mid_y)),
        ("q2_topright", (mid_x, 0, w, mid_y)),
        ("q3_bottomleft", (0, mid_y, mid_x, h)),
        ("q4_bottomright", (mid_x, mid_y, w, h)),
    ]
    for name, box in quads:
        crop = img.crop(box)
        out_path = os.path.join(OUT, f"page_{page_num+1:02d}_{name}.png")
        crop.save(out_path, "PNG", optimize=True)
        print(f"saved {out_path}  size={crop.size}")

print("\nDONE")
