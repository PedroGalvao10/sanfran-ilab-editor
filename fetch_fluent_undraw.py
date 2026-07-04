"""
Baixa Microsoft Fluent Emoji 3D + unDraw illustrations.
- Fluent: PNG 3D renderizado (parecem objetos reais)
- unDraw: SVG editorial com cor primária trocada para âmbar SanFran iLab
"""
import os
import urllib.request
import urllib.parse
from pathlib import Path

AMBAR = "#F4C430"
UNDRAW_DEFAULT_COLOR = "#6c63ff"  # cor padrão das ilustrações unDraw

ROOT = Path(__file__).parent
OUT_3D    = ROOT / "assets" / "fluent3d"
OUT_ILUS  = ROOT / "assets" / "illustrations"
OUT_3D.mkdir(parents=True, exist_ok=True)
OUT_ILUS.mkdir(parents=True, exist_ok=True)


def fetch(url, dest):
    """Baixa um arquivo binário."""
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (SanFran iLab Brand Tool)"
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
            dest.write_bytes(data)
            return len(data)
    except Exception as e:
        return None


# ════════════════════════════════════════════
# FLUENT EMOJI 3D — Microsoft (PNG)
# ════════════════════════════════════════════
# Formato: (folder_name_no_url, filename_no_extension, label_pt)
# Folder na URL precisa ser url-encoded (espaços → %20)
# Filename usa underscores
FLUENT_3D = [
    ("Light bulb",                "light_bulb",                 "Lâmpada"),
    ("Books",                     "books",                      "Livros"),
    ("Graduation cap",            "graduation_cap",             "Formatura"),
    ("Rocket",                    "rocket",                     "Foguete"),
    ("Brain",                     "brain",                      "Cérebro"),
    ("Gear",                      "gear",                       "Engrenagem"),
    ("Trophy",                    "trophy",                     "Troféu"),
    ("Briefcase",                 "briefcase",                  "Maleta"),
    ("Handshake",                 "handshake",                  "Aperto de mão"),
    ("Globe with meridians",      "globe_with_meridians",       "Globo"),
    ("Direct hit",                "direct_hit",                 "Alvo"),
    ("Chart increasing",          "chart_increasing",           "Gráfico"),
    ("Open book",                 "open_book",                  "Livro aberto"),
    ("Locked",                    "locked",                     "Cadeado"),
    ("Key",                       "key",                        "Chave"),
    ("Magnifying glass tilted left",  "magnifying_glass_tilted_left", "Lupa"),
    ("Hourglass done",            "hourglass_done",             "Ampulheta"),
    ("Memo",                      "memo",                       "Memorando"),
    ("Scroll",                    "scroll",                     "Pergaminho"),
    ("Balance scale",             "balance_scale",              "Balança"),
    ("Crystal ball",              "crystal_ball",               "Bola de cristal"),
    ("Sparkles",                  "sparkles",                   "Brilhos"),
    ("Telescope",                 "telescope",                  "Telescópio"),
    ("Gem stone",                 "gem_stone",                  "Gema"),
    ("Crown",                     "crown",                      "Coroa"),
    ("Newspaper",                 "newspaper",                  "Jornal"),
    ("Money bag",                 "money_bag",                  "Saco de dinheiro"),
    ("Floppy disk",               "floppy_disk",                "Disquete"),
    ("Pushpin",                   "pushpin",                    "Alfinete"),
    ("Megaphone",                 "megaphone",                  "Megafone"),
    ("Bar chart",                 "bar_chart",                  "Barras"),
    ("Laptop",                    "laptop",                     "Laptop"),
    ("Mobile phone",              "mobile_phone",               "Celular"),
    ("Robot",                     "robot",                      "Robô"),
    ("Calendar",                  "calendar",                   "Calendário"),
    ("Printer",                   "printer",                    "Impressora"),
]

BASE_FLUENT = "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets"

print(">>> Baixando Microsoft Fluent Emoji 3D...")
print(f"    {len(FLUENT_3D)} emojis 3D em PNG (renders reais, parecem objetos físicos)\n")

fluent_ok = []
fluent_err = []
for idx, (folder, fname, label_pt) in enumerate(FLUENT_3D, 1):
    folder_url = urllib.parse.quote(folder)
    url = f"{BASE_FLUENT}/{folder_url}/3D/{fname}_3d.png"
    dest = OUT_3D / f"{fname}.png"
    size = fetch(url, dest)
    if size:
        print(f"  [{idx:2d}/{len(FLUENT_3D)}] {fname:30s} OK ({size//1024}KB)")
        fluent_ok.append((fname, label_pt))
    else:
        # Tentar variação: Color (renderizado mais simples)
        url2 = f"{BASE_FLUENT}/{folder_url}/Color/{fname}_color.svg"
        size2 = fetch(url2, OUT_3D / f"{fname}.svg")
        if size2:
            print(f"  [{idx:2d}/{len(FLUENT_3D)}] {fname:30s} OK (Color SVG fallback)")
            fluent_ok.append((fname, label_pt))
        else:
            print(f"  [{idx:2d}/{len(FLUENT_3D)}] {fname:30s} ERRO")
            fluent_err.append(fname)

