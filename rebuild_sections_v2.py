"""
Reconstrói seções 11 (Ícones) e 12 (Elementos & Criativos) v2:
- Remove cards Glass (deletados)
- Adiciona botões de download SVG + PNG (4096px transparente) em cada card
- Mantém demais elementos (bubbles, tech, holo, mesh, 3D, patterns, decoratives)
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
INDEX = ROOT / "index.html"

# ─────────────────────────────────────────────────
# LISTAS DE ASSETS
# ─────────────────────────────────────────────────
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

BUBBLES = [
    ("bubble-cluster","Cluster Bolhas","bubbles"),
    ("bubble-giant-amber","Orb Amber","bubbles"),
    ("bubble-giant-orange","Orb Orange","bubbles"),
    ("bubble-giant-crimson","Orb Crimson","bubbles"),
    ("bubble-droplet","Droplet","bubbles"),
    ("bubble-floating-column","Floating","bubbles"),
    ("bubble-metaball","Metaball","bubbles"),
    ("bubble-trio-amber","Trio","bubbles"),
]

TECH = [
    ("tech-circuit","Circuit Board","tech"),
    ("tech-hex-grid","Hex Grid HUD","tech"),
    ("tech-neon-frame","Neon Frame","tech"),
    ("tech-data-flow","Data Flow","tech"),
    ("tech-hud-corner","HUD Corner","tech"),
    ("tech-perspective","Perspective","tech"),
    ("tech-terminal","Terminal","tech"),
    ("tech-chip","Chip iLab","tech"),
    ("tech-radar","Radar","tech"),
    ("tech-binary","Binary Rain","tech"),
]

HOLO = [
    ("holo-foil-amber","Foil Amber","holographic"),
    ("holo-foil-warm","Foil Warm","holographic"),
    ("holo-wave","Wave","holographic"),
    ("holo-prism","Prism","holographic"),
    ("holo-disc","Disc","holographic"),
]

MESH = [
    ("mesh-amber-sunrise","Amber Sunrise","creatives"),("mesh-crimson-ember","Crimson Ember","creatives"),
    ("mesh-dark-glow","Dark Glow","creatives"),("mesh-warm-haze","Warm Haze","creatives"),
    ("mesh-ember-deep","Ember Deep","creatives"),("mesh-golden-flare","Golden Flare","creatives"),
    ("mesh-sunset-fold","Sunset Fold","creatives"),("mesh-charcoal-bloom","Charcoal Bloom","creatives"),
    ("mesh-vanilla-dawn","Vanilla Dawn","creatives"),("mesh-amber-storm","Amber Storm","creatives"),
    ("mesh-fire-pulse","Fire Pulse","creatives"),("mesh-soft-radiance","Soft Radiance","creatives"),
]

SCENES_3D = [
    ("iso-cube-stack","Cube Stack","scenes_3d"),("iso-network","Network 3D","scenes_3d"),
    ("iso-layers","Camadas","scenes_3d"),("3d-sphere","Esfera","scenes_3d"),
    ("3d-torus","Torus","scenes_3d"),("3d-pyramid","Pirâmide","scenes_3d"),
]

PATTERNS = [
    ("dot-amber","Dot Pattern","patterns"),
    ("grid-warm","Grid Warm","patterns"),
    ("wave-ember","Wave Ember","patterns"),
    ("hex-golden","Hex Golden","patterns"),
]

DECOR = [
    ("bracket-corner-tl","Bracket","decoratives"),
    ("divider-flame","Divider","decoratives"),
    ("badge-circle","Badge iLab","decoratives"),
    ("arrow-stylized","Arrow","decoratives"),
    ("spark-corner","Spark","decoratives"),
    ("tag-banner","Tag Banner","decoratives"),
    ("quote-marks","Quote","decoratives"),
    ("ribbon","Ribbon","decoratives"),
]

BLOBS = [(f"blob-{i:02d}", f"Blob {i:02d}", "creatives") for i in range(1, 9)]


# ─────────────────────────────────────────────────
# SEÇÃO 11 — ÍCONES (PROFISSIONAIS DA ICONIFY)
# ─────────────────────────────────────────────────
def build_section_icones():
    html = '''<!-- 11 ÍCONES (ICONIFY: Lucide + Phosphor) -->
<section id="icones">
  <div class="section-label">11 — Ícones</div>
  <h2>Biblioteca de Ícones</h2>
  <p class="section-desc">32 ícones profissionais (Lucide + Phosphor via Iconify) em 4 estilos cada. Clique nos botões de cada card para baixar em SVG (vetor) ou PNG 4096px com fundo transparente.</p>

  <div class="ic-controls">
    <div class="ic-tabs">
      <button class="ic-tab active" data-style="outline">Outline · Lucide</button>
      <button class="ic-tab" data-style="solid">Solid · Phosphor</button>
      <button class="ic-tab" data-style="duotone">Duotone · Phosphor</button>
      <button class="ic-tab" data-style="gradient">Gradient · Lucide</button>
    </div>
    <div class="ic-filters">
      <button class="ic-filter active" data-cat="all">Todos</button>
      <button class="ic-filter" data-cat="Jurídico">Jurídico</button>
      <button class="ic-filter" data-cat="Tech">Tech</button>
      <button class="ic-filter" data-cat="Inovação">Inovação</button>
      <button class="ic-filter" data-cat="Educação">Educação</button>
      <button class="ic-filter" data-cat="Comunidade">Comunidade</button>
      <button class="ic-filter" data-cat="Mídia">Mídia</button>
      <button class="ic-filter" data-cat="Workflow">Workflow</button>
      <button class="ic-filter" data-cat="Dados">Dados</button>
    </div>
  </div>

  <div class="ic-grid">
'''
    for name, label, cat in ICONS:
        html += f'''    <div class="ic-card" data-icon="{name}" data-category="{cat}">
      <div class="ic-icon-wrap">
        <img src="assets/icons_v2/{name}-outline.svg" alt="{label}" class="ic-img" data-name="{name}">
      </div>
      <div class="ic-meta">
        <div class="ic-name">{label}</div>
        <div class="ic-cat">{cat}</div>
      </div>
      <div class="ic-actions">
        <button class="dl-btn dl-svg" data-asset="{name}" data-folder="icons_v2" data-style="outline" data-label="{name}" title="Baixar SVG vetorizado">SVG</button>
        <button class="dl-btn dl-png" data-asset="{name}" data-folder="icons_v2" data-style="outline" data-label="{name}" data-size="4096" title="Baixar PNG 4096px transparente">PNG</button>
      </div>
    </div>
'''
    html += '''  </div>
</section>
'''
    return html


# ─────────────────────────────────────────────────
# SEÇÃO 12 — ELEMENTOS & CRIATIVOS (SEM GLASS)
# ─────────────────────────────────────────────────
def el_card(name, label, folder, cat_filter, size=2048, tag=None, square=False, warm=False):
    tag = tag or cat_filter.title()
    classes = "el-card"
    if square: classes += " el-card-square"
    if warm:   classes += " el-card-decor"
    return f'''    <div class="{classes}" data-cat="{cat_filter}">
      <img src="assets/{folder}/{name}.svg" alt="{label}" class="el-img{' el-img-warm' if warm else ''}">
      <div class="el-label">
        <span>{label} <span class="el-tag">{tag}</span></span>
        <span class="el-dl">
          <button class="dl-mini dl-svg" data-asset="{name}" data-folder="{folder}" data-label="{name}" title="SVG">SVG</button>
          <button class="dl-mini dl-png" data-asset="{name}" data-folder="{folder}" data-label="{name}" data-size="{size}" title="PNG {size}px">PNG</button>
        </span>
      </div>
    </div>
'''


def build_section_elementos():
    html = '''<!-- 12 ELEMENTOS & CRIATIVOS (UNIFICADA · SEM GLASS) -->
<section id="elementos">
  <div class="section-label">12 — Elementos & Criativos</div>
  <h2>Biblioteca Visual Completa</h2>
  <p class="section-desc">66 elementos criativos: bolhas, tech, holográficos, mesh gradients, cenas 3D, padrões e decoratives. Todos vetorizados em SVG, dentro da paleta oficial. Cada item tem download SVG (vetor) ou PNG 2048-4096px com fundo transparente.</p>

  <div class="el-filters">
    <button class="el-filter active" data-cat="all">Todos</button>
    <button class="el-filter" data-cat="bubbles">Bolhas & Orbs</button>
    <button class="el-filter" data-cat="tech">Tech</button>
    <button class="el-filter" data-cat="holographic">Holográfico</button>
    <button class="el-filter" data-cat="creatives-mesh">Mesh Gradients</button>
    <button class="el-filter" data-cat="scenes_3d">Cenas 3D</button>
    <button class="el-filter" data-cat="creatives-blob">Blobs</button>
    <button class="el-filter" data-cat="patterns">Padrões</button>
    <button class="el-filter" data-cat="decoratives">Decoratives</button>
  </div>

  <div class="el-grid">
'''
    # BUBBLES (PNG 3000px - elementos visuais ricos)
    for name, label, folder in BUBBLES:
        html += el_card(name, label, folder, "bubbles", size=3000, tag="Bubble")
    # TECH
    for name, label, folder in TECH:
        html += el_card(name, label, folder, "tech", size=3000, tag="Tech")
    # HOLO
    for name, label, folder in HOLO:
        html += el_card(name, label, folder, "holographic", size=3000, tag="Holo")
    # MESH (PNG 4096 para uso como background)
    for name, label, folder in MESH:
        html += el_card(name, label, folder, "creatives-mesh", size=4096, tag="Mesh")
    # 3D
    for name, label, folder in SCENES_3D:
        html += el_card(name, label, folder, "scenes_3d", size=3000, tag="3D", square=True)
    # BLOBS
    for name, label, folder in BLOBS:
        html += el_card(name, label, folder, "creatives-blob", size=2048, tag="Blob", square=True, warm=True)
    # PATTERNS
    for name, label, folder in PATTERNS:
        html += el_card(name, label, folder, "patterns", size=1024, tag="Pattern", square=True)
    # DECOR
    for name, label, folder in DECOR:
        html += el_card(name, label, folder, "decoratives", size=2048, tag="Decor", square=True, warm=True)

    html += '''  </div>
</section>
'''
    return html


# ─────────────────────────────────────────────────
# SECTION 13 (Templates Canva) — mantém igual
# ─────────────────────────────────────────────────
SECTION_TEMPLATES = '''<!-- 13 TEMPLATES & INTEGRAÇÕES -->
<section id="canva-templates">
  <div class="section-label">13 — Templates & Integrações</div>
  <h2>Templates & Plataformas Conectadas</h2>
  <p class="section-desc">Designs ativos no Canva da marca + ferramentas de design integradas via MCP.</p>

  <div class="canva-grid">
    <div class="canva-card">
      <a href="https://www.canva.com/d/fc25DSfl3yKPeo9" target="_blank" class="canva-link">
        <div class="canva-thumb">
          <img src="https://design.canva.ai/mqrGAGISJxA8wXE" alt="Templadr Parceria" onerror="this.style.display='none';this.parentElement.style.background='linear-gradient(135deg,#F4C430,#FF6B35)';">
          <div class="canva-overlay"><span class="canva-cta">Abrir no Canva &rarr;</span></div>
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
      <div class="canva-tool"><div class="canva-tool-icon">🎨</div><div class="canva-tool-name">Canva MCP</div><div class="canva-tool-desc">Conectado · Criação, edição e exportação direto do Claude</div></div>
      <div class="canva-tool"><div class="canva-tool-icon">📦</div><div class="canva-tool-name">Iconify API</div><div class="canva-tool-desc">Lucide + Phosphor · 200+ packs de ícones profissionais</div></div>
      <div class="canva-tool"><div class="canva-tool-icon">🅰️</div><div class="canva-tool-name">Adobe Illustrator</div><div class="canva-tool-desc">Manual · Importar SVGs direto no .ai</div></div>
      <div class="canva-tool"><div class="canva-tool-icon">🖼️</div><div class="canva-tool-name">Adobe Photoshop</div><div class="canva-tool-desc">Manual · PNGs 4096px transparente</div></div>
    </div>
  </div>
</section>
'''

# ─────────────────────────────────────────────────
# CSS V2 (com botões dl + sem .glass-frosted etc)
# ─────────────────────────────────────────────────
EXTRA_CSS = '''
/* === SEÇÕES UNIFICADAS V2 (com download SVG/PNG) === */
.ic-controls{margin:24px 0 28px}
.ic-tabs{display:flex;gap:8px;margin-bottom:14px;flex-wrap:wrap}
.ic-tab{font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;background:#fff;border:1.5px solid #1A1A1A;color:#1A1A1A;padding:10px 18px;border-radius:6px;cursor:pointer;transition:all .2s}
.ic-tab:hover{background:#FAF3E0}
.ic-tab.active{background:#1A1A1A;color:#F4C430}
.ic-filters{display:flex;gap:6px;flex-wrap:wrap}
.ic-filter{font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:600;letter-spacing:.5px;text-transform:uppercase;background:#fff;border:1px solid #E5E5E5;color:#666;padding:6px 12px;border-radius:20px;cursor:pointer;transition:all .2s}
.ic-filter:hover{background:#FAF3E0;color:#1A1A1A;border-color:#F4C430}
.ic-filter.active{background:#FF6B35;color:#fff;border-color:#FF6B35}
.ic-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:16px}
.ic-card{background:#fff;border:1px solid #EEE;border-radius:12px;padding:18px 14px;text-align:center;transition:all .25s;position:relative;display:flex;flex-direction:column}
.ic-card.hidden{display:none}
.ic-card:hover{transform:translateY(-3px);border-color:#F4C430;box-shadow:0 10px 30px rgba(244,196,48,.18)}
.ic-icon-wrap{height:64px;display:flex;align-items:center;justify-content:center;margin-bottom:10px}
.ic-img{width:48px;height:48px}
.ic-name{font-family:'Poppins',sans-serif;font-weight:700;font-size:13px;color:#1A1A1A;margin-bottom:2px}
.ic-cat{font-family:'JetBrains Mono',monospace;font-size:9px;color:#999;letter-spacing:.5px;text-transform:uppercase;margin-bottom:10px}
.ic-actions{display:flex;gap:6px;justify-content:center;margin-top:auto}

.dl-btn{font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:700;letter-spacing:.5px;background:#1A1A1A;color:#F4C430;border:none;padding:6px 12px;border-radius:6px;cursor:pointer;transition:all .15s;flex:1;max-width:55px}
.dl-btn:hover{background:#F4C430;color:#1A1A1A}
.dl-btn.dl-png{background:#FF6B35;color:#fff}
.dl-btn.dl-png:hover{background:#C41E3A;color:#fff}

.el-filters{display:flex;gap:6px;flex-wrap:wrap;margin:24px 0 28px}
.el-filter{font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:600;letter-spacing:.5px;text-transform:uppercase;background:#fff;border:1px solid #E5E5E5;color:#666;padding:8px 14px;border-radius:20px;cursor:pointer;transition:all .2s}
.el-filter:hover{background:#FAF3E0;color:#1A1A1A;border-color:#F4C430}
.el-filter.active{background:#1A1A1A;color:#F4C430;border-color:#1A1A1A}
.el-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:18px}
.el-card{background:#1A1A1A;border-radius:12px;overflow:hidden;transition:transform .25s;display:flex;flex-direction:column}
.el-card.hidden{display:none}
.el-card:hover{transform:translateY(-3px);box-shadow:0 14px 36px rgba(0,0,0,.3)}
.el-card-square .el-img{aspect-ratio:1/1;object-fit:cover}
.el-img{width:100%;height:auto;display:block;flex:1;object-fit:cover}
.el-img-warm{background:#FAF3E0;padding:14px;box-sizing:border-box}
.el-label{font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#FAF3E0;background:#1A1A1A;padding:11px 14px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid rgba(244,196,48,.15);gap:8px}
.el-tag{font-size:9px;color:#F4C430;background:rgba(244,196,48,.15);padding:3px 8px;border-radius:10px;font-weight:600;margin-left:6px}
.el-dl{display:flex;gap:4px}
.dl-mini{font-family:'JetBrains Mono',monospace;font-size:9px;font-weight:700;letter-spacing:.5px;background:rgba(244,196,48,.18);color:#F4C430;border:none;padding:4px 8px;border-radius:4px;cursor:pointer;transition:all .15s}
.dl-mini:hover{background:#F4C430;color:#1A1A1A}
.dl-mini.dl-png{background:rgba(255,107,53,.2);color:#FF6B35}
.dl-mini.dl-png:hover{background:#FF6B35;color:#fff}
.el-card-decor{background:#FAF3E0;padding:20px;justify-content:center;align-items:center;min-height:220px}
.el-card-decor .el-label{color:#1A1A1A;background:#FAF3E0;border-top:1px solid rgba(0,0,0,.08)}
.el-card-decor .el-tag{color:#FF6B35;background:rgba(255,107,53,.12)}
.el-card-decor .dl-mini{background:rgba(26,26,26,.08);color:#1A1A1A}
.el-card-decor .dl-mini:hover{background:#1A1A1A;color:#F4C430}
.el-card-decor .dl-mini.dl-png{background:rgba(255,107,53,.15);color:#FF6B35}
.el-card-decor .dl-mini.dl-png:hover{background:#FF6B35;color:#fff}

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
.cr-h3{font-family:'Poppins',sans-serif;font-weight:900;font-size:18px;color:#1A1A1A;margin:36px 0 16px;letter-spacing:-.3px;text-transform:uppercase}
.canva-tools-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;margin-top:16px}
.canva-tool{background:#1A1A1A;border-radius:12px;padding:20px;color:#FAF3E0;border-top:3px solid #F4C430}
.canva-tool-icon{font-size:32px;margin-bottom:10px}
.canva-tool-name{font-family:'Poppins',sans-serif;font-weight:900;font-size:15px;color:#F4C430;margin-bottom:6px}
.canva-tool-desc{font-family:'JetBrains Mono',monospace;font-size:11px;line-height:1.5;color:#FAF3E0;opacity:.75}

/* Toast de download */
#dl-toast-v2{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(120%);background:#1A1A1A;color:#FAF3E0;padding:14px 22px;border-radius:8px;font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:1px;text-transform:uppercase;box-shadow:0 8px 32px rgba(0,0,0,.3);z-index:9999;transition:transform .35s cubic-bezier(.16,1,.3,1);pointer-events:none;border-left:3px solid #F4C430}
#dl-toast-v2.show{transform:translateX(-50%) translateY(0)}
'''

# ─────────────────────────────────────────────────
# JS V2 — download SVG + PNG transparente
# ─────────────────────────────────────────────────
EXTRA_JS = '''
<script>
// === Toast helper ===
(function(){
  let toast = document.getElementById('dl-toast-v2');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'dl-toast-v2';
    document.body.appendChild(toast);
  }
  window.showDlToast = function(msg) {
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(window._dlToastTimer);
    window._dlToastTimer = setTimeout(() => toast.classList.remove('show'), 2400);
  };
})();

// === Download SVG (vetor — link direto) ===
function dlSVG(folder, asset, style, label) {
  const filename = style ? `${asset}-${style}` : asset;
  const url = `assets/${folder}/${filename}.svg`;
  fetch(url).then(r => r.blob()).then(blob => {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `${label || filename}.svg`;
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    showDlToast(`SVG · ${a.download}`);
  });
}

// === Download PNG transparente em alta resolução ===
function dlPNG(folder, asset, style, label, size) {
  size = size || 2048;
  const filename = style ? `${asset}-${style}` : asset;
  const url = `assets/${folder}/${filename}.svg`;
  showDlToast(`Gerando PNG ${size}px...`);
  fetch(url).then(r => r.text()).then(svgText => {
    // Garantir width/height no SVG raiz
    const parser = new DOMParser();
    const doc = parser.parseFromString(svgText, 'image/svg+xml');
    const svg = doc.documentElement;
    let vbW = size, vbH = size;
    const vb = svg.getAttribute('viewBox');
    if (vb) {
      const parts = vb.split(/\\s+/).map(Number);
      const w = parts[2], h = parts[3];
      const ratio = w / h;
      vbW = size; vbH = Math.round(size / ratio);
    }
    svg.setAttribute('width', vbW);
    svg.setAttribute('height', vbH);
    const serialized = new XMLSerializer().serializeToString(svg);
    const svgBlob = new Blob([serialized], {type: 'image/svg+xml;charset=utf-8'});
    const blobUrl = URL.createObjectURL(svgBlob);
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement('canvas');
      canvas.width = vbW;
      canvas.height = vbH;
      const ctx = canvas.getContext('2d');
      // Fundo transparente (não pintar nada)
      ctx.drawImage(img, 0, 0, vbW, vbH);
      canvas.toBlob(blob => {
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = `${label || filename}-${size}px.png`;
        document.body.appendChild(a); a.click(); document.body.removeChild(a);
        URL.revokeObjectURL(blobUrl);
        showDlToast(`PNG ${vbW}x${vbH}px · ${a.download}`);
      }, 'image/png');
    };
    img.onerror = () => showDlToast('ERRO ao gerar PNG');
    img.src = blobUrl;
  });
}

// === Bind nos botões ===
document.addEventListener('click', (e) => {
  const btn = e.target.closest('.dl-svg, .dl-png');
  if (!btn) return;
  e.stopPropagation();
  const folder = btn.dataset.folder;
  const asset  = btn.dataset.asset;
  const style  = btn.dataset.style || '';
  const label  = btn.dataset.label || asset;
  if (btn.classList.contains('dl-svg')) {
    dlSVG(folder, asset, style, label);
  } else {
    const size = parseInt(btn.dataset.size || '2048', 10);
    dlPNG(folder, asset, style, label, size);
  }
});

// === Tabs de estilo dos ícones (atualiza img src + data-style dos botões) ===
document.querySelectorAll('.ic-tab').forEach(btn => {
  btn.addEventListener('click', () => {
    const style = btn.dataset.style;
    document.querySelectorAll('.ic-tab').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.ic-card').forEach(card => {
      const img = card.querySelector('.ic-img');
      const name = img.dataset.name;
      img.src = `assets/icons_v2/${name}-${style}.svg`;
      // Atualizar data-style dos botões dl
      card.querySelectorAll('.dl-btn').forEach(b => {
        b.dataset.style = style;
        b.dataset.label = `${name}-${style}`;
      });
    });
  });
});

// === Filtros de categoria dos ícones ===
document.querySelectorAll('.ic-filter').forEach(btn => {
  btn.addEventListener('click', () => {
    const cat = btn.dataset.cat;
    document.querySelectorAll('.ic-filter').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.ic-card').forEach(card => {
      card.classList.toggle('hidden', cat !== 'all' && card.dataset.category !== cat);
    });
  });
});

// === Filtros de elementos ===
document.querySelectorAll('.el-filter').forEach(btn => {
  btn.addEventListener('click', () => {
    const cat = btn.dataset.cat;
    document.querySelectorAll('.el-filter').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.el-card').forEach(card => {
      card.classList.toggle('hidden', cat !== 'all' && card.dataset.cat !== cat);
    });
  });
});
</script>
'''


# ─────────────────────────────────────────────────
# EXECUÇÃO
# ─────────────────────────────────────────────────
content = INDEX.read_text(encoding="utf-8")

def remove_section(html, section_id):
    pattern = re.compile(
        r'<!--[^>]*?-->\s*<section id="' + re.escape(section_id) + r'">.*?</section>\s*',
        re.DOTALL
    )
    new_html, n = pattern.subn('', html, count=1)
    if n == 0:
        pattern2 = re.compile(
            r'<section id="' + re.escape(section_id) + r'">.*?</section>\s*',
            re.DOTALL
        )
        new_html, n = pattern2.subn('', html, count=1)
    return new_html

# Remover seções antigas
for sid in ["icones", "elementos", "canva-templates"]:
    content = remove_section(content, sid)

# Remover CSS antigo
content = re.sub(
    r'/\* === SEÇÕES UNIFICADAS.*?(?=\n/\*[^/]|</style>)',
    '',
    content,
    flags=re.DOTALL
)

# Remover JS antigo (qualquer script com ic-tab, el-filter, dlSVG, dlPNG, ip-tab)
content = re.sub(
    r'<script>\s*(?://[^\n]*\n)*\s*(?://[^\n]*\n|.)*?(?:document\.querySelectorAll\(\'\.ic-tab\'\)|document\.querySelectorAll\(\'\.el-filter\'\)|document\.querySelectorAll\(\'\.ip-tab\'\)).*?</script>\s*',
    '',
    content,
    flags=re.DOTALL
)

# Inserir CSS
content = content.replace("</style>", EXTRA_CSS + "\n</style>", 1)

# Inserir seções
new_sections = build_section_icones() + "\n" + build_section_elementos() + "\n" + SECTION_TEMPLATES
content = content.replace("<footer>", new_sections + "\n<footer>", 1)

# Inserir JS
content = content.replace("</body>", EXTRA_JS + "\n</body>", 1)

# Atualizar nav (caso já tenha sido atualizada — não recriar duplicado)
INDEX.write_text(content, encoding="utf-8")
print("OK: secoes 11/12/13 reconstruidas (v2)")
print(f"  11 - Icones: 32 da Iconify (Lucide+Phosphor) x 4 estilos = 128 SVGs profissionais")
print(f"  12 - Elementos: 8 bubbles + 10 tech + 5 holo + 12 mesh + 6 3D + 8 blobs + 4 patterns + 8 decor = 61")
print(f"  13 - Templates & Integracoes")
print(f"  + Cada card agora tem botoes [SVG] e [PNG transparente] em alta resolucao")
