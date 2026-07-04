const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, 'index.html');
let content = fs.readFileSync(filePath, 'utf8');

// 1. story base
content = content.replace(
  /\.story \{\s+width: 180px; height: 320px;\s+border-radius: 12px; overflow: hidden;\s+position: relative;\s+box-shadow: 0 12px 32px rgba\(0,0,0,\.18\);\s+\}/,
  `.story {
      width: 180px; height: 320px;
      border-radius: 16px; overflow: hidden;
      position: relative;
      box-shadow: 0 16px 40px rgba(0,0,0,.12);
      transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.4s ease;
      transform-style: preserve-3d;
      border: 1px solid rgba(255,255,255,0.06);
    }
    .story:hover {
      transform: translateY(-6px) scale(1.02);
      box-shadow: 0 28px 50px rgba(0,0,0,.25);
    }
    .story::after {
      content: ''; position: absolute; inset: 0; pointer-events: none;
      box-shadow: inset 0 0 0 1px rgba(255,255,255,0.1);
      border-radius: 16px; z-index: 10;
    }`
);

// 2. se-badge (Encontro)
content = content.replace(
  /\.story-encontro \.se-badge \{[\s\S]*?border-radius: 3px;\s+\}/,
  `.story-encontro .se-badge {
      position: absolute; top: 42px; left: 12px; z-index: 2;
      background: rgba(255, 107, 53, 0.35); 
      backdrop-filter: blur(12px) saturate(180%); -webkit-backdrop-filter: blur(12px) saturate(180%);
      border: 1px solid rgba(255, 255, 255, 0.25); color: #fff;
      font-family: 'JetBrains Mono', monospace; font-size: 7px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;
      padding: 4px 10px; border-radius: 12px; box-shadow: 0 4px 12px rgba(255,107,53, 0.2);
    }`
);

// 3. sa-badge (Artigo)
content = content.replace(
  /\.story-artigo \.sa-badge \{[\s\S]*?border-radius: 3px;\s+\}/,
  `.story-artigo .sa-badge {
      position: absolute; top: 12px; left: 12px; z-index: 2;
      background: rgba(255, 107, 53, 0.35); 
      backdrop-filter: blur(12px) saturate(180%); -webkit-backdrop-filter: blur(12px) saturate(180%);
      border: 1px solid rgba(255, 255, 255, 0.25); color: #fff;
      font-family: 'JetBrains Mono', monospace; font-size: 7px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;
      padding: 4px 10px; border-radius: 12px; box-shadow: 0 4px 12px rgba(255,107,53, 0.2);
    }`
);

// 4. sp-badge (Pessoa)
content = content.replace(
  /\.story-pessoa \.sp-badge \{[\s\S]*?border-radius: 3px;\s+\}/,
  `.story-pessoa .sp-badge {
      position: absolute; top: 12px; left: 16px; z-index: 3;
      background: rgba(255, 255, 255, 0.7); 
      backdrop-filter: blur(16px) saturate(180%); -webkit-backdrop-filter: blur(16px) saturate(180%);
      border: 1px solid rgba(255, 255, 255, 0.9); color: var(--black);
      font-family: 'JetBrains Mono', monospace; font-size: 7px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;
      padding: 4px 10px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0, 0.1);
    }`
);

// 5. sc-badge (Chamada)
content = content.replace(
  /\.story-chamada \.sc-badge \{[\s\S]*?border-radius: 3px;\s+display: flex; align-items: center; gap: 5px;\s+\}/,
  `.story-chamada .sc-badge {
      position: absolute; top: 12px; left: 12px; z-index: 3;
      background: rgba(196, 30, 58, 0.45); 
      backdrop-filter: blur(12px) saturate(180%); -webkit-backdrop-filter: blur(12px) saturate(180%);
      border: 1px solid rgba(255, 255, 255, 0.25); color: #fff;
      font-family: 'JetBrains Mono', monospace; font-size: 7px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;
      padding: 4px 10px; border-radius: 12px; display: flex; align-items: center; gap: 5px; box-shadow: 0 4px 12px rgba(196,30,58, 0.2);
    }`
);

// 6. sr-badge (Reel)
content = content.replace(
  /\.story-reel \.sr-badge \{[\s\S]*?border-radius: 3px;\s+\}/,
  `.story-reel .sr-badge {
      position: absolute; top: 12px; right: 12px; z-index: 2;
      background: linear-gradient(90deg, rgba(255,107,53,.6), rgba(196,30,58,.6)); 
      backdrop-filter: blur(12px) saturate(180%); -webkit-backdrop-filter: blur(12px) saturate(180%);
      border: 1px solid rgba(255, 255, 255, 0.25); color: #fff;
      font-family: 'JetBrains Mono', monospace; font-size: 7px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;
      padding: 4px 10px; border-radius: 12px; box-shadow: 0 4px 12px rgba(196,30,58, 0.2);
    }`
);


