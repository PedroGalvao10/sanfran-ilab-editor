# SanFran iLab — Brand API + MCP Server

API REST + MCP Server expondo as guidelines de brand do **SanFran iLab (FD-USP)** para uso por agentes de IA, automações (n8n, Make, Zapier) e clientes MCP (Claude Code).

---

## Estrutura

```
brand-api/
├── brand.json          # fonte única da verdade
├── api/                # REST (Fastify)
│   ├── server.js
│   ├── lib/            # brand-loader, prompt-builder, validator
│   ├── middleware/     # auth Bearer
│   └── routes/         # 7 endpoints
├── mcp/                # MCP Server
│   └── server.js       # 5 tools
└── test/smoke.js
```

---

## Setup

```bash
cd brand-api
npm install
cp .env.example .env
# edite .env e defina API_KEY (opcional em dev)
```

### Rodar API

```bash
npm run dev          # com hot reload
npm start            # produção
```

Servidor sobe em `http://localhost:3000`.

### Rodar smoke test

```bash
npm test
```

---

## Endpoints REST

Todos exigem `Authorization: Bearer <API_KEY>` (exceto `/` e `/health`).

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Info da API e lista de endpoints |
| GET | `/health` | Healthcheck |
| GET | `/brand/context` | JSON completo das guidelines |
| GET | `/brand/prompt?format=text\|json` | System prompt pronto pra LLM |
| GET | `/brand/templates` | Lista os 8 templates |
| GET | `/brand/templates/:id` | Template específico (encontro, dica, etc) |
| POST | `/brand/validate` | Valida copy → `{ valid, score, issues[] }` |
| GET | `/brand/hashtags?category=core` | Hashtags filtradas |
| GET | `/brand/voice` | Tom de voz, persona, DOs/DON'Ts |
| **POST** | **`/brand/generate-copy`** | **Gera copy on-brand via LLM (Claude)** |
| **POST** | **`/brand/render-story`** | **Renderiza PNG 1080×1920 do template** |
| **GET**  | **`/brand/instagram-info`** | **Info da conta IG conectada** |
| **POST** | **`/brand/publish-instagram`** | **Publica no Instagram via Meta Graph API** |

### Exemplos

**Gerar copy on-brand (LLM):**
```bash
curl -X POST http://localhost:3000/brand/generate-copy \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "brief": "Anunciar workshop sobre prompt engineering jurídico dia 15/06",
    "template": "chamada",
    "format": "both"
  }'
```

**Renderizar PNG do template:**
```bash
curl -X POST http://localhost:3000/brand/render-story \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "template": "dica",
    "fields": {
      "bignum": "03",
      "title": "Use [accent]prompts específicos[/accent] em juridiquês.",
      "tag": "#DicaiLab"
    }
  }' --output story.png
```

**Publicar no Instagram (precisa de PNG hospedado em HTTPS público):**
```bash
curl -X POST http://localhost:3000/brand/publish-instagram \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/story.png",
    "caption": "Texto da legenda... #iLab #DireitoEIA",
    "is_story": false
  }'
```

**Status da conexão IG:**
```bash
curl http://localhost:3000/brand/instagram-info -H "Authorization: Bearer YOUR_KEY"
```

---

## MCP Server

Para integrar com Claude Code, adicione ao `.mcp.json` (ou `.claude/settings.json`):

```json
{
  "mcpServers": {
    "ilab-brand": {
      "command": "node",
      "args": ["./brand-api/mcp/server.js"]
    }
  }
}
```

### 5 tools expostas

| Tool | Descrição |
|---|---|
| `get_brand_context` | Guidelines completas (JSON ou system prompt) |
| `validate_copy` | Valida texto → score + issues |
| `get_story_template` | Detalhes de um template específico |
| `list_hashtags` | Hashtags por categoria |
| `get_voice_guidelines` | Tom de voz, DOs e DON'Ts |

---

## Pipeline completo (brief → post no IG)

```
1. POST /brand/generate-copy  { brief: "evento X dia Y" }
   → recebe { story_fields, caption, suggested_template, validation }

2. POST /brand/render-story   { template, fields: story_fields }
   → recebe PNG 1080×1920

3. (externo) upload do PNG para S3 / Cloudinary / Vercel Blob
   → obtém URL HTTPS pública

4. POST /brand/publish-instagram  { image_url, caption }
   → recebe { media_id, permalink }
```

Pode ser orquestrado por agente IA, n8n, Make ou Zapier.

---

## Configuração do Instagram

Para publicar no IG é necessário:

1. **Conta Business ou Creator** no Instagram
2. **Página do Facebook** conectada à conta IG
3. **App** no [developers.facebook.com](https://developers.facebook.com/)
4. **Access Token** (long-lived) com permissões:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_show_list`
   - `pages_read_engagement`
5. **IG_USER_ID** — ID numérico da conta business

Documentação oficial: https://developers.facebook.com/docs/instagram-api/guides/content-publishing

**Importante:** o PNG precisa estar em URL **HTTPS pública** acessível pela Meta. Não funciona com localhost, IP local ou data URLs.

---

## Deploy

### Vercel (serverless, com Playwright)

`vercel.json` já configurado com:
- `memory: 3008MB` (mínimo p/ Chromium)
- `maxDuration: 60s`
- `includeFiles: brand.json + index.html`
- `IS_SERVERLESS=1` (ativa playwright-core + @sparticuz/chromium-min)

```bash
cd brand-api
vercel              # primeira vez (configura)
vercel --prod       # deploy production
```

Variáveis de ambiente a definir na Vercel:
- `API_KEY` — Bearer token
- `ANTHROPIC_API_KEY` — para generate-copy
- `META_ACCESS_TOKEN` + `IG_USER_ID` — para Instagram

### Outros providers
- **Railway** / **Fly.io**: funciona com Chromium full do `playwright` (sem precisar de `IS_SERVERLESS=1`)
- **AWS Lambda**: idem Vercel — usa `IS_SERVERLESS=1`

### MCP Server

Roda local via stdio. Para acesso remoto, embarcar em container e usar transporte HTTP/SSE.

---

## Atualizando o brand

1. Edite `brand.json`
2. API recarrega automaticamente (cache TTL 60s)
3. MCP picks up no próximo restart

Não duplique dados — `brand.json` é a fonte única.
