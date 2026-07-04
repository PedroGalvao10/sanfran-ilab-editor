"""
Integração final v3:
- Remove cards bubbles (já apagamos os arquivos)
- Adiciona 4 nova categorias na seção 12: OpenMoji, Avatars, Mockups
- Atualiza filtros e contadores
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
INDEX = ROOT / "index.html"

# ─────────────────────────────────────────
# LISTAS COMPLETAS
# ─────────────────────────────────────────
OPENMOJI = [
    ("lightbulb","Lâmpada","Inovação"),("books","Livros","Educação"),
    ("graduation","Formatura","Educação"),("rocket","Foguete","Inovação"),
    ("brain","Cérebro","Inovação"),("gear","Engrenagem","Sistema"),
    ("trophy","Troféu","Conquista"),("briefcase","Maleta","Profissional"),
    ("handshake","Parceria","Comunidade"),("globe","Globo","Global"),
    ("target","Alvo","Dados"),("chart-up","Gráfico","Dados"),
    ("open-book","Livro Aberto","Educação"),("locked","Cadeado","Segurança"),
    ("key","Chave","Segurança"),("search","Lupa","Pesquisa"),
    ("hourglass","Ampulheta","Tempo"),("memo","Memorando","Jurídico"),
    ("scroll","Pergaminho","Jurídico"),("scale","Balança","Jurídico"),
    ("crystal-ball","Bola Cristal","Futuro"),("sparkles","Brilhos","Destaque"),
    ("telescope","Telescópio","Visão"),("gem","Gema","Premium"),
    ("crown","Coroa","Premium"),("newspaper","Jornal","Mídia"),
    ("money-bag","Dinheiro","Negócios"),("floppy","Disquete","Tech"),
    ("pushpin","Alfinete","Workflow"),("megaphone","Megafone","Comunicação"),
    ("bar-chart","Barras","Dados"),("laptop","Laptop","Tech"),
    ("mobile","Celular","Tech"),("robot","Robô","IA"),
    ("calendar","Calendário","Workflow"),("bookmark-tabs","Marcadores","Workflow"),
    ("clipboard","Prancheta","Workflow"),("paperclip","Clipe","Workflow"),
    ("old-key","Chave Antiga","Segurança"),("video-camera","Câmera","Mídia"),
]

AVATARS = [
    ("alex","Alex"),("maria","Maria"),("joao","João"),("camila","Camila"),
    ("rafael","Rafael"),("beatriz","Beatriz"),("lucas","Lucas"),("ana","Ana"),
    ("pedro","Pedro"),("fernanda","Fernanda"),("gustavo","Gustavo"),("juliana","Juliana"),
    ("smile-alex","Alex Smile"),("smile-maria","Maria Smile"),("smile-joao","João Smile"),
    ("smile-camila","Camila Smile"),("smile-rafael","Rafael Smile"),("smile-beatriz","Bia Smile"),
]

MOCKUPS = [
    ("insta-announcement","Post · Anúncio","Instagram 1080x1080"),
    ("insta-quote","Post · Citação","Instagram 1080x1080"),
    ("insta-event","Post · Evento","Instagram 1080x1080"),
    ("slide-cover","Slide · Capa","Apresentação 1920x1080"),
    ("slide-content","Slide · Conteúdo","Apresentação 1920x1080"),
    ("card-front","Cartão · Frente","Cartão 9x5cm"),
    ("card-back","Cartão · Verso","Cartão 9x5cm"),
    ("story-vertical","Story · Vertical","Instagram 1080x1920"),
]


# ─────────────────────────────────────────
# Gerar HTML dos cards
# ─────────────────────────────────────────
def build_openmoji_cards():
    html = ""
    for slug, label, theme in OPENMOJI:
        html += f'''    <div class="el-card el-card-square el-card-openmoji" data-cat="openmoji" data-theme="{theme}">
      <img src="assets/openmoji/{slug}.svg" alt="{label}" class="el-img el-img-openmoji">
      <div class="el-label">
        <span>{label} <span class="el-tag">OpenMoji · {theme}</span></span>
        <span class="el-dl">
          <button class="dl-mini dl-svg" data-asset="{slug}" data-folder="openmoji" data-label="openmoji-{slug}" title="SVG">SVG</button>
          <button class="dl-mini dl-png" data-asset="{slug}" data-folder="openmoji" data-label="openmoji-{slug}" data-size="2048" title="PNG 2048px">PNG</button>
        </span>
      </div>
    </div>
'''
    return html


def build_avatar_cards():
    html = ""
    for slug, name in AVATARS:
        html += f'''    <div class="el-card el-card-square el-card-avatar" data-cat="avatars">
      <img src="assets/avatars/{slug}.svg" alt="{name}" class="el-img el-img-avatar">
      <div class="el-label">
        <span>{name} <span class="el-tag">Persona</span></span>
        <span class="el-dl">
          <button class="dl-mini dl-svg" data-asset="{slug}" data-folder="avatars" data-label="avatar-{slug}" title="SVG">SVG</button>
          <button class="dl-mini dl-png" data-asset="{slug}" data-folder="avatars" data-label="avatar-{slug}" data-size="1024" title="PNG 1024px">PNG</button>
        </span>
      </div>
    </div>
'''
    return html


def build_mockup_cards():
    html = ""
    for slug, label, desc in MOCKUPS:
        # Mockups têm proporções diversas — não forçar square
        size = 3000 if "slide" in slug else (2048 if "card" in slug else 2048)
        html += f'''    <div class="el-card el-card-mockup" data-cat="mockups">
      <div class="el-mockup-wrap">
        <img src="assets/mockups/{slug}.svg" alt="{label}" class="el-img el-img-mockup">
      </div>
      <div class="el-label">
        <span>{label} <span class="el-tag">{desc}</span></span>
        <span class="el-dl">
          <button class="dl-mini dl-svg" data-asset="{slug}" data-folder="mockups" data-label="mockup-{slug}" title="SVG">SVG</button>
          <button class="dl-mini dl-png" data-asset="{slug}" data-folder="mockups" data-label="mockup-{slug}" data-size="{size}" title="PNG {size}px">PNG</button>
        </span>
      </div>
    </div>
'''
    return html


# ─────────────────────────────────────────
# EXECUÇÃO
# ─────────────────────────────────────────
content = INDEX.read_text(encoding="utf-8")

# 1) Remover TODOS os cards de bubbles
pattern_bubble_cards = re.compile(
    r'\s*<div class="el-card[^"]*" data-cat="bubbles"[^>]*>.*?</div>\s*</div>\s*',
    re.DOTALL
)
removed = len(pattern_bubble_cards.findall(content))
content = pattern_bubble_cards.sub("", content)
print(f"Removidos {removed} cards de bubbles")

# 2) Remover botão de filtro bubbles
content = re.sub(
    r'<button class="el-filter" data-cat="bubbles">[^<]*</button>\s*',
    '',
    content
)

# 3) Adicionar novos filtros (após o filter de fluent3d ou após "all")
new_filters = (
    '<button class="el-filter" data-cat="openmoji">🎨 OpenMoji</button>\n    '
    '<button class="el-filter" data-cat="avatars">👤 Personas</button>\n    '
    '<button class="el-filter" data-cat="mockups">📐 Mockups</button>\n    '
)
content = re.sub(
    r'(<button class="el-filter" data-cat="fluent3d">[^<]*</button>\s*)',
    lambda m: m.group(1) + new_filters,
    content,
    count=1
)

# 4) Inserir os novos cards no INÍCIO do .el-grid (após Fluent 3D que já está no início)
new_cards = build_mockup_cards() + build_openmoji_cards() + build_avatar_cards()
# Inserir após o último card Fluent 3D (procuro o pattern do filtro fluent3d primeiro)
# Estratégia: encontrar o último '</div>' do bloco Fluent 3D inicial. Mais simples: inserir logo após o "data-cat=\"fluent3d\"" pattern
# Vou inserir antes do primeiro card com data-cat != fluent3d e != avatars/openmoji/mockups
# Estratégia mais simples: pegar o último card data-cat="fluent3d" e injetar depois dele

# Encontrar a posição do último card fluent3d
last_fluent_match = None
for m in re.finditer(r'<div class="el-card[^"]*" data-cat="fluent3d"[^>]*>.*?</div>\s*</div>\s*', content, re.DOTALL):
    last_fluent_match = m

if last_fluent_match:
    pos = last_fluent_match.end()
    content = content[:pos] + new_cards + content[pos:]
    print(f"Cards novos inseridos após o último Fluent 3D")
else:
    # Fallback: inserir no início do .el-grid
    content = re.sub(
        r'(<section id="elementos">.*?<div class="el-grid">\s*)',
        lambda m: m.group(1) + new_cards,
        content,
        count=1,
        flags=re.DOTALL
    )

# 5) Atualizar contagem total
content = re.sub(
    r'101 elementos criativos',
    f'{101 - removed + len(OPENMOJI) + len(AVATARS) + len(MOCKUPS)} elementos criativos',
    content
)
# Descrição detalhada
content = re.sub(
    r'35 Fluent 3D \+ 8 bubbles \+ 10 tech.*?= 96',
    f'35 Fluent 3D + {len(OPENMOJI)} OpenMoji + {len(AVATARS)} Personas + {len(MOCKUPS)} Mockups + 10 tech + 5 holo + 12 mesh + 6 3D + 8 blobs + 4 patterns + 8 decor = {35+len(OPENMOJI)+len(AVATARS)+len(MOCKUPS)+10+5+12+6+8+4+8}',
    content
)

# 6) CSS extra para novos cards
extra_css = '''
/* === OPENMOJI / AVATARS / MOCKUPS === */
.el-card-openmoji{background:linear-gradient(135deg,#FAF3E0 0%,#fff 100%);padding:0;border:1px solid rgba(244,196,48,.15)}
.el-card-openmoji .el-img-openmoji{width:100%;aspect-ratio:1/1;object-fit:contain;padding:22px;box-sizing:border-box;background:#FFF}
.el-card-openmoji:hover{border-color:#F4C430;box-shadow:0 12px 36px rgba(244,196,48,.2)}
.el-card-openmoji .el-label{background:#FAF3E0;color:#1A1A1A;border-top:1px solid rgba(0,0,0,.06)}
.el-card-openmoji .el-tag{color:#FF6B35;background:rgba(255,107,53,.12)}
.el-card-openmoji .dl-mini{background:rgba(26,26,26,.08);color:#1A1A1A}
.el-card-openmoji .dl-mini:hover{background:#F4C430;color:#1A1A1A}
.el-card-openmoji .dl-mini.dl-png{background:rgba(255,107,53,.18);color:#FF6B35}
.el-card-openmoji .dl-mini.dl-png:hover{background:#FF6B35;color:#fff}

.el-card-avatar{background:linear-gradient(135deg,#fff 0%,#FAF3E0 100%);padding:0;border:1px solid rgba(244,196,48,.15)}
.el-card-avatar .el-img-avatar{width:100%;aspect-ratio:1/1;object-fit:cover}
.el-card-avatar:hover{border-color:#F4C430;box-shadow:0 12px 36px rgba(244,196,48,.2)}
.el-card-avatar .el-label{background:#FAF3E0;color:#1A1A1A;border-top:1px solid rgba(0,0,0,.06)}
.el-card-avatar .el-tag{color:#C41E3A;background:rgba(196,30,58,.1)}
.el-card-avatar .dl-mini{background:rgba(26,26,26,.08);color:#1A1A1A}
.el-card-avatar .dl-mini:hover{background:#F4C430;color:#1A1A1A}
.el-card-avatar .dl-mini.dl-png{background:rgba(196,30,58,.12);color:#C41E3A}
.el-card-avatar .dl-mini.dl-png:hover{background:#C41E3A;color:#fff}

.el-card-mockup{background:#1A1A1A;padding:0;grid-column:span 2}
.el-card-mockup .el-mockup-wrap{background:#0f0f0f;padding:18px;display:flex;align-items:center;justify-content:center}
.el-card-mockup .el-img-mockup{max-width:100%;height:auto;display:block;box-shadow:0 20px 60px rgba(0,0,0,.5);border-radius:6px}
.el-card-mockup .el-label{background:#1A1A1A;color:#F4C430}
.el-card-mockup .el-tag{color:#F4C430;background:rgba(244,196,48,.15)}
@media (max-width: 768px) { .el-card-mockup { grid-column: span 1; } }
'''
content = content.replace("</style>", extra_css + "\n</style>", 1)

INDEX.write_text(content, encoding="utf-8")
print(f"\nTotal adicionado:")
print(f"  OpenMoji:  {len(OPENMOJI)} SVGs")
print(f"  Avatars:   {len(AVATARS)} SVGs (Notion-style + Big Smile)")
print(f"  Mockups:   {len(MOCKUPS)} (Insta, slides, cartão, story)")
print(f"  Removidos: {removed} bubbles")