print(f"\n   Fluent 3D: {len(fluent_ok)}/{len(FLUENT_3D)} baixados")


# ════════════════════════════════════════════
# unDraw illustrations
# Repo público com SVGs editoriais (CC0)
# ════════════════════════════════════════════
# Lista curada de ilustrações relevantes para o tema iLab
UNDRAW_LIST = [
    ("innovation",          "Inovação"),
    ("law",                 "Direito"),
    ("court",               "Tribunal"),
    ("contract",            "Contrato"),
    ("team_collaboration",  "Colaboração"),
    ("ideas_flow",          "Fluxo de ideias"),
    ("research",            "Pesquisa"),
    ("teaching",            "Ensino"),
    ("graduation",          "Formatura"),
    ("startup_life",        "Startup"),
    ("artificial_intelligence","IA"),
    ("data",                "Dados"),
    ("scrum_board",         "Workflow"),
    ("connected_world",     "Conectado"),
    ("public_discussion",   "Discussão"),
]

# unDraw serve SVGs via:
# https://undraw.co/api/illustrations
# Mas usamos o jeito direto: https://undraw.co/illustrations/[slug].svg
# Ou via raw GitHub do repo @undraw-co/undraw (não oficial mas estável)
# Vamos tentar a URL direta primeiro
print("\n>>> Tentando baixar unDraw illustrations...")
undraw_ok = []
undraw_err = []
for slug, label in UNDRAW_LIST:
    # Tentar URL pública direta do unDraw
    url = f"https://undraw.co/api/illustrations/{slug}.svg"
    dest = OUT_ILUS / f"{slug}.svg"
    size = fetch(url, dest)
    if size and size > 200:
        # Trocar cor primária para âmbar
        try:
            content = dest.read_text(encoding="utf-8")
            content = content.replace(UNDRAW_DEFAULT_COLOR, AMBAR)
            content = content.replace(UNDRAW_DEFAULT_COLOR.upper(), AMBAR)
            dest.write_text(content, encoding="utf-8")
            print(f"  [{slug:30s}] OK ({size//1024}KB)")
            undraw_ok.append((slug, label))
        except Exception as e:
            print(f"  [{slug:30s}] OK mas erro ao recolorir: {e}")
            undraw_ok.append((slug, label))
    else:
        # Fallback: tentar URL alternativa
        url2 = f"https://raw.githubusercontent.com/undraw-co/undraw/master/svg/{slug}.svg"
        size2 = fetch(url2, dest)
        if size2 and size2 > 200:
            try:
                content = dest.read_text(encoding="utf-8")
                content = content.replace(UNDRAW_DEFAULT_COLOR, AMBAR)
                content = content.replace(UNDRAW_DEFAULT_COLOR.upper(), AMBAR)
                dest.write_text(content, encoding="utf-8")
                print(f"  [{slug:30s}] OK via fallback ({size2//1024}KB)")
                undraw_ok.append((slug, label))
            except: pass
        else:
            print(f"  [{slug:30s}] FALHOU")
            undraw_err.append(slug)
            if dest.exists():
                dest.unlink()

print(f"\n   unDraw: {len(undraw_ok)}/{len(UNDRAW_LIST)} baixados")


# ════════════════════════════════════════════
# RELATÓRIO FINAL
# ════════════════════════════════════════════
print()
print("=" * 60)
print(f"TOTAL ADICIONADO: {len(fluent_ok) + len(undraw_ok)} novos assets")
print(f"  Fluent Emoji 3D:  {len(fluent_ok)}/{len(FLUENT_3D)}")
print(f"  unDraw illust.:   {len(undraw_ok)}/{len(UNDRAW_LIST)}")
print("=" * 60)
print()
print("Lista para integracao no index.html:")
print()
print("FLUENT_3D_ASSETS = [")
for fname, label in fluent_ok:
    ext = "png" if (OUT_3D / f"{fname}.png").exists() else "svg"
    print(f'    ("{fname}", "{label}", "{ext}"),')
print("]")
print()
print("UNDRAW_ASSETS = [")
for slug, label in undraw_ok:
    print(f'    ("{slug}", "{label}"),')
print("]")
