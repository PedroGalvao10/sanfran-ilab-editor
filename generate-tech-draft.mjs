import { saveDraft } from './brand-api/api/lib/draft-store.js';

// Assets for Derecho and Tech
const draft = {
  templateId: 'carrossel_4x5',
  fields: {
    headline: 'O Futuro da Advocacia 5.0',
    body_text: 'Como a IA generativa está redefinindo o modelo operacional dos grandes escritórios. Descubra os pilares da transformação digital que já não são diferenciais, mas pré-requisitos para a sobrevivência no mercado.',
    page_indicator: '1 / 5',
    brand_footer: 'SanFran iLab'
  },
  photoUrl: null, // We won't use a background photo, just the deep black background
  decorations: [
    // Top Right HUD Corner
    {
      url: 'http://127.0.0.1:3000/assets/tech/tech-hud-corner.svg',
      x: 780, y: 40, width: 250, height: 250, opacity: 0.5, name: 'HUD TopRight'
    },
    // Circuit left
    {
      url: 'http://127.0.0.1:3000/assets/tech/tech-circuit.svg',
      x: -50, y: 600, width: 400, height: 400, opacity: 0.3, name: 'Circuito'
    },
    // Binary code background
    {
      url: 'http://127.0.0.1:3000/assets/tech/tech-binary.svg',
      x: 100, y: 900, width: 800, height: 400, opacity: 0.1, name: 'Binário'
    },
    // 3D Scales of Justice floating
    {
      url: 'http://127.0.0.1:3000/assets/3dicons/3d-balance.png',
      x: 600, y: 750, width: 450, height: 450, opacity: 1, name: 'Balança 3D',
      effects: [{ type: 'dropShadow', enabled: true, x: 0, y: 16, blur: 32, color: 'rgba(244, 196, 48, 0.3)' }]
    },
    // 3D Brain tech
    {
      url: 'http://127.0.0.1:3000/assets/3dicons/3d-brain-tech.png',
      x: 80, y: 880, width: 300, height: 300, opacity: 1, name: 'Cérebro Tech',
      effects: [{ type: 'dropShadow', enabled: true, x: 0, y: 12, blur: 24, color: 'rgba(255, 107, 53, 0.4)' }]
    }
  ]
};

const draftId = saveDraft(draft);
console.log(`✅ Draft generated successfully! URL:`);
console.log(`http://127.0.0.1:8080/editor-pro.html?draft=${draftId}`);
