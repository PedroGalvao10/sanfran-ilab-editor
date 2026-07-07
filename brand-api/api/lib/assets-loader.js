import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const ALLOWED_CATEGORIES = new Set([
  'lex',
  'elementos',
  'icons_v2',
  'patterns',
  'scenes_3d',
  'tech',
  'templates'
]);

// Em serverless (Vercel), o backend é implantado como projeto próprio SEM a
// pasta `assets/` (que vive um nível acima, fora do que é enviado) — o scan de
// disco abaixo sempre falharia lá. Fallback: catálogo pré-computado localmente
// (script de geração: rodar listAssets() com o filesystem real disponível e
// salvar aqui), com URLs absolutas apontando pro host que REALMENTE serve os
// arquivos (o brandbook estático). Regenerar sempre que assets/ mudar.
const STATIC_CATALOG_PATH = path.join(__dirname, 'assets-catalog.json');

export function listAssets(baseUrl = '') {
  const assetsDir = path.resolve(process.cwd(), '../assets');
  if (!fs.existsSync(assetsDir)) {
    if (fs.existsSync(STATIC_CATALOG_PATH)) {
      try { return JSON.parse(fs.readFileSync(STATIC_CATALOG_PATH, 'utf-8')); }
      catch { return { error: 'Assets folder not found (catálogo estático corrompido)' }; }
    }
    return { error: 'Assets folder not found' };
  }

  const catalog = {};
  
  function scanDir(currentPath, baseCategory = '') {
    const items = fs.readdirSync(currentPath);
    for (const item of items) {
      const itemPath = path.join(currentPath, item);
      const stat = fs.statSync(itemPath);
      
      if (stat.isDirectory()) {
        const catName = baseCategory ? `${baseCategory}/${item}` : item;
        
        // Only recurse if it's an allowed category or we are at root scanning allowed categories
        if (!baseCategory && !ALLOWED_CATEGORIES.has(catName)) {
          continue;
        }
        
        scanDir(itemPath, catName);
      } else {
        if (item.startsWith('.')) continue;
        
        const category = baseCategory || 'root';
        if (!catalog[category]) catalog[category] = [];
        
        const relativeUrlPath = itemPath.replace(assetsDir, '').replace(/\\/g, '/');
        
        catalog[category].push({
          name: item,
          url: `${baseUrl}/assets${relativeUrlPath}`,
          type: path.extname(item).replace('.', '')
        });
      }
    }
  }

  scanDir(assetsDir);
  return catalog;
}
