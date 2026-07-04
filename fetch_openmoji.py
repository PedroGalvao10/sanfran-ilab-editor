"""
Baixa OpenMoji (SVG colorido open-source).
Codepoint hex via CDN público.
"""
import urllib.request
from pathlib import Path

OUT = Path(__file__).parent / "assets" / "openmoji"
OUT.mkdir(parents=True, exist_ok=True)

# (codepoint, slug, label_pt, theme)
OPENMOJI = [
    ("1F4A1", "lightbulb",     "Lâmpada",         "Inovação"),
    ("1F4DA", "books",         "Livros",          "Educação"),
    ("1F393", "graduation",    "Formatura",       "Educação"),
    ("1F680", "rocket",        "Foguete",         "Inovação"),
    ("1F9E0", "brain",         "Cérebro",         "Inovação"),
    ("2699",  "gear",          "Engrenagem",      "Sistema"),
    ("1F3C6", "trophy",        "Troféu",          "Conquista"),
    ("1F4BC", "briefcase",     "Maleta",          "Profissional"),
    ("1F91D", "handshake",     "Parceria",        "Comunidade"),
    ("1F30D", "globe",         "Globo",           "Global"),
    ("1F3AF", "target",        "Alvo",            "Dados"),
    ("1F4C8", "chart-up",      "Gráfico",         "Dados"),
    ("1F4D6", "open-book",     "Livro Aberto",    "Educação"),
    ("1F512", "locked",        "Cadeado",         "Segurança"),
    ("1F511", "key",           "Chave",           "Segurança"),
    ("1F50D", "search",        "Lupa",            "Pesquisa"),
    ("23F3",  "hourglass",     "Ampulheta",       "Tempo"),
    ("1F4DD", "memo",          "Memorando",       "Jurídico"),
    ("1F4DC", "scroll",        "Pergaminho",      "Jurídico"),
    ("2696",  "scale",         "Balança",         "Jurídico"),
    ("1F52E", "crystal-ball",  "Bola de Cristal", "Futuro"),
    ("2728",  "sparkles",      "Brilhos",         "Destaque"),
    ("1F52D", "telescope",     "Telescópio",      "Visão"),
    ("1F48E", "gem",           "Gema",            "Premium"),
    ("1F451", "crown",         "Coroa",           "Premium"),
    ("1F4F0", "newspaper",     "Jornal",          "Mídia"),
    ("1F4B0", "money-bag",     "Saco Dinheiro",   "Negócios"),
    ("1F4BE", "floppy",        "Disquete",        "Tech"),
    ("1F4CC", "pushpin",       "Alfinete",        "Workflow"),
    ("1F4E2", "megaphone",     "Megafone",        "Comunicação"),
    ("1F4CA", "bar-chart",     "Barras",          "Dados"),
    ("1F4BB", "laptop",        "Laptop",          "Tech"),
    ("1F4F1", "mobile",        "Celular",         "Tech"),
    ("1F916", "robot",         "Robô",            "IA"),
    ("1F4C5", "calendar",      "Calendário",      "Workflow"),
    ("1F4D1", "bookmark-tabs", "Marcadores",      "Workflow"),
    ("1F4CB", "clipboard",     "Prancheta",       "Workflow"),
    ("1F4CE", "paperclip",     "Clipe",           "Workflow"),
    ("1F5DD", "old-key",       "Chave Antiga",    "Segurança"),
    ("1F4F9", "video-camera",  "Câmera",          "Mídia"),
]

CDN = "https://cdn.jsdelivr.net/gh/hfg-gmuend/openmoji@latest/color/svg"

def fetch(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read()
            dest.write_bytes(data)
            return len(data)
    except Exception as e:
        return None

print(f">>> OpenMoji ({len(OPENMOJI)} itens via jsDelivr CDN)\n")
ok, err = [], []
for idx, (hex_cp, slug, label, theme) in enumerate(OPENMOJI, 1):
    url = f"{CDN}/{hex_cp}.svg"
    dest = OUT / f"{slug}.svg"
    size = fetch(url, dest)
    if size and size > 200:
        ok.append((slug, label, theme))
        print(f"  [{idx:2d}/{len(OPENMOJI)}] {slug:18s} OK ({size//1024}KB)")
    else:
        err.append(slug)
        print(f"  [{idx:2d}/{len(OPENMOJI)}] {slug:18s} ERRO")

print()
print(f"OpenMoji: {len(ok)}/{len(OPENMOJI)} baixados")
print()
print("OPENMOJI_ASSETS = [")
for slug, label, theme in ok:
    print(f'    ("{slug}", "{label}", "{theme}"),')
print("]")