// 7. Cinematic Fades and Overlays
// story-encontro se-bottom
content = content.replace(
  /\.story-encontro \.se-bottom \{[\s\S]*?z-index: 2;\s+\}/,
  `.story-encontro .se-bottom {
      position: absolute; bottom: 0; left: 0; right: 0; height: 65%;
      background: linear-gradient(0deg, #111 5%, rgba(17,17,17,0.85) 30%, transparent 100%);
      display: flex; flex-direction: column; justify-content: flex-end;
      padding: 0 14px 14px; z-index: 2;
    }`
);
// story-artigo sa-bottom
content = content.replace(
  /\.story-artigo \.sa-bottom \{[\s\S]*?justify-content: flex-end;\s+\}/,
  `.story-artigo .sa-bottom {
      position: absolute; bottom: 0; left: 0; right: 0; height: 65%;
      background: linear-gradient(0deg, #111 5%, rgba(17,17,17,0.85) 30%, transparent 100%);
      padding: 14px 14px 12px; z-index: 2;
      display: flex; flex-direction: column; justify-content: flex-end;
    }`
);
// story-pessoa sp-bottom
content = content.replace(
  /\.story-pessoa \.sp-bottom \{[\s\S]*?flex-direction: column;\s+\}/,
  `.story-pessoa .sp-bottom {
      position: absolute; bottom: 0; left: 0; right: 0; height: 45%;
      background: linear-gradient(0deg, #111 15%, rgba(17,17,17,0.8) 40%, transparent 100%);
      padding: 16px 16px 14px; z-index: 2;
      display: flex; flex-direction: column; justify-content: flex-end;
    }`
);


// 8. Grids Cibernéticos nas texturas "Dado" e "Dica"
content = content.replace(
  /\.story-dado \{([\s\S]*?)\}/,
  `.story-dado {
      $1
      position: relative;
    }
    .story-dado::after {
      content: ''; position: absolute; inset: 0; pointer-events: none;
      background-image: linear-gradient(rgba(17,17,17,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(17,17,17,0.03) 1px, transparent 1px);
      background-size: 8px 8px; z-index: 1;
    }`
);
content = content.replace(
  /\.story-dica::before \{[\s\S]*?z-index: 0;\s+\}/,
  `.story-dica::before {
      content: ''; position: absolute; inset: 0;
      background-image: radial-gradient(rgba(244,196,48,.15) 1px, transparent 1px),
                        linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px);
      background-size: 12px 12px, 32px 32px; z-index: 0;
    }`
);


// 9. CTAs Estilo Apple
// sr-cta (Reel)
content = content.replace(
  /\.story-reel \.sr-cta \{[\s\S]*?margin-bottom: 8px;\s+\}/,
  `.story-reel .sr-cta {
      display: block; text-align: center;
      background: rgba(255,255,255,0.9); color: var(--black);
      backdrop-filter: blur(8px);
      font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 9px;
      padding: 8px; border-radius: 20px; margin-bottom: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15); transition: transform 0.2s, background 0.2s;
    }
    .story-reel .sr-cta:hover { transform: scale(1.05); background: #fff; }`
);
// sc-cta (Chamada)
content = content.replace(
  /\.story-chamada \.sc-cta \{[\s\S]*?margin-bottom: 6px; letter-spacing: \.3px;\s+\}/,
  `.story-chamada .sc-cta {
      background: linear-gradient(90deg,#FF6B35,#C41E3A); color: #fff;
      font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 9.5px;
      padding: 8px; border-radius: 20px; text-align: center;
      margin-bottom: 6px; letter-spacing: .3px;
      box-shadow: 0 8px 24px rgba(255,107,53, 0.3); transition: transform 0.2s, box-shadow 0.2s;
    }
    .story-chamada .sc-cta:hover { transform: translateY(-2px); box-shadow: 0 12px 28px rgba(255,107,53, 0.4); }`
);


// 10. Atualiza números da dica/dado
content = content.replace(
  /\.story-dado \.sd-stat-value \{([\s\S]*?)\}/,
  `.story-dado .sd-stat-value {
      $1
      background: linear-gradient(135deg, #FF6B35, #C41E3A);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }`
);


fs.writeFileSync(filePath, content, 'utf8');
console.log('Design Apple injetado com sucesso no index.html!');
