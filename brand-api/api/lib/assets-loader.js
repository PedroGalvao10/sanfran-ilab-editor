import fs from 'fs';
import path from 'path';

const ALLOWED_CATEGORIES = new Set([
  'lex',
  'elementos',
  'icons_v2',
  'patterns',
  'scenes_3d',
  'tech',
  'templates'
]);

export function listAssets(baseUrl = '') {
  const assetsDir = path.resolve(process.cwd(), '../assets');
  if (!fs.existsSync(assetsDir)) return { error: 'Assets folder not found' };

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
