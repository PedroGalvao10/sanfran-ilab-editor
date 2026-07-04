"""Build the new section 04 HTML from manifest."""
import json
import os

MANIFEST = r"C:\Users\soare\.gemini\antigravity\scratch\sanfran-ilab-brand\assets\lex\_manifest.json"
OUT = r"C:\Users\soare\.gemini\antigravity\scratch\sanfran-ilab-brand\_section_04.html"

with open(MANIFEST, encoding="utf-8") as f:
    items = json.load(f)

CATEGORIES = {
    "empatia":   {"name": "Empatia",   "desc": "Emoções sociais e conexão humana — onde a marca conversa com sentimentos.",     "color": "#FF6B35", "icon": "💛"},
    "intelecto": {"name": "Intelecto", "desc": "Pensar, estudar, ensinar — a Lex como mente analítica e didática.",             "color": "#F4C430", "icon": "🧠"},
    "execucao":  {"name": "Execução",  "desc": "Mão na massa, construir, fazer acontecer — o lado tech e operacional.",          "color": "#2E7D32", "icon": "⚙️"},
    "astucia":   {"name": "Astúcia",   "desc": "Estratégia, lei, negociação — a Lex jurídica e ardilosa, do Largo São Francisco.","color": "#C41E3A", "icon": "⚖️"},
}

by_cat = {k: [] for k in CATEGORIES}
for it in items:
    by_cat[it["category"]].append(it)

# build HTML
parts = []
parts.append('<!-- 04 SISTEMA LEX — Galeria completa de expressões -->')
parts.append('<section id="lex">')
parts.append('  <div class="section-label">04 — Sistema Lex</div>')
parts.append('  <h2>Galeria de Expressões</h2>')
parts.append('  <p class="section-desc">40 variações de comportamento e emoção do mascote Lex, organizadas em 4 categorias. Cada raposa é um estado comunicativo. Clique em qualquer uma para baixar em PNG transparente.</p>')

for cat_key, cat in CATEGORIES.items():
    expressions = by_cat[cat_key]
    parts.append(f'')
    parts.append(f'  <!-- CATEGORIA: {cat["name"]} -->')
    parts.append(f'  <div style="margin-top:40px;">')
    parts.append(f'    <div style="display:flex;align-items:baseline;gap:14px;margin-bottom:18px;padding-bottom:14px;border-bottom:2px solid {cat["color"]};">')
    parts.append(f'      <span style="font-size:22px;">{cat["icon"]}</span>')
    parts.append(f'      <h3 style="font-family:\'Poppins\',sans-serif;font-weight:900;font-size:24px;color:{cat["color"]};margin:0;">{cat["name"]}</h3>')
    parts.append(f'      <span style="font-family:\'JetBrains Mono\',monospace;font-size:11px;letter-spacing:1.5px;color:var(--gray-text);text-transform:uppercase;">{len(expressions)} expressões</span>')
    parts.append(f'    </div>')
    parts.append(f'    <p style="font-size:13px;color:var(--gray-text);margin-bottom:18px;max-width:680px;line-height:1.6;">{cat["desc"]}</p>')
    parts.append(f'    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:14px;">')
    for ex in expressions:
        parts.append(f'      <div style="background:white;border:1px solid var(--gray);border-radius:12px;overflow:hidden;transition:transform .25s ease,box-shadow .25s ease;">')
        parts.append(f'        <div style="aspect-ratio:1/1;background:#FAFAFA;display:flex;align-items:center;justify-content:center;padding:8px;">')
        parts.append(f'          <img src="{ex["file"]}" alt="Lex — {ex["label"]}" data-asset="lex-{ex["slug"]}" style="max-width:100%;max-height:100%;object-fit:contain;cursor:pointer;">')
        parts.append(f'        </div>')
        parts.append(f'        <div style="padding:10px 14px 12px;border-top:1px solid var(--gray);">')
        parts.append(f'          <div style="font-family:\'Poppins\',sans-serif;font-weight:700;font-size:13px;color:var(--black);line-height:1.2;">{ex["label"]}</div>')
        parts.append(f'        </div>')
        parts.append(f'      </div>')
    parts.append(f'    </div>')
    parts.append(f'  </div>')

parts.append('')
parts.append('  <div style="margin-top:40px;background:var(--warm-white);border-left:4px solid var(--orange);border-radius:0 8px 8px 0;padding:18px 22px;font-size:13px;line-height:1.65;">')
parts.append('    <strong style="color:var(--orange);font-family:\'JetBrains Mono\',monospace;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;display:block;margin-bottom:6px;">Como usar</strong>')
parts.append('    Escolha a expressão pelo contexto comunicativo, não pela estética. <strong>Empatia</strong> para social/atendimento, <strong>Intelecto</strong> para conteúdo educacional/pesquisa, <strong>Execução</strong> para produto/dev/falhas técnicas, <strong>Astúcia</strong> para conteúdo jurídico/negócios. Clique em qualquer raposa para baixar.')
parts.append('  </div>')
parts.append('</section>')

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(parts))

print(f"Built: {OUT}")
print(f"Lines: {len(parts)}")
print(f"Categories: {[(k, len(v)) for k,v in by_cat.items()]}")
