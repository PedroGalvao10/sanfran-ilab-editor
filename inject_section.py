"""Replace section 04 in index.html with new gallery."""
import re

INDEX = r"C:\Users\soare\.gemini\antigravity\scratch\sanfran-ilab-brand\index.html"
NEW_SECTION = r"C:\Users\soare\.gemini\antigravity\scratch\sanfran-ilab-brand\_section_04.html"

with open(INDEX, encoding="utf-8") as f:
    html = f.read()

with open(NEW_SECTION, encoding="utf-8") as f:
    new_section = f.read()

# Match the old section 04 from comment header through </section>
pattern = re.compile(
    r'<!-- 04 SISTEMA LEX -->\s*<section id="lex">.*?</section>',
    re.DOTALL
)
match = pattern.search(html)
if not match:
    print("ERR: section 04 not found")
    raise SystemExit(1)

print(f"Found old section: {match.start()}-{match.end()} ({match.end()-match.start()} chars)")

new_html = html[:match.start()] + new_section + html[match.end():]

with open(INDEX, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"Replaced. New length: {len(new_html)} (old: {len(html)})")
