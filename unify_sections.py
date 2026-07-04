"""
Unifica as seções do brandbook:
- Remove seções 11, 12, 13, 14 antigas
- Cria seção 11 (Ícones) unificada — 32 ícones × 4 estilos
- Cria seção 12 (Elementos & Criativos) unificada — TUDO de elementos + criativos + glass + tech + bubbles + holo
- Renomeia seção 15 (Templates) para 13
- Atualiza nav
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
INDEX = ROOT / "index.html"

# ─────────────────────────────────────────────────
# DADOS — listas completas de assets
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

GLASS = [
    ("glass-frosted-amber","Frosted Amber"),
    ("glass-refraction","Refraction"),
    ("glass-neon","Neon"),
    ("glass-chrome","Chrome"),
    ("glass-iridescent","Iridescent"),
    ("glass-aurora","Aurora"),
    ("glass-prism","Prism"),
    ("glass-holographic","Holographic"),
]

BUBBLES = [
    ("bubble-cluster","Cluster"),
    ("bubble-giant-amber","Orb Amber"),
    ("bubble-giant-orange","Orb Orange"),
    ("bubble-giant-crimson","Orb Crimson"),
    ("bubble-droplet","Droplet"),
    ("bubble-floating-column","Floating"),
    ("bubble-metaball","Metaball"),
    ("bubble-trio-amber","Trio"),
]

TECH = [
    ("tech-circuit","Circuit"),
    ("tech-hex-grid","Hex Grid"),
    ("tech-neon-frame","Neon Frame"),
    ("tech-data-flow","Data Flow"),
    ("tech-hud-corner","HUD"),
    ("tech-perspective","Perspective"),
    ("tech-terminal","Terminal"),
    ("tech-chip","Chip"),
    ("tech-radar","Radar"),
    ("tech-binary","Binary Rain"),
]

HOLO = [
    ("holo-foil-amber","Foil Amber"),
    ("holo-foil-warm","Foil Warm"),
    ("holo-wave","Wave"),
    ("holo-prism","Prism"),
    ("holo-disc","Disc"),
]

MESH = [
    ("mesh-amber-sunrise","Amber Sunrise"),("mesh-crimson-ember","Crimson Ember"),
    ("mesh-dark-glow","Dark Glow"),("mesh-warm-haze","Warm Haze"),
    ("mesh-ember-deep","Ember Deep"),("mesh-golden-flare","Golden Flare"),
    ("mesh-sunset-fold","Sunset Fold"),("mesh-charcoal-bloom","Charcoal Bloom"),
    ("mesh-vanilla-dawn","Vanilla Dawn"),("mesh-amber-storm","Amber Storm"),
    ("mesh-fire-pulse","Fire Pulse"),("mesh-soft-radiance","Soft Radiance"),
]

SCENES_3D = [
    ("iso-cube-stack","Cube Stack"),("iso-network","Network 3D"),
    ("iso-layers","Camadas"),("3d-sphere","Esfera"),
    ("3d-torus","Torus"),("3d-pyramid","Pirâmide"),
]

PATTERNS = [("dot-amber","Dot"),("grid-warm","Grid"),("wave-ember","Wave"),("hex-golden","Hex")]

DECOR = [
    ("bracket-corner-tl","Bracket"),("divider-flame","Divider"),
    ("badge-circle","Badge"),("arrow-stylized","Arrow"),
    ("spark-corner","Spark"),("tag-banner","Tag"),
    ("quote-marks","Quote"),("ribbon","Ribbon"),
]

BLOBS = [(f"blob-{i:02d}", f"Blob {i:02d}") for i in range(1, 9)]


# ─────────────────────────────────────────────────
# SEÇÃO 11 — ÍCONES UNIFICADA
# ─────────────────────────────────────────────────
def build_section_icones():
    html = '''<!-- 11 ÍCONES (UNIFICADA) -->
<section id="icones">
  <div class="section-label">11 — Ícones</div>
  <h2>Biblioteca Completa de Ícones</h2>
  <p class="section-desc">32 ícones vetorizados em 4 estilos (128 SVGs). Use os tabs para alternar entre Outline, Solid, Duotone e Gradient. Filtros por categoria abaixo.</p>

  <div class="ic-controls">
    <div class="ic-tabs">
      <button class="ic-tab active" data-style="outline">Outline</button>
      <button class="ic-tab" data-style="solid">Solid</button>
      <button class="ic-tab" data-style="duotone">Duotone</button>
      <button class="ic-tab" data-style="gradient">Gradient</button>
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
    </div>
'''
    html += '''  </div>
</section>
'''
    return html


# ─────────────────────────────────────────────────
# SEÇÃO 12 — ELEMENTOS & CRIATIVOS (UNIFICADA)
# Tudo: elementos antigos + criativos + glass + tech + bubbles + holo
# ─────────────────────────────────────────────────
def build_section_elementos():
    html = '''<!-- 12 ELEMENTOS & CRIATIVOS (UNIFICADA) -->
<section id="elementos">
  <div class="section-label">12 — Elementos & Criativos</div>
  <h2>Biblioteca Visual Completa</h2>
  <p class="section-desc">Glass, tech, bolhas, holográficos, mesh gradients, cenas 3D, padrões e decoratives. Tudo vetorizado em SVG, dentro da paleta oficial. Filtre por categoria.</p>

  <div class="el-filters">
    <button class="el-filter active" data-cat="all">Todos</button>
    <button class="el-filter" data-cat="glass">Liquid Glass</button>
    <button class="el-filter" data-cat="bubbles">Bolhas & Orbs</button>
    <button class="el-filter" data-cat="tech">Tech</button>
    <button class="el-filter" data-cat="holo">Holográfico</button>
    <button class="el-filter" data-cat="mesh">Mesh Gradients</button>
    <button class="el-filter" data-cat="3d">Cenas 3D</button>
    <button class="el-filter" data-cat="patterns">Padrões</button>
    <button class="el-filter" data-cat="decor">Decoratives</button>
    <button class="el-filter" data-cat="basics">Básicos</button>
  </div>

  <div class="el-grid">
'''
    # GLASS
    for name, label in GLASS:
        html += f'''    <div class="el-card" data-cat="glass">
      <img src="assets/glass/{name}.svg" alt="{label}" class="el-img">
      <div class="el-label">{label} <span class="el-tag">Glass</span></div>
    </div>
'''
    # BUBBLES
    for name, label in BUBBLES:
        html += f'''    <div class="el-card el-card-tall" data-cat="bubbles">
      <img src="assets/bubbles/{name}.svg" alt="{label}" class="el-img">
      <div class="el-label">{label} <span class="el-tag">Bubble</span></div>
    </div>
'''
    # TECH
    for name, label in TECH:
        html += f'''    <div class="el-card" data-cat="tech">
      <img src="assets/tech/{name}.svg" alt="{label}" class="el-img">
      <div class="el-label">{label} <span class="el-tag">Tech</span></div>
    </div>
'''
    # HOLO
    for name, label in HOLO:
        html += f'''    <div class="el-card el-card-tall" data-cat="holo">
      <img src="assets/holographic/{name}.svg" alt="{label}" class="el-img">
      <div class="el-label">{label} <span class="el-tag">Holo</span></div>
    </div>
'''
    # MESH
    for name, label in MESH:
        html += f'''    <div class="el-card" data-cat="mesh">
      <img src="assets/creatives/{name}.svg" alt="{label}" class="el-img">
      <div class="el-label">{label} <span class="el-tag">Mesh</span></div>
    </div>
'''
    # 3D
    for name, label in SCENES_3D:
        html += f'''    <div class="el-card el-card-square" data-cat="3d">
      <img src="assets/scenes_3d/{name}.svg" alt="{label}" class="el-img">
      <div class="el-label">{label} <span class="el-tag">3D</span></div>
    </div>
'''
    # BLOBS
    for name, label in BLOBS:
        html += f'''    <div class="el-card el-card-square" data-cat="3d">
      <img src="assets/creatives/{name}.svg" alt="{label}" class="el-img el-img-warm">
      <div class="el-label">{label} <span class="el-tag">Blob</span></div>
    </div>
'''
    # PATTERNS
    for name, label in PATTERNS:
        html += f'''    <div class="el-card el-card-square" data-cat="patterns">
      <div class="el-pat-preview" style="background-image:url(assets/patterns/{name}.svg);"></div>
      <div class="el-label">{label} <span class="el-tag">Pattern</span></div>
    </div>
'''
    # DECOR
    for name, label in DECOR:
        html += f'''    <div class="el-card el-card-square el-card-decor" data-cat="decor">
      <img src="assets/decoratives/{name}.svg" alt="{label}" class="el-img">
      <div class="el-label">{label} <span class="el-tag">Decor</span></div>
    </div>
'''
    # BÁSICOS (elementos antigos como dot grid, gradient bars, etc.)
    basics = [
        ("dotgrid", "Dot Grid", "Fundo dark com pontos âmbar"),
        ("gradbar-h", "Barra Gradiente H", "Topo de cards, 4px"),
        ("gradbar-v", "Barra Gradiente V", "Lateral de cards, 4px"),
        ("section-tag", "Tag de Seção", "01 — Identidade · mono uppercase"),
        ("circuit-line", "Linha Circuito", "Detalhe tech bordas"),
    ]
    for slug, label, desc in basics:
        html += f'''    <div class="el-card el-card-basic" data-cat="basics">
      <div class="el-basic el-basic-{slug}"></div>
      <div class="el-label">{label} <span class="el-tag">Básico</span></div>
    </div>
'''
    html += '''  </div>
</section>
'''
    return html


# ─────────────────────────────────────────────────
# SEÇÃO 13 — TEMPLATES & INTEGRAÇÕES (era a 15)
# ─────────────────────────────────────────────────
SECTION_TEMPLATES = '''<!-- 13 TEMPLATES & INTEGRAÇÕES -->
<section id="canva-templates">
  <div class="section-label">13 — Templates & Integrações</div>
  <h2>Templates & Plataformas Conectadas</h2>
  <p class="section-desc">Designs ativos no Canva da marca + ferramentas de design integradas via MCP e via manual.</p>

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
      <div class="canva-tool"><div class="canva-tool-icon">🎨</div><div class="canva-tool-name">Canva MCP</div><div class="canva-tool-desc">Conectado · Criação, edição e exportação direto do Claude</div></div>
      <div class="canva-tool"><div class="canva-tool-icon">📐</div><div class="canva-tool-name">Figma</div><div class="canva-tool-desc">MCP disponível · Import design tokens & components</div></div>
      <div class="canva-tool"><div class="canva-tool-icon">🅰️</div><div class="canva-tool-name">Adobe Illustrator</div><div class="canva-tool-desc">Manual · Importar SVGs direto no .ai</div></div>
      <div class="canva-tool"><div class="canva-tool-icon">🖼️</div><div class="canva-tool-name">Adobe Photoshop</div><div class="canva-tool-desc">Manual · Mesh gradients em camadas, PSD</div></div>
    </div>
  </div>
</section>
'''

# ─────────────────────────────────────────────────
# CSS EXTRA UNIFICADO
# ─────────────────────────────────────────────────
EXTRA_CSS = '''
/* === SEÇÕES UNIFICADAS 11/12/13 === */
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
.ic-card{background:#fff;border:1px solid #EEE;border-radius:12px;padding:20px 14px;text-align:center;transition:all .25s;cursor:pointer}
.ic-card.hidden{display:none}
.ic-card:hover{transform:translateY(-3px);border-color:#F4C430;box-shadow:0 10px 30px rgba(244,196,48,.18)}
.ic-icon-wrap{height:64px;display:flex;align-items:center;justify-content:center;margin-bottom:10px}
.ic-img{width:48px;height:48px}
.ic-name{font-family:'Poppins',sans-serif;font-weight:700;font-size:13px;color:#1A1A1A;margin-bottom:2px}
.ic-cat{font-family:'JetBrains Mono',monospace;font-size:9px;color:#999;letter-spacing:.5px;text-transform:uppercase}

.el-filters{display:flex;gap:6px;flex-wrap:wrap;margin:24px 0 28px}
.el-filter{font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:600;letter-spacing:.5px;text-transform:uppercase;background:#fff;border:1px solid #E5E5E5;color:#666;padding:8px 14px;border-radius:20px;cursor:pointer;transition:all .2s}
.el-filter:hover{background:#FAF3E0;color:#1A1A1A;border-color:#F4C430}
.el-filter.active{background:#1A1A1A;color:#F4C430;border-color:#1A1A1A}
.el-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px}
.el-card{background:#1A1A1A;border-radius:12px;overflow:hidden;transition:transform .25s;display:flex;flex-direction:column}
.el-card.hidden{display:none}
.el-card:hover{transform:translateY(-3px);box-shadow:0 14px 36px rgba(0,0,0,.3)}
.el-card-tall{grid-row:span 1}
.el-card-square .el-img{aspect-ratio:1/1;object-fit:cover}
.el-img{width:100%;height:auto;display:block;flex:1;object-fit:cover}
.el-img-warm{background:#FAF3E0;padding:14px;box-sizing:border-box}
.el-pat-preview{aspect-ratio:1/1;background-repeat:repeat;background-size:auto}
.el-label{font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#FAF3E0;background:#1A1A1A;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid rgba(244,196,48,.15)}
.el-tag{font-size:9px;color:#F4C430;background:rgba(244,196,48,.15);padding:3px 8px;border-radius:10px;font-weight:600}
.el-card-decor{background:#FAF3E0;padding:20px;justify-content:center;align-items:center;min-height:200px}
.el-card-decor .el-label{color:#1A1A1A;background:#FAF3E0;border-top:1px solid rgba(0,0,0,.08)}
.el-card-decor .el-tag{color:#FF6B35;background:rgba(255,107,53,.12)}
.el-card-basic{background:#FAF3E0;padding:20px;min-height:200px}
.el-card-basic .el-label{color:#1A1A1A;background:#FAF3E0}
.el-card-basic .el-tag{color:#FF6B35;background:rgba(255,107,53,.12)}
.el-basic{flex:1;min-height:120px;border-radius:6px}
.el-basic-dotgrid{background:#1A1A1A;background-image:radial-gradient(rgba(244,196,48,.5) 1px,transparent 1px);background-size:18px 18px}
.el-basic-gradbar-h{background:linear-gradient(90deg,#F4C430,#FF6B35);height:4px;margin-top:60px;align-self:stretch}
.el-basic-gradbar-v{background:linear-gradient(180deg,#F4C430,#FF6B35);width:4px;margin:0 auto;min-height:120px}
.el-basic-section-tag{background:#FAF3E0;color:#1A1A1A;font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;display:flex;align-items:center;justify-content:center;border:1px solid rgba(0,0,0,.1);border-radius:6px}
.el-basic-section-tag::before{content:"01 — IDENTIDADE"}
.el-basic-circuit-line{background:#1A1A1A;position:relative}
.el-basic-circuit-line::before{content:"";position:absolute;inset:50% 20%;border-top:1px solid #F4C430;border-radius:0}
.el-basic-circuit-line::after{content:"";position:absolute;left:20%;top:48%;width:6px;height:6px;background:#FF6B35;border-radius:1px}

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
'''

# ─────────────────────────────────────────────────
# JS UNIFICADO
# ─────────────────────────────────────────────────
EXTRA_JS = '''
<script>
// Tabs de estilo dos ícones
document.querySelectorAll('.ic-tab').forEach(btn => {
  btn.addEventListener('click', () => {
    const style = btn.dataset.style;
    document.querySelectorAll('.ic-tab').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.ic-img').forEach(img => {
      img.src = `assets/icons_v2/${img.dataset.name}-${style}.svg`;
    });
  });
});
// Filtros de categoria dos ícones
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
// Filtros de elementos
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
# EXECUÇÃO — remover seções antigas e injetar novas
# ─────────────────────────────────────────────────
content = INDEX.read_text(encoding="utf-8")

# 1) Remover seções antigas (11, 12, 13, 14, 15)
# Regex: capturar <section id="ID">...</section> com balanceamento simples (não tem section aninhada)
def remove_section(html, section_id):
    pattern = re.compile(
        r'<!--[^>]*?-->\s*<section id="' + re.escape(section_id) + r'">.*?</section>\s*',
        re.DOTALL
    )
    # Fallback se não tiver comentário antes
    new_html, n = pattern.subn('', html, count=1)
    if n == 0:
        pattern2 = re.compile(
            r'<section id="' + re.escape(section_id) + r'">.*?</section>\s*',
            re.DOTALL
        )
        new_html, n = pattern2.subn('', html, count=1)
    return new_html

for sid in ["icones", "elementos", "icones-plus", "criativos", "canva-templates"]:
    content = remove_section(content, sid)

# 2) Remover CSS antigo (entre /* === 13/14/15 e o próximo /* ou </style>)
content = re.sub(
    r'/\* === 13/14/15 — ESTILOS DAS NOVAS SEÇÕES === \*/.*?(?=\n/\*|</style>)',
    '',
    content,
    flags=re.DOTALL
)

# 3) Remover JS antigo (o script de tabs ip-tab)
content = re.sub(
    r'<script>\s*//\s*Tabs de estilo dos ícones\+.*?</script>\s*',
    '',
    content,
    flags=re.DOTALL
)

# 4) Inserir CSS novo antes de </style>
content = content.replace("</style>", EXTRA_CSS + "\n</style>", 1)

# 5) Inserir as 3 novas seções unificadas antes do <footer>
new_sections = build_section_icones() + "\n" + build_section_elementos() + "\n" + SECTION_TEMPLATES
content = content.replace("<footer>", new_sections + "\n<footer>", 1)

# 6) Inserir JS antes de </body>
content = content.replace("</body>", EXTRA_JS + "\n</body>", 1)

# 7) Atualizar nav menu
nav_pattern = re.compile(
    r'(<a href="#stories">10 · Stories</a>).*?(</nav>)',
    re.DOTALL
)
new_nav = '''<a href="#stories">10 · Stories</a>
      <a href="#icones">11 · Ícones</a>
      <a href="#elementos">12 · Elementos & Criativos</a>
      <a href="#canva-templates">13 · Templates</a>
    </nav>'''
content = nav_pattern.sub(new_nav, content)

INDEX.write_text(content, encoding="utf-8")
print("OK: secoes unificadas")
print(f"  11 - Icones: 32 icones x 4 estilos = 128 SVGs, com filtros por categoria")
print(f"  12 - Elementos & Criativos: {len(GLASS)+len(BUBBLES)+len(TECH)+len(HOLO)+len(MESH)+len(SCENES_3D)+len(BLOBS)+len(PATTERNS)+len(DECOR)+5} elementos, filtros 10 categorias")
print(f"  13 - Templates & Integracoes (era 15)")
