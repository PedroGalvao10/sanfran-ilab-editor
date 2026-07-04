"""Gera o HTML das 3 novas seções (13/14/15) e injeta no index.html."""
from pathlib import Path

ROOT = Path(__file__).parent
INDEX = ROOT / "index.html"

# Listas de assets
ICONS = [
    ("scales","Balança","Jurídico"),("gavel","Martelo","Jurídico"),
    ("contract","Contrato","Jurídico"),("courthouse","Tribunal","Jurídico"),
    ("cpu","Processador","Tech"),("code","Código","Tech"),
    ("cloud","Cloud","Tech"),("api","API","Tech"),
    ("lightbulb","Ideia","Inovação"),("rocket","Lançamento","Inovação"),
    ("gear-arrow","Sistema","Inovação"),("blueprint","Blueprint","Inovação"),
    ("book","Livro","Educação"),("mortarboard","Formatura","Educação"),
    ("chalkboard","Quadro","Educação"),("certificate","Certificado","Educação"),
    ("handshake","Parceria","Comunidade"),("network","Rede","Comunidade"),
    ("megaphone","Voz","Comunidade"),("globe","Global","Comunidade"),
    ("camera","Câmera","Mídia"),("microphone","Microfone","Mídia"),
    ("broadcast","Broadcast","Mídia"),("play-circle","Play","Mídia"),
    ("kanban","Kanban","Workflow"),("checklist","Checklist","Workflow"),
    ("calendar","Calendário","Workflow"),("sync","Sync","Workflow"),
    ("chart-bar","Métricas","Dados"),("chart-line","Tendência","Dados"),
    ("target","Alvo","Dados"),("pulse","Pulso","Dados"),
]

STYLES = ["outline","solid","duotone","gradient"]
STYLE_LABELS = {"outline":"Outline","solid":"Solid","duotone":"Duotone","gradient":"Gradient"}

# ─────────────────────────────────────────
# SEÇÃO 13 — ÍCONES+
# ─────────────────────────────────────────
icons_html = '''
<!-- 13 ÍCONES+ -->
<section id="icones-plus">
  <div class="section-label">13 — Ícones+ (Expansão)</div>
  <h2>Biblioteca Estendida</h2>
  <p class="section-desc">32 ícones vetorizados em 4 estilos cada (128 SVGs totais). Outline, Solid, Duotone e Gradient. Use o estilo conforme o contexto: outline para UI, solid para destaque, duotone para cards, gradient para hero/premium.</p>

  <div class="ip-tabs">
    <button class="ip-tab active" data-style="outline">Outline</button>
    <button class="ip-tab" data-style="solid">Solid</button>
    <button class="ip-tab" data-style="duotone">Duotone</button>
    <button class="ip-tab" data-style="gradient">Gradient</button>
  </div>

  <div class="ip-grid">
'''
for name, label, cat in ICONS:
    icons_html += f'''    <div class="ip-card" data-icon="{name}" data-category="{cat}">
      <div class="ip-icon-wrap">
        <img src="assets/icons_v2/{name}-outline.svg" alt="{label}" class="ip-img" data-name="{name}">
      </div>
      <div class="ip-meta">
        <div class="ip-name">{label}</div>
        <div class="ip-cat">{cat}</div>
      </div>
    </div>
'''
icons_html += '''  </div>
</section>
'''

# ─────────────────────────────────────────
# SEÇÃO 14 — CRIATIVOS
# ─────────────────────────────────────────
MESH = [
    ("mesh-amber-sunrise","Amber Sunrise"),("mesh-crimson-ember","Crimson Ember"),
    ("mesh-dark-glow","Dark Glow"),("mesh-warm-haze","Warm Haze"),
    ("mesh-ember-deep","Ember Deep"),("mesh-golden-flare","Golden Flare"),
    ("mesh-sunset-fold","Sunset Fold"),("mesh-charcoal-bloom","Charcoal Bloom"),
    ("mesh-vanilla-dawn","Vanilla Dawn"),("mesh-amber-storm","Amber Storm"),
    ("mesh-fire-pulse","Fire Pulse"),("mesh-soft-radiance","Soft Radiance"),
]
SCENES_3D = [
    ("iso-cube-stack","Cube Stack","Isométrico"),
    ("iso-network","Network 3D","Isométrico"),
    ("iso-layers","Camadas","Isométrico"),
    ("3d-sphere","Esfera","3D"),
    ("3d-torus","Torus","3D"),
    ("3d-pyramid","Pirâmide","3D"),
]
PATTERNS = [("dot-amber","Dot Pattern"),("grid-warm","Grid Warm"),
            ("wave-ember","Wave Ember"),("hex-golden","Hex Golden")]
