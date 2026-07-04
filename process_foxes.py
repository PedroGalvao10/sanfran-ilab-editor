"""Process all 40 fox quadrants — IMPROVED crop:
1. Crop top 76% of each quadrant (removes bottom label text)
2. Make white background transparent
3. Auto-crop to content (tight fit around the fox only)
"""
import os
import io
import json
from PIL import Image

QUADRANTS = r"C:\Users\soare\.gemini\antigravity\scratch\sanfran-ilab-brand\assets\foxes_quadrants"
OUT = r"C:\Users\soare\.gemini\antigravity\scratch\sanfran-ilab-brand\assets\lex"
os.makedirs(OUT, exist_ok=True)

MAPPING = {
    (2, "q1"): ("Acolhimento", "acolhimento", "empatia"),
    (2, "q2"): ("Olá", "ola", "empatia"),
    (2, "q3"): ("Aprovação", "aprovacao", "empatia"),
    (2, "q4"): ("Gratidão", "gratidao", "empatia"),
    (3, "q1"): ("Ideia Brilhante", "ideia-brilhante", "intelecto"),
    (3, "q2"): ("Empolgação", "empolgacao", "empatia"),
    (3, "q3"): ("Surpresa", "surpresa", "empatia"),
    (3, "q4"): ("Euforia", "euforia", "empatia"),
    (4, "q1"): ("Estudioso", "estudioso", "intelecto"),
    (4, "q2"): ("Analítico", "analitico", "intelecto"),
    (4, "q3"): ("Anotações", "anotacoes", "intelecto"),
    (4, "q4"): ("Investigação", "investigacao", "intelecto"),
    (5, "q1"): ("Construtor", "construtor", "execucao"),
    (5, "q2"): ("Mão na Massa", "mao-na-massa", "execucao"),
    (5, "q3"): ("Multitarefa", "multitarefa", "execucao"),
    (5, "q4"): ("Prototipando", "prototipando", "execucao"),
    (6, "q1"): ("Confusão Técnica", "confusao-tecnica", "execucao"),
    (6, "q2"): ("Perdido", "perdido", "execucao"),
    (6, "q3"): ("Erro 404", "erro-404", "execucao"),
    (6, "q4"): ("Bloqueio", "bloqueio", "execucao"),
    (7, "q1"): ("Dor de Cabeça", "dor-de-cabeca", "empatia"),
    (7, "q2"): ("Exaustão", "exaustao", "empatia"),
    (7, "q3"): ("Tristeza", "tristeza", "empatia"),
    (7, "q4"): ("Frustração", "frustracao", "empatia"),
    (8, "q1"): ("Astúcia", "astucia", "astucia"),
    (8, "q2"): ("Negócio Fechado", "negocio-fechado", "astucia"),
    (8, "q3"): ("Segredo", "segredo", "astucia"),
    (8, "q4"): ("Confiança", "confianca", "astucia"),
    (9, "q1"): ("Veredito", "veredito", "astucia"),
    (9, "q2"): ("Equilíbrio", "equilibrio", "astucia"),
    (9, "q3"): ("Objeção", "objecao", "astucia"),
    (9, "q4"): ("Solenidade", "solenidade", "astucia"),
    (10, "q1"): ("Didática", "didatica", "intelecto"),
    (10, "q2"): ("Apresentação", "apresentacao", "intelecto"),
    (10, "q3"): ("Discurso", "discurso", "intelecto"),
    (10, "q4"): ("Mentoria", "mentoria", "intelecto"),
    (11, "q1"): ("Conectado", "conectado", "execucao"),
    (11, "q2"): ("Pausa", "pausa", "empatia"),
    (11, "q3"): ("Pesquisa", "pesquisa", "intelecto"),
    (11, "q4"): ("Mobile", "mobile", "execucao"),
}

QUAD_NAMES = {
    "q1": "q1_topleft",
    "q2": "q2_topright",
    "q3": "q3_bottomleft",
    "q4": "q4_bottomright",
}

def crop_label_off(img, label_ratio=0.78):
    """Crop top X% of the image to remove the bottom label."""
    w, h = img.size
    return img.crop((0, 0, w, int(h * label_ratio)))

def remove_white_bg(img, threshold=235):
    """Convert near-white pixels to transparent using fast numpy if available."""
    img = img.convert("RGBA")
    try:
        import numpy as np
        arr = np.array(img)
        # mask: pixels where R,G,B all >= threshold
        mask = (arr[..., 0] >= threshold) & (arr[..., 1] >= threshold) & (arr[..., 2] >= threshold)
        arr[mask] = [255, 255, 255, 0]
        return Image.fromarray(arr, "RGBA")
    except ImportError:
        data = list(img.getdata())
        new_data = [(255,255,255,0) if (r>=threshold and g>=threshold and b>=threshold) else (r,g,b,a) for r,g,b,a in data]
        img.putdata(new_data)
        return img

def crop_to_content(img, padding=12):
    bbox = img.getbbox()
    if bbox is None:
        return img
    left, top, right, bottom = bbox
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(img.width, right + padding)
    bottom = min(img.height, bottom + padding)
    return img.crop((left, top, right, bottom))

manifest = []
for (page, quad), (label, slug, category) in sorted(MAPPING.items()):
    src = os.path.join(QUADRANTS, f"page_{page:02d}_{QUAD_NAMES[quad]}.png")
    if not os.path.exists(src):
        print(f"MISSING: {src}")
        continue

    img = Image.open(src)
    # STEP 1: cut off bottom label
    img = crop_label_off(img, label_ratio=0.78)
    # STEP 2: white -> transparent
    img = remove_white_bg(img, threshold=235)
    # STEP 3: tight bbox
    img = crop_to_content(img, padding=8)

    out_path = os.path.join(OUT, f"{slug}.png")
    img.save(out_path, "PNG", optimize=True)
    manifest.append({
        "label": label, "slug": slug, "category": category,
        "file": f"assets/lex/{slug}.png", "size": img.size
    })
    print(f"{category:10s} | {label:20s} | {img.size}")

with open(os.path.join(OUT, "_manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"\n{len(manifest)} expressions processed.")
