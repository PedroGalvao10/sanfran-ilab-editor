// === Helper: armazenamento de rascunhos (ponte MCP → Editor) ===
// Um rascunho é um JSON persistido temporariamente. A tool MCP `create_post_draft` grava,
// e o Editor Pro lê via GET /brand/drafts/:id.
// O arquivo é mantido para compor o histórico de rascunhos.
// TTL de 24h limpa arquivos muito antigos (chamado no boot do server).
// Arquivo em disco (não banco) porque o processo MCP (stdio) e o processo
// Fastify (:3000) não compartilham memória — o filesystem é a ponte mais simples.

import { randomBytes } from 'crypto';
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync, unlinkSync, statSync } from 'fs';
import path from 'path';
import os from 'os';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
// Em serverless (Vercel/Lambda) o bundle é somente-leitura — só /tmp é gravável.
// Local/Railway seguem usando a pasta do projeto (mais fácil de inspecionar em dev).
const DRAFTS_DIR = process.env.VERCEL
  ? path.join(os.tmpdir(), 'ilab-drafts')
  : path.resolve(__dirname, '../../data/drafts');
const TTL_MS = 24 * 60 * 60 * 1000;
const ID_PATTERN = /^[a-f0-9]{12}$/; // formato exato gerado por saveDraft — qualquer coisa fora disso é rejeitada

function ensureDir() {
  if (!existsSync(DRAFTS_DIR)) mkdirSync(DRAFTS_DIR, { recursive: true });
}

export function saveDraft(data) {
  ensureDir();
  const id = randomBytes(6).toString('hex');
  writeFileSync(path.join(DRAFTS_DIR, `${id}.json`), JSON.stringify({ ...data, createdAt: Date.now() }));
  return id;
}

// Lê um rascunho (sem apagar, permitindo histórico).
// Valida o formato do id antes de montar o caminho.
export function readDraft(id) {
  if (typeof id !== 'string' || !ID_PATTERN.test(id)) return null;
  ensureDir();
  const filePath = path.join(DRAFTS_DIR, `${id}.json`);
  if (!existsSync(filePath)) return null;
  const data = JSON.parse(readFileSync(filePath, 'utf-8'));
  return data;
}

// Lista os rascunhos disponíveis
export function listDrafts() {
  ensureDir();
  const drafts = [];
  for (const file of readdirSync(DRAFTS_DIR)) {
    if (!file.endsWith('.json')) continue;
    const id = file.replace('.json', '');
    try {
      const data = JSON.parse(readFileSync(path.join(DRAFTS_DIR, file), 'utf-8'));
      drafts.push({
        id,
        createdAt: data.createdAt || 0,
        template_id: data.template_id || 'desconhecido'
      });
    } catch {
      // ignora arquivos corrompidos
    }
  }
  // Ordena os mais recentes primeiro
  return drafts.sort((a, b) => b.createdAt - a.createdAt);
}

export function cleanupStaleDrafts() {
  ensureDir();
  const now = Date.now();
  for (const file of readdirSync(DRAFTS_DIR)) {
    if (!file.endsWith('.json')) continue;
    const filePath = path.join(DRAFTS_DIR, file);
    try {
      if (now - statSync(filePath).mtimeMs > TTL_MS) unlinkSync(filePath);
    } catch {
      // arquivo pode ter sido removido concorrentemente (outra requisição consumiu
      // o mesmo rascunho entre o readdir e o stat) — ignora, não é um erro real.
    }
  }
}