DECOR = [
    ("bracket-corner-tl","Bracket Corner"),("divider-flame","Divider Flame"),
    ("badge-circle","Badge iLab"),("arrow-stylized","Arrow"),
    ("spark-corner","Spark"),("tag-banner","Tag Banner"),
    ("quote-marks","Quote Marks"),("ribbon","Ribbon"),
]

creativos_html = '''
<!-- 14 CRIATIVOS -->
<section id="criativos">
  <div class="section-label">14 — Criativos & 3D</div>
  <h2>Criativos, Abstratos & 3D</h2>
  <p class="section-desc">Mesh gradients, blobs orgânicos, cenas isométricas 3D, padrões geométricos e decoratives. Todos vetorizados em SVG, dentro da paleta oficial. Use como backgrounds, headers, separadores ou elementos de destaque.</p>

  <h3 class="cr-h3">Mesh Gradients · 12</h3>
  <div class="cr-grid cr-grid-mesh">
'''
for name, label in MESH:
    creativos_html += f'''    <div class="cr-card">
      <img src="assets/creatives/{name}.svg" alt="{label}" class="cr-img">
      <div class="cr-label">{label}</div>
    </div>
'''
creativos_html += '''  </div>

  <h3 class="cr-h3">Blobs Orgânicos · 8</h3>
  <div class="cr-grid cr-grid-blobs">
'''
for i in range(1, 9):
    creativos_html += f'''    <div class="cr-card cr-blob">
      <img src="assets/creatives/blob-{i:02d}.svg" alt="Blob {i}" class="cr-img">
      <div class="cr-label">Blob {i:02d}</div>
    </div>
'''
creativos_html += '''  </div>

  <h3 class="cr-h3">Cenas 3D & Isométricas · 6</h3>
  <div class="cr-grid cr-grid-3d">
'''
for name, label, tag in SCENES_3D:
    creativos_html += f'''    <div class="cr-card">
      <img src="assets/scenes_3d/{name}.svg" alt="{label}" class="cr-img">
      <div class="cr-label">{label} <span class="cr-tag">{tag}</span></div>
    </div>
'''
creativos_html += '''  </div>

  <h3 class="cr-h3">Padrões Geométricos · 4</h3>
  <div class="cr-grid cr-grid-pat">
'''
for name, label in PATTERNS:
    creativos_html += f'''    <div class="cr-card">
      <div class="cr-pat-preview" style="background-image:url(assets/patterns/{name}.svg);"></div>
      <div class="cr-label">{label}</div>
    </div>
'''
creativos_html += '''  </div>

  <h3 class="cr-h3">Decoratives · 8</h3>
  <div class="cr-grid cr-grid-dec">
'''
for name, label in DECOR:
    creativos_html += f'''    <div class="cr-card cr-dec">
      <img src="assets/decoratives/{name}.svg" alt="{label}" class="cr-img">
      <div class="cr-label">{label}</div>
    </div>
'''
creativos_html += '''  </div>
</section>
'''

