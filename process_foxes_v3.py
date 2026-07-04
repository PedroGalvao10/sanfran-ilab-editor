"""V3: flood-fill background removal.
Só remove o branco conectado às bordas. Olho/dente/pelo interno ficam.
"""
import os, json
from PIL import Image
import numpy as np
from scipy import ndimage

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
QUAD_NAMES = {"q1":"q1_topleft","q2":"q2_topright","q3":"q3_bottomleft","q4":"q4_bottomright"}

def crop_label_off(img, ratio=0.78):
    w, h = img.size
    return img.crop((0, 0, w, int(h * ratio)))

def remove_bg_floodfill(img, threshold=230):
    """Flood-fill: só branco conectado às bordas vira transparente."""
    img = img.convert("RGBA")
    arr = np.array(img)
    r, g, b = arr[...,0], arr[...,1], arr[...,2]
    # mask de pixels "brancos" (background candidatos)
    white_mask = (r >= threshold) & (g >= threshold) & (b >= threshold)
    # label connected components de pixels brancos
    labeled, n = ndimage.label(white_mask)
    if n == 0:
        return img
    # quais labels tocam a borda?
    border_labels = set()
    border_labels.update(np.unique(labeled[0,  :]).tolist())
    border_labels.update(np.unique(labeled[-1, :]).tolist())
    border_labels.update(np.unique(labeled[:,  0]).tolist())
    border_labels.update(np.unique(labeled[:, -1]).tolist())
    border_labels.discard(0)
    # mask final: pixels brancos cujo label toca a borda
    bg_mask = np.isin(labeled, list(border_labels))
    arr[bg_mask] = [255, 255, 255, 0]
    return Image.fromarray(arr, "RGBA")

def crop_to_content(img, padding=10):
    bbox = img.getbbox()
    if not bbox:
        return img
    l, t, r, b = bbox
    return img.crop((max(0,l-padding), max(0,t-padding),
                     min(img.width, r+padding), min(img.height, b+padding)))

manifest = []
for (page, quad), (label, slug, category) in sorted(MAPPING.items()):
    src = os.path.join(QUADRANTS, f"page_{page:02d}_{QUAD_NAMES[quad]}.png")
    if not os.path.exists(src):
        print(f"MISSING: {src}")
        continue
    img = Image.open(src)
    img = crop_label_off(img, 0.78)
    img = remove_bg_floodfill(img, threshold=230)
    img = crop_to_content(img, 10)
    out_path = os.path.join(OUT, f"{slug}.png")
    img.save(out_path, "PNG", optimize=True)
    manifest.append({"label":label, "slug":slug, "category":category,
                     "file":f"assets/lex/{slug}.png", "size":img.size})
    print(f"{category:10s} | {label:20s} | {img.size}")

with open(os.path.join(OUT, "_manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print(f"\n{len(manifest)} processadas com flood-fill.")
