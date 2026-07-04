import re

path = r'C:\Users\soare\.gemini\antigravity\scratch\sanfran-ilab-brand\index.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

story_start = html.find('    .story-grid {')
icons_start = html.find('\n    .icons-grid {', story_start)

new_story_css = """    /* == STORIES — PHOTO FRAME TEMPLATES == */
    .story-grid {
      display: grid;
      grid-template-columns: repeat(3, 180px);
      gap: 32px;
    }
    .story-wrap { display: flex; flex-direction: column; gap: 10px; }
    .story-label {
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase;
      color: var(--gray-text);
    }
    .story {
      width: 180px; height: 320px;
      border-radius: 12px; overflow: hidden;
      position: relative;
      box-shadow: 0 12px 32px rgba(0,0,0,.18);
    }
    /* Photo placeholder checkerboard */
    .photo-ph {
      position: absolute; inset: 0;
      background: repeating-conic-gradient(#c8c8c8 0% 25%, #e0e0e0 0% 50%) 0 0 / 18px 18px;
    }
    .photo-ph::after {
      content: '\\1F4F7';
      position: absolute; top: 50%; left: 50%;
      transform: translate(-50%,-50%);
      font-size: 28px; opacity: .35;
    }

    /* A: ENCONTRO (presencial / online) */
    .story-encontro .photo-ph { top: 0; height: 70%; }
    .story-encontro .se-brand-bar {
      position: absolute; top: 0; left: 0; right: 0; height: 38px;
      background: linear-gradient(180deg, rgba(17,17,17,.75) 0%, transparent 100%);
      display: flex; align-items: center; justify-content: space-between;
      padding: 0 12px; z-index: 2;
    }
    .story-encontro .se-logo {
      font-family: 'Poppins', sans-serif; font-weight: 900; font-size: 10px; color: #fff;
    }
    .story-encontro .se-logo em {
      font-style: normal;
      background: linear-gradient(90deg,#F4C430,#FF6B35);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .story-encontro .se-handle {
      font-family: 'JetBrains Mono', monospace; font-size: 7px;
      color: rgba(255,255,255,.5); letter-spacing: .5px;
    }
    .story-encontro .se-badge {
      position: absolute; top: 42px; left: 12px; z-index: 2;
      background: var(--orange); color: #fff;
      font-family: 'JetBrains Mono', monospace;
      font-size: 7px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;
      padding: 3px 8px; border-radius: 3px;
    }
    .story-encontro .se-bottom {
      position: absolute; bottom: 0; left: 0; right: 0; height: 38%;
      background: linear-gradient(0deg, #111 0%, rgba(17,17,17,.92) 65%, transparent 100%);
      display: flex; flex-direction: column; justify-content: flex-end;
      padding: 0 14px 14px; z-index: 2;
    }
    .story-encontro .se-type {
      font-family: 'JetBrains Mono', monospace; font-size: 8px;
      letter-spacing: 2px; text-transform: uppercase; color: var(--yellow); margin-bottom: 3px;
    }
    .story-encontro .se-divider {
      width: 28px; height: 2px;
      background: linear-gradient(90deg,#F4C430,#FF6B35); margin-bottom: 5px;
    }
    .story-encontro .se-title {
      font-family: 'Poppins', sans-serif; font-weight: 900;
      font-size: 16px; line-height: 1.1; color: #fff; margin-bottom: 5px;
    }
    .story-encontro .se-meta {
      font-family: 'JetBrains Mono', monospace; font-size: 7.5px;
      color: rgba(255,255,255,.5); letter-spacing: .5px;
    }

    /* B: NOVIDADES / REPOST */
    .story-novidade { background: var(--warm-white); }
    .story-novidade .sn-top-bar {
      position: absolute; top: 0; left: 0; right: 0; height: 44px;
      background: var(--black-deep);
      display: flex; align-items: center; justify-content: space-between;
      padding: 0 12px; z-index: 2;
    }
    .story-novidade .sn-label {
      font-family: 'JetBrains Mono', monospace; font-size: 9px; font-weight: 700;
      letter-spacing: 2px; text-transform: uppercase; color: var(--yellow);
    }
    .story-novidade .sn-logo {
      font-family: 'Poppins', sans-serif; font-weight: 900; font-size: 9px; color: #fff;
    }
    .story-novidade .sn-accent {
      position: absolute; top: 44px; left: 0; right: 0; height: 3px;
      background: linear-gradient(90deg,#F4C430,#FF6B35,#C41E3A); z-index: 2;
    }
    .story-novidade .sn-photo-frame {
      position: absolute; top: 54px; left: 12px; right: 12px; height: 156px;
      border: 2px solid rgba(255,107,53,.35); border-radius: 6px; overflow: hidden; z-index: 1;
    }
    .story-novidade .sn-photo-frame .photo-ph::after { font-size: 20px; }
    .story-novidade .sn-repost {
      position: absolute; top: 216px; left: 12px; right: 12px; z-index: 2;
    }
    .story-novidade .sn-from {
      font-family: 'JetBrains Mono', monospace; font-size: 7px;
      letter-spacing: 1px; text-transform: uppercase; color: var(--gray-text); margin-bottom: 3px;
    }
    .story-novidade .sn-account {
      font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 11px; color: var(--black);
    }
    .story-novidade .sn-tags {
      position: absolute; top: 252px; left: 12px; z-index: 2; display: flex; gap: 5px;
    }
    .story-novidade .sn-tags span {
      font-family: 'JetBrains Mono', monospace; font-size: 7px;
      letter-spacing: .5px; color: var(--orange);
    }
    .story-novidade .sn-footer {
      position: absolute; bottom: 0; left: 0; right: 0; height: 40px;
      background: var(--black-deep);
      display: flex; align-items: center; justify-content: space-between;
      padding: 0 12px; z-index: 2;
    }
    .story-novidade .sn-brand {
      font-family: 'Poppins', sans-serif; font-weight: 900; font-size: 10px;
    }
    .story-novidade .sn-brand .ni { color: var(--yellow); }
    .story-novidade .sn-brand .nlab { color: #fff; }
    .story-novidade .sn-handle {
      font-family: 'JetBrains Mono', monospace; font-size: 7px;
      color: rgba(255,255,255,.45); letter-spacing: .5px;
    }

    /* C: REEL DESTAQUE — full bleed */
    .story-reel .photo-ph { inset: 0; }
    .story-reel .sr-overlay {
      position: absolute; inset: 0;
      background: linear-gradient(180deg,
        rgba(17,17,17,.22) 0%, transparent 28%,
        transparent 44%, rgba(17,17,17,.55) 68%, rgba(17,17,17,.90) 100%);
      z-index: 1;
    }
    .story-reel .sr-logo {
      position: absolute; top: 12px; left: 12px; z-index: 2;
      font-family: 'Poppins', sans-serif; font-weight: 900; font-size: 10px; color: #fff;
    }
    .story-reel .sr-logo em {
      font-style: normal; background: linear-gradient(90deg,#F4C430,#FF6B35);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .story-reel .sr-badge {
      position: absolute; top: 12px; right: 12px; z-index: 2;
      background: linear-gradient(90deg,#FF6B35,#C41E3A); color: #fff;
      font-family: 'JetBrains Mono', monospace; font-size: 7px; font-weight: 700;
      letter-spacing: 1.5px; text-transform: uppercase;
      padding: 3px 8px; border-radius: 3px;
    }
    .story-reel .sr-center {
      position: absolute; top: 50%; left: 14px; right: 14px;
      transform: translateY(-50%); z-index: 2; text-align: center;
    }
    .story-reel .sr-supertitle {
      font-family: 'JetBrains Mono', monospace; font-size: 7.5px;
      letter-spacing: 2px; text-transform: uppercase; color: var(--yellow); margin-bottom: 5px;
    }
    .story-reel .sr-headline {
      font-family: 'Poppins', sans-serif; font-weight: 900;
      font-size: 18px; line-height: 1.1; color: #fff;
    }
    .story-reel .sr-bottom {
      position: absolute; bottom: 0; left: 0; right: 0; padding: 0 14px 14px; z-index: 2;
    }
    .story-reel .sr-cta {
      display: block; text-align: center;
      background: linear-gradient(90deg,#F4C430,#FF6B35); color: var(--black);
      font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 9px;
      padding: 7px; border-radius: 20px; margin-bottom: 8px;
    }
    .story-reel .sr-footer {
      display: flex; justify-content: space-between; align-items: center;
    }
    .story-reel .sr-handle {
      font-family: 'JetBrains Mono', monospace; font-size: 7px;
      color: rgba(255,255,255,.5); letter-spacing: .5px;
    }
    .story-reel .sr-dots { display: flex; gap: 3px; }
    .story-reel .sr-dots span {
      width: 4px; height: 4px; border-radius: 50%; background: rgba(255,255,255,.3);
    }
    .story-reel .sr-dots span:first-child {
      background: var(--yellow); width: 12px; border-radius: 2px;
    }

"""

html = html[:story_start] + new_story_css + html[icons_start:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

print('Story CSS replaced successfully.')
for cls in ['story-encontro', 'story-novidade', 'story-reel', 'photo-ph']:
    print(f'  .{cls}: {"OK" if cls in html else "MISSING"}')
