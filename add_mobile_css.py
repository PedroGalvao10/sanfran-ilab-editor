"""
Adiciona bloco completo de responsividade mobile ao index.html.
Cobre 3 breakpoints: 1024px (tablet), 768px (mobile portrait), 480px (small mobile).
"""
from pathlib import Path

INDEX = Path(__file__).parent / "index.html"

MOBILE_CSS = '''
/* ════════════════════════════════════════════════
   RESPONSIVIDADE MOBILE
   1024px tablet · 768px mobile · 480px small
════════════════════════════════════════════════ */

/* Safety global — evita overflow horizontal */
html, body { overflow-x: hidden; max-width: 100vw; }
img, svg { max-width: 100%; height: auto; }

/* ─── TABLET LANDSCAPE (≤ 1024px) ─── */
@media (max-width: 1024px) {
  .hero { padding: 56px 40px 44px; }
  .hero h1 { font-size: 44px; }
  section { padding: 56px 40px; }
  h2 { font-size: 28px; }
  .insta-grid { grid-template-columns: repeat(2, 1fr) !important; }
  .slides-grid { grid-template-columns: 1fr !important; }
  .icons-grid { grid-template-columns: repeat(6, 1fr) !important; }
  .elements-grid { grid-template-columns: repeat(3, 1fr) !important; }
  .ic-grid { grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)) !important; }
  .el-grid { grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)) !important; }
}

/* ─── MOBILE / TABLET PORTRAIT (≤ 768px) ─── */
@media (max-width: 768px) {
  /* HERO */
  .hero { padding: 44px 20px 36px; }
  .hero h1 { font-size: 36px; line-height: 1.05; }
  .hero-sub { font-size: 14px; }
  .hero-tag { font-size: 10px; padding: 4px 10px; margin-bottom: 14px; }

  /* TOC — links menores e cabíveis */
  .toc { gap: 6px; margin-top: 22px; }
  .toc a { font-size: 10px; padding: 6px 10px; }

  /* SECTIONS — padding reduzido */
  section { padding: 44px 20px; }
  h2 { font-size: 22px; line-height: 1.15; }
  .section-label { font-size: 10px; letter-spacing: 2px; }
  .section-desc { font-size: 13px; margin-bottom: 28px; }

  /* GRIDS HARDCODED → 1-2 colunas */
  .insta-grid { grid-template-columns: 1fr !important; gap: 18px; }
  .slides-grid { grid-template-columns: 1fr !important; }
  .icons-grid { grid-template-columns: repeat(4, 1fr) !important; gap: 8px; }
  .elements-grid { grid-template-columns: repeat(2, 1fr) !important; gap: 12px; }

  /* GRIDS DINÂMICOS */
  .ic-grid { grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)) !important; gap: 10px; }
  .ic-card { padding: 14px 8px; }
  .ic-name { font-size: 11px; }
  .ic-cat { font-size: 8px; }
  .el-grid { grid-template-columns: 1fr !important; gap: 14px; }
  .canva-grid { grid-template-columns: 1fr !important; }
  .canva-tools-grid { grid-template-columns: 1fr !important; }

  /* FILTROS — mais compactos */
  .ic-tabs, .ic-filters, .el-filters { gap: 4px; }
  .ic-tab { font-size: 10px; padding: 8px 12px; }
  .ic-filter, .el-filter { font-size: 9px; padding: 6px 10px; }

  /* CARDS DE DOWNLOAD */
  .dl-btn { font-size: 9px; padding: 5px 8px; max-width: none; }
  .dl-mini { font-size: 8px; padding: 3px 6px; }

  /* MOCKUPS — sempre 1 coluna */
  .el-card-mockup { grid-column: span 1 !important; }
  .el-card-mockup .el-mockup-wrap { padding: 12px; }

  /* PALETTE / TIPOGRAFIA / outros grids inline */
  [style*="grid-template-columns:repeat(8"], [style*="grid-template-columns: repeat(8"] {
    grid-template-columns: repeat(4, 1fr) !important;
  }
  [style*="grid-template-columns:repeat(6"], [style*="grid-template-columns: repeat(6"] {
    grid-template-columns: repeat(3, 1fr) !important;
  }
  [style*="grid-template-columns:repeat(4"], [style*="grid-template-columns: repeat(4"] {
    grid-template-columns: repeat(2, 1fr) !important;
  }
  [style*="grid-template-columns:1fr 1fr"], [style*="grid-template-columns: 1fr 1fr"] {
    grid-template-columns: 1fr !important;
  }
  [style*="grid-template-columns:repeat(2"], [style*="grid-template-columns: repeat(2"] {
    grid-template-columns: 1fr !important;
  }

  /* Tipografia gigante (180px etc.) */
  [style*="font-size: 180px"], [style*="font-size:180px"] { font-size: 80px !important; }
  [style*="font-size: 120px"], [style*="font-size:120px"] { font-size: 60px !important; }
  [style*="font-size: 96px"], [style*="font-size:96px"] { font-size: 48px !important; }
  [style*="font-size: 64px"], [style*="font-size:64px"] { font-size: 36px !important; }
  [style*="font-size: 48px"], [style*="font-size:48px"] { font-size: 30px !important; }

  /* Padding gigante inline */
  [style*="padding: 56px"], [style*="padding:56px"] { padding: 24px !important; }
  [style*="padding: 72px"], [style*="padding:72px"] { padding: 28px !important; }
  [style*="padding: 48px"], [style*="padding:48px"] { padding: 20px !important; }

  /* FOOTER */
  footer { padding: 32px 20px !important; }
  footer .logo { font-size: 24px !important; }

  /* LEX SLIDES e cards */
  .lex-card { padding: 16px !important; }
  .lex-card svg { width: 80px !important; height: 80px !important; }

  /* CANVA CARDS */
  .canva-thumb { aspect-ratio: 4/3; }
  .canva-plus { font-size: 48px; }

  /* TOAST */
  #dl-toast, #dl-toast-v2 { left: 16px; right: 16px; transform: translateY(120%); max-width: none; }
  #dl-toast.show, #dl-toast-v2.show { transform: translateY(0); }
}

/* ─── SMALL MOBILE (≤ 480px) ─── */
@media (max-width: 480px) {
  .hero { padding: 36px 16px 28px; }
  .hero h1 { font-size: 30px; }
  section { padding: 36px 16px; }
  h2 { font-size: 20px; }

  /* TOC ainda mais compacto */
  .toc { gap: 4px; }
  .toc a { font-size: 9px; padding: 5px 8px; letter-spacing: 0; }

  /* Ícones em 3 colunas */
  .ic-grid { grid-template-columns: repeat(3, 1fr) !important; gap: 8px; }
  .icons-grid { grid-template-columns: repeat(3, 1fr) !important; gap: 6px; }
  .ic-card { padding: 10px 6px; }
  .ic-icon-wrap { height: 48px; }
  .ic-img { width: 36px; height: 36px; }

  .elements-grid { grid-template-columns: 1fr !important; }

  /* Tabs em coluna */
  .ic-tabs { flex-direction: column; }
  .ic-tab { width: 100%; }

  /* Botões dl em coluna no card de ícone */
  .ic-actions { flex-direction: row; }
  .dl-btn { padding: 4px 6px; font-size: 9px; }

  /* Tipografia muito grande */
  [style*="font-size: 96px"], [style*="font-size:96px"] { font-size: 38px !important; }
  [style*="font-size: 64px"], [style*="font-size:64px"] { font-size: 28px !important; }
  [style*="font-size: 48px"], [style*="font-size:48px"] { font-size: 24px !important; }
}
'''

content = INDEX.read_text(encoding="utf-8")

# Remover qualquer bloco mobile anterior (idempotência)
import re
content = re.sub(
    r'/\* ═+\s*RESPONSIVIDADE MOBILE.*?════════════════════════════════════════════════ \*/\s*',
    '',
    content,
    flags=re.DOTALL
)
# Limpar qualquer @media residual de versão anterior
# (Conservar a única que já existia para .el-card-mockup, será sobrescrita pela nova)

# Inserir antes do último </style>
content = content.replace("</style>", MOBILE_CSS + "\n</style>", 1)

INDEX.write_text(content, encoding="utf-8")
print("OK: bloco de responsividade mobile adicionado")
print("  - 3 breakpoints: 1024px / 768px / 480px")
print("  - Cobre: hero, sections, grids (5 tipos), filtros, tipografia inline, padding inline")
