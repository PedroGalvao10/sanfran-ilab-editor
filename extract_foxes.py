"""Extract foxes from PDF: render each page as PNG, then extract embedded images.
Saves results to assets/ folder.
"""
import fitz
import os
import re

PDF = r"C:\Users\soare\Downloads\Mascot_Expression_Guide_Law_Innovation (2).pdf"
OUT = r"C:\Users\soare\.gemini\antigravity\scratch\sanfran-ilab-brand\assets\foxes"
os.makedirs(OUT, exist_ok=True)

doc = fitz.open(PDF)
print(f"pages: {len(doc)}")

manifest = []

for i, page in enumerate(doc):
    text = page.get_text().strip()
    print(f"\n=== PAGE {i+1} ===")
    print(text[:400])

    # render full page at 300 DPI
    pix = page.get_pixmap(dpi=300, alpha=True)
    page_png = os.path.join(OUT, f"page_{i+1:02d}_full.png")
    pix.save(page_png)
    print(f"  saved page: {page_png}")

    # extract embedded images
    for j, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        try:
            base = doc.extract_image(xref)
            ext = base["ext"]
            data = base["image"]
            img_path = os.path.join(OUT, f"page_{i+1:02d}_img_{j+1}.{ext}")
            with open(img_path, "wb") as f:
                f.write(data)
            print(f"  saved image: {img_path} ({len(data)//1024} KB, ext={ext})")
            manifest.append({"page": i+1, "img": img_path, "text": text[:200]})
        except Exception as e:
            print(f"  err: {e}")

print(f"\nDONE. {len(manifest)} images extracted to {OUT}")
