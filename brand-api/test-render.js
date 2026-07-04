import fs from 'fs';
import { exec } from 'child_process';

console.log('Iniciando servidor local (Porta 3005)...');
const server = exec('node api/server.js', { env: { ...process.env, PORT: 3005, BRAND_API_TOKEN: 'token123' } });

// server.stdout.on('data', data => console.log(`[API]: ${data}`));
server.stderr.on('data', data => console.error(`[API ERRO]: ${data}`));

setTimeout(async () => {
  console.log('Disparando requisição de renderização para a IA...');
  try {
    const res = await fetch('http://127.0.0.1:3005/brand/render-story', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer token123' },
      body: JSON.stringify({
        template: 'feed_carrossel',
        fields: {
          badge_top: 'IA & DIREITO',
          headline: 'Novo Blueprint de Integração',
          body_text: 'O Brandbook agora produz Posts de Feed Quadrados (1:1) de forma 100% autônoma pela API, usando Chromium headless para renderizar as fontes e o CSS final do Design System (Apple-style).',
          page_indicator: '01/10',
          brand_footer: 'SanFran <em>iLab</em>'
        }
      })
    });
    
    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`HTTP error: ${res.status} - Body: ${errorText}`);
    }
    
    const arrayBuffer = await res.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);
    fs.writeFileSync('story_teste_carrossel.png', buffer);
    console.log('✅ Imagem PNG salva com sucesso: story_teste_carrossel.png');
  } catch (err) {
    console.error('❌ Erro ao renderizar:', err.message);
  } finally {
    server.kill();
    process.exit(0);
  }
}, 3000);
