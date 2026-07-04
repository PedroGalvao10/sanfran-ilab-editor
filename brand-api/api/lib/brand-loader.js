// === Helper: carrega brand.json e provê acesso unificado ===
// Single source of truth para API REST e MCP Server.

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// brand.json fica em ../../brand.json relativo a este arquivo
const BRAND_PATH = process.env.BRAND_JSON_PATH || join(__dirname, '..', '..', 'brand.json');

let cache = null;
let cacheTime = 0;
const CACHE_TTL = 60 * 1000; // 60s

export function loadBrand() {
  const now = Date.now();
  if (cache && (now - cacheTime) < CACHE_TTL) return cache;
  cache = JSON.parse(readFileSync(BRAND_PATH, 'utf-8'));
  cacheTime = now;
  return cache;
}

export function getBrand() {
  return loadBrand();
}

export function getTemplate(id) {
  const brand = loadBrand();
  return brand.templates[id] || null;
}

export function getHashtags(category) {
  const brand = loadBrand();
  if (!category) return brand.hashtags;
  return brand.hashtags[category] || [];
}
