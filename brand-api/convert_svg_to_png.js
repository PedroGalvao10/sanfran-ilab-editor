import { chromium } from 'playwright';
import path from 'path';

(async () => {
  console.log('Iniciando conversão via Playwright...');
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport: { width: 1080, height: 1080 }
  });

  const outPath = path.resolve(process.cwd(), '../');
  
  for (let i = 1; i <= 3; i++) {
    const file = `carrossel_0${i}`;
    const svgPath = `file:///${path.join(outPath, file + '.svg').replace(/\\/g, '/')}`;
    console.log(`Carregando ${svgPath}...`);
    
    await page.goto(svgPath, { waitUntil: 'load', timeout: 10000 }); // networkidle garante que webfonts carreguem
    
    // Aguarda fontes da API do Google renderizarem se necessário
    await page.evaluate(() => document.fonts.ready);
    
    const pngPath = path.join(outPath, `${file}.png`);
    await page.screenshot({ path: pngPath });
    console.log(`✅ Salvo: ${pngPath}`);
  }

  await browser.close();
  console.log('Finalizado.');
})();
