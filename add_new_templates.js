const fs = require('fs');
const path = require('path');

// 1. brand.json
const brandPath = path.join(__dirname, 'brand-api', 'brand.json');
let brand = JSON.parse(fs.readFileSync(brandPath, 'utf8'));

brand.templates.feed_carrossel = {
  name: "Feed Carrossel / Quadrado",
  useCase: "Slides aprofundados pro Instagram/LinkedIn",
  format: "1:1 (Post)",
  hasPhoto: false,
  fields: ["badge_top", "headline", "body_text", "page_indicator", "brand_footer"]
};

brand.templates.video_reel = {
  name: "Capa / Molde de Reel",
  useCase: "Thumbnail ou frame lateral para vídeos curtos",
  format: "9:16 (Vídeo)",
  hasPhoto: false,
  fields: ["safe_title", "speaker_badge", "topic_chip"]
};

fs.writeFileSync(brandPath, JSON.stringify(brand, null, 2), 'utf8');


// 2. index.html
const indexPath = path.join(__dirname, 'index.html');
let html = fs.readFileSync(indexPath, 'utf8');

// Injetar o CSS
const cssToInject = `
    /* =================================== */
    /* LAYOUTS 1:1 (FEED/CARROSSEL)        */
    /* =================================== */
    .feed-post {
      width: 320px; height: 320px; /* 1080x1080 na escala viewport */
      border-radius: 16px; overflow: hidden;
      position: relative;
      background: var(--black-deep);
      box-shadow: 0 16px 40px rgba(0,0,0,.12);
      border: 1px solid rgba(255,255,255,0.06);
      padding: 24px;
      display: flex; flex-direction: column;
      transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.4s ease;
      transform-style: preserve-3d;
    }
    .feed-post:hover {
      transform: translateY(-6px) scale(1.02);
      box-shadow: 0 28px 50px rgba(0,0,0,.25);
    }
    .feed-post::after {
      content: ''; position: absolute; inset: 0; pointer-events: none;
      background-image: linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
      background-size: 16px 16px; z-index: 1; border-radius: 16px;
    }
    .feed-post .fp-badge {
      background: rgba(255, 107, 53, 0.25); backdrop-filter: blur(12px) saturate(180%);
      border: 1px solid rgba(255, 255, 255, 0.15); color: #fff;
      font-family: 'JetBrains Mono', monospace; font-size: 9px; font-weight: 700;
      letter-spacing: 1.5px; text-transform: uppercase;
      padding: 6px 14px; border-radius: 16px; width: fit-content; margin-bottom: 20px;
      position: relative; z-index: 2;
    }
    .feed-post .fp-headline {
      font-family: 'Poppins', sans-serif; font-weight: 900; font-size: 26px;
      line-height: 1.1; color: #fff; margin-bottom: 12px; letter-spacing: -1px;
      position: relative; z-index: 2;
    }
    .feed-post .fp-body {
      font-family: 'Montserrat', sans-serif; font-weight: 500; font-size: 11px;
      line-height: 1.5; color: rgba(255,255,255,0.75);
      position: relative; z-index: 2;
    }
    .feed-post .fp-footer {
      margin-top: auto; display: flex; justify-content: space-between; align-items: center;
      border-top: 1px solid rgba(255,255,255,0.1); padding-top: 14px;
      position: relative; z-index: 2;
    }
    .feed-post .fp-page {
      font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--yellow);
    }
    .feed-post .fp-brand {
      font-family: 'Poppins', sans-serif; font-weight: 900; font-size: 13px; color: #fff;
    }
    .feed-post .fp-brand em {
      font-style: normal; background: linear-gradient(90deg, #F4C430, #FF6B35); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }

    /* =================================== */
    /* LAYOUT VIDEO (REEL/THUMBNAIL)       */
    /* =================================== */
    .video-reel {
      width: 180px; height: 320px;
      border-radius: 16px; overflow: hidden; position: relative;
      background: var(--black-deep); /* placeholder para video real */
      box-shadow: 0 16px 40px rgba(0,0,0,.12);
      border: 1px solid rgba(255,255,255,0.06);
      display: flex; flex-direction: column; justify-content: space-between;
      padding: 18px 12px;
      transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
    }
    .video-reel:hover { transform: translateY(-6px) scale(1.02); }
    .video-reel::before {
      content: ''; position: absolute; inset: 0; pointer-events: none;
      background: linear-gradient(180deg, rgba(17,17,17,0.85) 0%, transparent 20%, transparent 75%, rgba(17,17,17,0.95) 100%);
      z-index: 1;
    }
    .video-reel::after {
      content: '▶'; position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%);
      font-size: 24px; color: rgba(255,255,255,0.3); z-index: 0;
    }
    .video-reel .vr-title {
      position: relative; z-index: 2; text-align: center;
      font-family: 'Poppins', sans-serif; font-weight: 900; font-size: 15px; color: #fff; line-height: 1.1;
      text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }
    .video-reel .vr-bottom {
      position: relative; z-index: 2; display: flex; flex-direction: column; gap: 8px;
    }
    .video-reel .vr-speaker {
      background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(12px) saturate(180%);
      border: 1px solid rgba(255, 255, 255, 0.3); color: #fff;
      font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 10px;
      padding: 6px 12px; border-radius: 12px; width: fit-content;
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .video-reel .vr-chip {
      background: rgba(244, 196, 48, 0.2); border: 1px solid rgba(244,196,48,0.4); color: var(--yellow);
      font-family: 'JetBrains Mono', monospace; font-size: 8px; font-weight: 700;
      padding: 4px 10px; border-radius: 10px; width: fit-content; text-transform: uppercase; letter-spacing: 1px;
    }
`;

