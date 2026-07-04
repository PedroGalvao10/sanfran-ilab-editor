"""
Integra 35 Fluent Emoji 3D no brandbook:
- Adiciona como nova categoria 'fluent3d' na seção 12 (Elementos & Criativos)
- Cada item tem download direto do PNG (já é PNG transparente 3D)
- Inclui filtro de tema
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
INDEX = ROOT / "index.html"

# 35 Fluent 3D Emojis baixados (filename, label_pt, theme)
FLUENT_3D = [
    ("light_bulb", "Lâmpada", "Inovação"),
    ("books", "Livros", "Educação"),
    ("graduation_cap", "Formatura", "Educação"),
    ("rocket", "Foguete", "Inovação"),
    ("brain", "Cérebro", "Inovação"),
    ("gear", "Engrenagem", "Sistema"),
    ("trophy", "Troféu", "Conquista"),
    ("briefcase", "Maleta", "Profissional"),
    ("handshake", "Parceria", "Comunidade"),
    ("globe_with_meridians", "Globo", "Global"),
    ("chart_increasing", "Gráfico", "Dados"),
    ("open_book", "Livro Aberto", "Educação"),
    ("locked", "Cadeado", "Segurança"),
    ("key", "Chave", "Segurança"),
    ("magnifying_glass_tilted_left", "Lupa", "Pesquisa"),
    ("hourglass_done", "Ampulheta", "Tempo"),
    ("memo", "Memorando", "Jurídico"),
    ("scroll", "Pergaminho", "Jurídico"),
    ("balance_scale", "Balança", "Jurídico"),
    ("crystal_ball", "Bola de Cristal", "Futuro"),
    ("sparkles", "Brilhos", "Destaque"),
    ("telescope", "Telescópio", "Visão"),
    ("gem_stone", "Gema", "Premium"),
    ("crown", "Coroa", "Premium"),
    ("newspaper", "Jornal", "Mídia"),
    ("money_bag", "Saco de Dinheiro", "Negócios"),
    ("floppy_disk", "Disquete", "Tech"),
    ("pushpin", "Alfinete", "Workflow"),
    ("megaphone", "Megafone", "Comunicação"),
    ("bar_chart", "Barras", "Dados"),
    ("laptop", "Laptop", "Tech"),
    ("mobile_phone", "Celular", "Tech"),
    ("robot", "Robô", "IA"),
    ("calendar", "Calendário", "Workflow"),
    ("printer", "Impressora", "Tech"),
]


def build_fluent_cards():
    """Gera cards de Fluent 3D para inserir na seção 12."""
    cards = ""
    for fname, label, theme in FLUENT_3D:
        cards += f'''    <div class="el-card el-card-square el-card-fluent" data-cat="fluent3d" data-theme="{theme}">
      <img src="assets/fluent3d/{fname}.png" alt="{label}" class="el-img el-img-fluent">
      <div class="el-label">
        <span>{label} <span class="el-tag">3D · {theme}</span></span>
        <span class="el-dl">
          <button class="dl-mini dl-svg" data-asset="{fname}" data-folder="fluent3d" data-label="{fname}-3d" data-ext="png" title="Baixar PNG transparente">PNG</button>
        </span>
      </div>
    </div>
'''
    return cards


def main():
    content = INDEX.read_text(encoding="utf-8")

    # 1) Adicionar filtro "fluent3d" na lista de filtros da seção elementos
    # Localizar o div .el-filters dentro da seção elementos e adicionar botão
    new_filter = '<button class="el-filter" data-cat="fluent3d">🎲 Fluent 3D</button>\n    '

    pattern_filters = re.compile(
        r'(<div class="el-filters">\s*<button class="el-filter active" data-cat="all">Todos</button>\s*)',
        re.DOTALL
    )
    content = pattern_filters.sub(
        lambda m: m.group(1) + new_filter,
        content,
        count=1
    )

    # 2) Inserir os cards Fluent 3D no início do .el-grid (após o opening tag)
    fluent_cards = build_fluent_cards()
    pattern_grid = re.compile(
        r'(<section id="elementos">.*?<div class="el-grid">\s*)',
        re.DOTALL
    )
    content = pattern_grid.sub(
        lambda m: m.group(1) + fluent_cards,
        content,
        count=1
    )

    # 3) Adicionar CSS para .el-card-fluent (fundo neutro, sem padding excessivo)
    extra_css = '''
/* === FLUENT 3D CARDS === */
.el-card-fluent{background:linear-gradient(135deg,#FAF3E0 0%,#fff 100%);padding:0;min-height:auto;border:1px solid rgba(244,196,48,.15)}
.el-card-fluent .el-img-fluent{width:100%;aspect-ratio:1/1;object-fit:contain;padding:24px;box-sizing:border-box;background:transparent}
.el-card-fluent:hover{box-shadow:0 14px 40px rgba(244,196,48,.25);border-color:#F4C430}
.el-card-fluent .el-label{background:#FAF3E0;color:#1A1A1A;border-top:1px solid rgba(0,0,0,.06)}
.el-card-fluent .el-tag{color:#FF6B35;background:rgba(255,107,53,.12)}
.el-card-fluent .dl-mini{background:rgba(26,26,26,.08);color:#1A1A1A}
.el-card-fluent .dl-mini:hover{background:#F4C430;color:#1A1A1A}
.el-card-fluent .dl-mini.dl-png{background:rgba(255,107,53,.18);color:#FF6B35}
.el-card-fluent .dl-mini.dl-png:hover{background:#FF6B35;color:#fff}
'''
    content = content.replace("</style>", extra_css + "\n</style>", 1)

    # 4) Atualizar contagem na descrição da seção 12 (66 → 101)
    content = content.replace(
        "66 elementos criativos",
        "101 elementos criativos"
    )
    content = content.replace(
        "8 bubbles + 10 tech + 5 holo + 12 mesh + 6 3D + 8 blobs + 4 patterns + 8 decor = 61",
        "35 Fluent 3D + 8 bubbles + 10 tech + 5 holo + 12 mesh + 6 3D + 8 blobs + 4 patterns + 8 decor = 96"
    )

    # 5) Atualizar handler de download — agora deve suportar extensão png direto para Fluent 3D
    # O JS atual usa apenas SVG. Vou adicionar handler que detecta data-ext="png"
    new_js_handler = '''
// === Override: Fluent 3D já é PNG, download direto ===
document.addEventListener('click', (e) => {
  const btn = e.target.closest('.dl-mini[data-ext="png"]');
  if (!btn) return;
  e.stopImmediatePropagation();
  e.preventDefault();
  const folder = btn.dataset.folder;
  const asset = btn.dataset.asset;
  const label = btn.dataset.label || asset;
  const url = `assets/${folder}/${asset}.png`;
  fetch(url).then(r => r.blob()).then(blob => {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `${label}.png`;
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    if (window.showDlToast) window.showDlToast(`PNG · ${a.download}`);
  });
}, true); // capture phase para rodar antes do handler genérico
</script>
'''
    # Inserir antes do último </script> (o handler genérico)
    content = re.sub(
        r'(// === Bind nos botões ===)',
        new_js_handler + '\n<script>\n\\1',
        content,
        count=1
    )

    INDEX.write_text(content, encoding="utf-8")
    print("OK: 35 Fluent 3D integrados na secao 12 (filtro 'Fluent 3D')")
    print(f"   Total seção 12: 101 elementos (35 Fluent 3D + 66 criados)")


if __name__ == "__main__":
    main()
