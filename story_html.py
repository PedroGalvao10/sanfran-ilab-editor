import re

path = r'C:\Users\soare\.gemini\antigravity\scratch\sanfran-ilab-brand\index.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

# Find the stories section (HTML body part)
stories_sec_start = html.find('<section id="stories">')
stories_sec_end = html.find('</section>', stories_sec_start) + len('</section>')

new_stories_html = '''<section id="stories">
  <div class="section-label">05 — Instagram Stories</div>
  <h2>Stories — 3 layouts</h2>
  <p class="section-desc">Molduras 9:16 para aplicar fotos de eventos, reposts e reels. A área quadriculada representa onde a foto entra.</p>

  <div class="story-grid">

    <!-- A: ENCONTRO PRESENCIAL / ONLINE -->
    <div class="story-wrap">
      <div class="story-label">A · Encontro Presencial / Online</div>
      <div class="story story-encontro">
        <!-- photo placeholder -->
        <div class="photo-ph"></div>
        <!-- top brand bar -->
        <div class="se-brand-bar">
          <div class="se-logo">SanFran <em>iLab</em></div>
          <div class="se-handle">@sanfran.ilab</div>
        </div>
        <!-- badge type -->
        <div class="se-badge">Encontro Presencial</div>
        <!-- bottom overlay content -->
        <div class="se-bottom">
          <div class="se-type">iLab · Evento</div>
          <div class="se-divider"></div>
          <div class="se-title">Nome do<br>Evento</div>
          <div class="se-meta">📅 Data · Local · FD-USP</div>
        </div>
      </div>
    </div>

    <!-- B: NOVIDADES / REPOST -->
    <div class="story-wrap">
      <div class="story-label">B · Novidades / Repost</div>
      <div class="story story-novidade">
        <!-- top bar -->
        <div class="sn-top-bar">
          <div class="sn-label">Novidades</div>
          <div class="sn-logo">iLab</div>
        </div>
        <!-- gradient accent line -->
        <div class="sn-accent"></div>
        <!-- bordered photo frame -->
        <div class="sn-photo-frame">
          <div class="photo-ph"></div>
        </div>
        <!-- repost attribution -->
        <div class="sn-repost">
          <div class="sn-from">Reposto de</div>
          <div class="sn-account">@conta_original</div>
        </div>
        <!-- tags -->
        <div class="sn-tags">
          <span>#Direito</span>
          <span>#Inovação</span>
          <span>#IA</span>
        </div>
        <!-- footer bar -->
        <div class="sn-footer">
          <div class="sn-brand"><span class="ni">i</span><span class="nlab">Lab</span></div>
          <div class="sn-handle">@sanfran.ilab</div>
        </div>
      </div>
    </div>

    <!-- C: REEL / DESTAQUE -->
    <div class="story-wrap">
      <div class="story-label">C · Reel / Destaque</div>
      <div class="story story-reel">
        <!-- full-bleed photo -->
        <div class="photo-ph"></div>
        <!-- gradient overlay -->
        <div class="sr-overlay"></div>
        <!-- top left logo -->
        <div class="sr-logo">SanFran <em>iLab</em></div>
        <!-- top right badge -->
        <div class="sr-badge">Destaque</div>
        <!-- center headline -->
        <div class="sr-center">
          <div class="sr-supertitle">iLab · 2026</div>
          <div class="sr-headline">Título do<br>Reel Aqui</div>
        </div>
        <!-- bottom CTA -->
        <div class="sr-bottom">
          <a class="sr-cta" href="#">Ver mais no perfil →</a>
          <div class="sr-footer">
            <div class="sr-handle">@sanfran.ilab</div>
            <div class="sr-dots">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</section>'''

html = html[:stories_sec_start] + new_stories_html + html[stories_sec_end:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

print('Stories HTML replaced.')
print('Templates present:')
for t in ['story-encontro', 'story-novidade', 'story-reel', 'photo-ph', 'Encontro Presencial']:
    print(f'  {t}: {"OK" if t in html else "MISSING"}')