# ─────────────────────────────────────────
# SEÇÃO 15 — TEMPLATES CANVA
# ─────────────────────────────────────────
canva_html = '''
<!-- 15 TEMPLATES CANVA -->
<section id="canva-templates">
  <div class="section-label">15 — Templates Canva</div>
  <h2>Designs no Canva</h2>
  <p class="section-desc">Templates e designs ativos no Canva da marca. Para criar novos materiais, parta destes designs ou abra um novo a partir do brand kit.</p>

  <div class="canva-grid">
    <div class="canva-card">
      <a href="https://www.canva.com/d/fc25DSfl3yKPeo9" target="_blank" class="canva-link">
        <div class="canva-thumb">
          <img src="https://design.canva.ai/mqrGAGISJxA8wXE" alt="Templadr Parceria" onerror="this.style.display='none';this.parentElement.style.background='linear-gradient(135deg,#F4C430,#FF6B35)';">
          <div class="canva-overlay">
            <span class="canva-cta">Abrir no Canva →</span>
          </div>
        </div>
        <div class="canva-meta">
          <div class="canva-title">Templadr Parceria</div>
          <div class="canva-sub">2 páginas · Apresentação institucional</div>
        </div>
      </a>
    </div>

    <div class="canva-card canva-new">
      <a href="https://www.canva.com/design" target="_blank" class="canva-link">
        <div class="canva-thumb canva-thumb-empty">
          <div class="canva-plus">+</div>
          <div class="canva-newlabel">Criar novo design</div>
        </div>
        <div class="canva-meta">
          <div class="canva-title">Novo design</div>
          <div class="canva-sub">Abrir Canva e começar do zero</div>
        </div>
      </a>
    </div>
  </div>

  <div class="canva-tools">
    <h3 class="cr-h3">Integrações & Plugins</h3>
    <div class="canva-tools-grid">
      <div class="canva-tool">
        <div class="canva-tool-icon">🎨</div>
        <div class="canva-tool-name">Canva MCP</div>
        <div class="canva-tool-desc">Conectado · Criação, edição e exportação direto do Claude</div>
      </div>
      <div class="canva-tool">
        <div class="canva-tool-icon">📐</div>
        <div class="canva-tool-name">Figma</div>
        <div class="canva-tool-desc">MCP disponível · Import design tokens & components</div>
      </div>
      <div class="canva-tool">
        <div class="canva-tool-icon">🅰️</div>
        <div class="canva-tool-name">Adobe Illustrator</div>
        <div class="canva-tool-desc">Manual · Importar SVGs desta biblioteca direto no .ai</div>
      </div>
      <div class="canva-tool">
        <div class="canva-tool-icon">🖼️</div>
        <div class="canva-tool-name">Adobe Photoshop</div>
        <div class="canva-tool-desc">Manual · Mesh gradients em camadas, exportar PNG/PSD</div>
      </div>
    </div>
  </div>
</section>
'''