// Insert CSS just before .icons-grid (around line 1300)
html = html.replace('.icons-grid {', cssToInject + '\n    .icons-grid {');


// HTML a injetar (Novo grupo no DOM do template gallery)
const htmlToInject = `
      <!-- FORMATOS EXTRAS -->
      <h3 style="margin: 40px 0 20px; font-family: 'Poppins', sans-serif; color: var(--black); font-size: 24px;">Novos Formatos</h3>
      <div class="story-grid" style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 40px; align-items: start;">
        
        <!-- Carrossel -->
        <div class="story-wrap" style="grid-column: span 2;">
          <div class="story-label">Feed Carrossel (1080x1080)</div>
          <div class="feed-post" id="tpl-feed_carrossel" onclick="loadTemplateToEditor('feed_carrossel', this)">
            <div class="fp-badge" id="dyn-badge_top">Artigo</div>
            <div class="fp-headline" id="dyn-headline">Vieses algorítmicos em decisões judiciais</div>
            <div class="fp-body" id="dyn-body_text">Uma análise empírica de 2.400 sentenças brasileiras mostra que o uso de sistemas genéricos de IA em tribunais de primeira instância tende a replicar precedentes enviesados.</div>
            <div class="fp-footer">
              <div class="fp-brand" id="dyn-brand_footer">SanFran <em>iLab</em></div>
              <div class="fp-page" id="dyn-page_indicator">01/05</div>
            </div>
          </div>
        </div>

        <!-- Reel Capa -->
        <div class="story-wrap">
          <div class="story-label">Video Reel (1080x1920)</div>
          <div class="video-reel" id="tpl-video_reel" onclick="loadTemplateToEditor('video_reel', this)">
            <div class="vr-title" id="dyn-safe_title">Como fazer Prompt de Contrato</div>
            <div class="vr-bottom">
              <div class="vr-speaker" id="dyn-speaker_badge">Prof. Silva</div>
              <div class="vr-chip" id="dyn-topic_chip">TUTORIAL</div>
            </div>
          </div>
        </div>
      </div>
`;

// Replace right before the </section> of the story gallery
html = html.replace('<!-- INJECT_NEW_TEMPLATES_HERE -->', htmlToInject); // Se nao tiver a flag, faremos um fallback

if (!html.includes('<!-- INJECT_NEW_TEMPLATES_HERE -->')) {
    // Insere depois da div story-grid que termina a seção (gambiarra safe é inserir antes da tag section fechar se não tem mais nada)
    html = html.replace(/(<\/div>\s*<\/section>\s*<!-- ELEMENTS -->)/, htmlToInject + '\n      $1');
}

// Injetar lógica no iLabRender no script JS (linha ~3800)
const scriptToInject = `
      } else if (tpl === 'feed_carrossel') {
        if (f.badge_top) base.querySelector('#dyn-badge_top').innerText = f.badge_top;
        if (f.headline) base.querySelector('#dyn-headline').innerText = f.headline;
        if (f.body_text) base.querySelector('#dyn-body_text').innerText = f.body_text;
        if (f.page_indicator) base.querySelector('#dyn-page_indicator').innerText = f.page_indicator;
        if (f.brand_footer) base.querySelector('#dyn-brand_footer').innerHTML = f.brand_footer;
      } else if (tpl === 'video_reel') {
        if (f.safe_title) base.querySelector('#dyn-safe_title').innerText = f.safe_title;
        if (f.speaker_badge) base.querySelector('#dyn-speaker_badge').innerText = f.speaker_badge;
        if (f.topic_chip) base.querySelector('#dyn-topic_chip').innerText = f.topic_chip;
`;

html = html.replace(/(\} else if \(tpl === 'dica'\) \{[\s\S]*?\})/, '$1' + scriptToInject);


fs.writeFileSync(indexPath, html, 'utf8');
console.log('Templates Carrossel e Reel adicionados com sucesso ao HTML e JSON!');