# ─────────────────────────────────────────
# CSS adicional (vai dentro do <style>)
# ─────────────────────────────────────────
extra_css = '''
/* === 13/14/15 — ESTILOS DAS NOVAS SEÇÕES === */
.ip-tabs{display:flex;gap:8px;margin:24px 0 32px;flex-wrap:wrap}
.ip-tab{font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;background:#fff;border:1.5px solid #1A1A1A;color:#1A1A1A;padding:10px 18px;border-radius:6px;cursor:pointer;transition:all .2s}
.ip-tab:hover{background:#FAF3E0}
.ip-tab.active{background:#1A1A1A;color:#F4C430}

.ip-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:16px}
.ip-card{background:#fff;border:1px solid #EEE;border-radius:12px;padding:18px 12px;text-align:center;transition:all .25s;cursor:pointer}
.ip-card:hover{transform:translateY(-3px);border-color:#F4C430;box-shadow:0 10px 30px rgba(244,196,48,.18)}
.ip-icon-wrap{height:64px;display:flex;align-items:center;justify-content:center;margin-bottom:10px}
.ip-img{width:48px;height:48px}
.ip-name{font-family:'Poppins',sans-serif;font-weight:700;font-size:13px;color:#1A1A1A;margin-bottom:2px}
.ip-cat{font-family:'JetBrains Mono',monospace;font-size:9px;color:#999;letter-spacing:.5px;text-transform:uppercase}

.cr-h3{font-family:'Poppins',sans-serif;font-weight:900;font-size:18px;color:#1A1A1A;margin:36px 0 16px;letter-spacing:-.3px;text-transform:uppercase}
.cr-h3:first-of-type{margin-top:24px}
.cr-grid{display:grid;gap:18px;margin-bottom:24px}
.cr-grid-mesh{grid-template-columns:repeat(auto-fill,minmax(220px,1fr))}
.cr-grid-blobs{grid-template-columns:repeat(auto-fill,minmax(160px,1fr))}
.cr-grid-3d{grid-template-columns:repeat(auto-fill,minmax(220px,1fr))}
.cr-grid-pat{grid-template-columns:repeat(auto-fill,minmax(180px,1fr))}
.cr-grid-dec{grid-template-columns:repeat(auto-fill,minmax(180px,1fr))}
.cr-card{background:#1A1A1A;border-radius:12px;overflow:hidden;transition:transform .25s}
.cr-card:hover{transform:translateY(-3px)}
.cr-img{width:100%;height:auto;display:block}
.cr-blob{background:#FAF3E0;padding:12px}
.cr-dec{background:#FAF3E0;padding:14px;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:140px}
.cr-pat-preview{aspect-ratio:1/1;background-repeat:repeat;background-size:auto}
.cr-label{font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#FAF3E0;background:#1A1A1A;padding:10px 14px;display:flex;justify-content:space-between;align-items:center}
.cr-blob .cr-label,.cr-dec .cr-label{color:#1A1A1A;background:#FAF3E0;border-top:1px solid rgba(0,0,0,.08);margin-top:8px}
.cr-tag{font-size:9px;color:#F4C430;background:rgba(244,196,48,.15);padding:2px 8px;border-radius:10px}
.cr-blob .cr-tag,.cr-dec .cr-tag{color:#FF6B35;background:rgba(255,107,53,.12)}

.canva-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:20px;margin:24px 0 40px}
.canva-card{background:#fff;border:1px solid #EEE;border-radius:12px;overflow:hidden;transition:all .25s}
.canva-card:hover{transform:translateY(-4px);box-shadow:0 12px 36px rgba(0,0,0,.12)}
.canva-link{text-decoration:none;color:inherit;display:block}
.canva-thumb{aspect-ratio:4/5;position:relative;overflow:hidden;background:#1A1A1A}
.canva-thumb img{width:100%;height:100%;object-fit:cover}
.canva-overlay{position:absolute;inset:0;background:linear-gradient(0deg,rgba(26,26,26,.85) 0%,rgba(26,26,26,0) 60%);display:flex;align-items:flex-end;justify-content:center;padding:20px;opacity:0;transition:opacity .25s}
.canva-card:hover .canva-overlay{opacity:1}
.canva-cta{font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#F4C430}
.canva-thumb-empty{display:flex;flex-direction:column;align-items:center;justify-content:center;background:linear-gradient(135deg,#FAF3E0 0%,#fff 100%);color:#1A1A1A;border:2px dashed #DDD}
.canva-plus{font-size:64px;font-weight:200;color:#F4C430;line-height:1}
.canva-newlabel{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:1px;text-transform:uppercase;color:#999;margin-top:8px}
.canva-meta{padding:16px 18px}
.canva-title{font-family:'Poppins',sans-serif;font-weight:900;font-size:15px;color:#1A1A1A;margin-bottom:4px}
.canva-sub{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.5px;text-transform:uppercase;color:#999}

.canva-tools-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;margin-top:16px}
.canva-tool{background:#1A1A1A;border-radius:12px;padding:20px;color:#FAF3E0;border-top:3px solid #F4C430}
.canva-tool-icon{font-size:32px;margin-bottom:10px}
.canva-tool-name{font-family:'Poppins',sans-serif;font-weight:900;font-size:15px;color:#F4C430;margin-bottom:6px}
.canva-tool-desc{font-family:'JetBrains Mono',monospace;font-size:11px;line-height:1.5;color:#FAF3E0;opacity:.75}
'''

# Script para troca de estilo nos ícones
extra_js = '''
<script>
// Tabs de estilo dos ícones+
document.querySelectorAll('.ip-tab').forEach(btn => {
  btn.addEventListener('click', () => {
    const style = btn.dataset.style;
    document.querySelectorAll('.ip-tab').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.ip-img').forEach(img => {
      const name = img.dataset.name;
      img.src = `assets/icons_v2/${name}-${style}.svg`;
    });
  });
});
</script>
'''

# ─────────────────────────────────────────
# Injetar no index.html
# ─────────────────────────────────────────
content = INDEX.read_text(encoding="utf-8")

# 1) Adicionar CSS antes do </style>
content = content.replace("</style>", extra_css + "\n</style>", 1)

# 2) Adicionar as 3 novas seções antes do <footer>
new_sections = icons_html + creativos_html + canva_html
content = content.replace("<footer>", new_sections + "\n<footer>", 1)

# 3) Adicionar JS antes de </body>
content = content.replace("</body>", extra_js + "\n</body>", 1)

INDEX.write_text(content, encoding="utf-8")
print("OK: 3 novas secoes injetadas no index.html")
print("  - 13 Icones+ (32 icones x 4 estilos)")
print("  - 14 Criativos (12 mesh + 8 blobs + 6 3D + 4 patterns + 8 decoratives)")
print("  - 15 Templates Canva (1 design existente + 4 plataformas)")
