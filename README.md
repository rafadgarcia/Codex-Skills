# Guia de Arquitetura, Curadoria e Manutenção das Skills (`Codex-Skills`)

Este documento registra a estruturação realizada na pasta de skills (`C:\Users\Rafa\.codex\skills` / repositório [`rafadgarcia/Codex-Skills`](https://github.com/rafadgarcia/Codex-Skills)), explica os critérios de curadoria e Políticas de Sincronização adotadas, e estabelece o procedimento padrão para adicionar, atualizar ou podar skills no futuro.

---

## 1. Resumo do que foi feito

### 1.1. Integração Git Direta e Limpeza de Submódulos
- A pasta local `C:\Users\Rafa\.codex\skills` foi transformada diretamente no clone versionado do repositório `rafadgarcia/Codex-Skills` (branch `master`).
- O submódulo órfão quebrado (`secure-web-apps`) foi removido do índice do Git.
- Foi criado o arquivo [`.gitignore`](.gitignore) para ignorar arquivos gerados em tempo de execução (`**/__pycache__/`, `*.pyc`) e a pasta interna de sistema do Codex (`.system/`).
- Como o Antigravity (`.gemini/config/skills.json`) aponta para `~/.codex/skills`, qualquer atualização feita aqui reflete automaticamente tanto no **Codex** quanto no **Antigravity**.

### 1.2. Limpeza, Fusão e Substituição de Skills
- **Removidas definitivamente (7 skills):** `debugging-and-error-recovery`, `test-driven-development`, `source-driven-development`, `observability-and-instrumentation`, `shipping-and-launch`, `check-my-vibe` e `visual-qa-web` (fundida diretamente dentro de [`site-recreation/SKILL.md`](site-recreation/SKILL.md)).
- **Substituição de Supabase por PostgreSQL Oficial:** As pastas `supabase` e `supabase-postgres-best-practices` foram removidas e substituídas pela skill oficial e 100% agnóstica **[`postgres-best-practices`](postgres-best-practices/SKILL.md)** (de `neondatabase/postgres-skills`, escrita com membros do PostgreSQL Core Team para Postgres 14–18).
- **Novas Skills Criadas / Adicionadas:**
  1. **[`nextjs-16-modern`](nextjs-16-modern/SKILL.md):** Garante as convenções do Next.js 16 + React 19 + Tailwind v4 (`proxy.ts` substituindo `middleware.ts`, `await params`/`searchParams`/`cookies()`/`headers()`, fronteiras `server-only`, sanitização de HTML Tiptap e `output: "standalone"`).
  2. **[`docker-caddy-vps`](docker-caddy-vps/SKILL.md):** Padroniza os deployments em Docker Compose + Caddy v2 na VPS (`init: true` contra processos zumbis, rotação de logs `10m`, isolamento entre rede `edge` e bridge interna do Postgres, healthchecks e Dockerfile multi-stage para Next.js standalone + Prisma).
  3. **Suite REA (`reverse-engineer-anything`, `rea-tool-design`, `rea-changelog-update`)** e preservação das skills congeladas (`pinned`) no manifesto.

---

## 2. Catálogo Atual das 24 Skills e suas Políticas (`skills-manifest.json`)

O arquivo [`skills-manifest.json`](skills-manifest.json) controla como cada skill é tratada pelo script [`sync-skills.ps1`](sync-skills.ps1):

| Skill | Modo no Manifesto | Repositório Upstream | Arquivos Protegidos / Observações |
| :--- | :---: | :--- | :--- |
| **`audit-logging`** | `local` | *(Autoral)* | Nunca sobrescrita pelo sync. |
| **`site-recreation`** | `local` | *(Autoral)* | Inclui checklist de QA visual integrado. Nunca sobrescrita. |
| **`nextjs-16-modern`** | `local` | *(Autoral)* | Regras de Next.js 16, React 19, `proxy.ts` e Tailwind v4. |
| **`docker-caddy-vps`** | `local` | *(Autoral)* | Padrão de containers Docker, healthcheck e rede `edge` Caddy. |
| **`frontend-design`** | `overlay` | `vipulgupta2048/codex-skills` | Protege `SKILL.md` e `references/visual-intensity-and-motion.md` (customização sua). |
| **`ui-ux-pro-max`** | `overlay` | `nextlevelbuilder/ui-ux-pro-max-skill` | Protege `data/web-interface.csv`. |
| **`ui-responsive-audit`** | `overlay` | `ov3rf1w/ui-responsive-audit` | Motor Playwright (81 KB) de auditoria geométrica em 18 viewports. |
| **`playwright-interactive`** | `overlay` | `openai/skills` | Sessão interativa persistente via `js_repl` (Web e Electron). |
| **`postgres-best-practices`** | `overlay` | `neondatabase/postgres-skills` | 14 guias de PostgreSQL 14–18 puro (schema, índices, `EXPLAIN`, backup, pool). |
| **`prisma-upgrade-v7`** | `overlay` | `prisma/skills` | Migração Prisma v6 -> v7 (`prisma.config.ts` e driver adapters). |
| **`prisma-cli`** | `overlay` | `prisma/skills` | Comandos CLI do Prisma v7. |
| **`prisma-client-api`** | `overlay` | `prisma/skills` | Queries, filtros, relações e transações do Prisma Client. |
| **`cloudflare`** | `overlay` | `cloudflare/skills` | 320 arquivos de referência da plataforma Cloudflare (R2, Workers, KV, D1, AI). |
| **`workers-best-practices`** | `overlay` | `cloudflare/skills` | Boas práticas de produção para Cloudflare Workers. |
| **`turnstile-spin`** | `overlay` | `cloudflare/skills` | Configuração end-to-end do CAPTCHA Cloudflare Turnstile. |
| **`webhook-handler-patterns`** | `overlay` | `hookdeck/webhook-skills` | Verificação de assinatura raw body, idempotência e retries. |
| **`prisma-postgres`** | `pinned` | `prisma/skills` | Congelada porque o upstream deprecou esse nome e apagou `references/`. |
| **`prisma-database-setup`** | `pinned` | `prisma/skills` | Nome de compatibilidade depreciado; substituta upstream: `prisma-orm-setup`. |
| **`restful-api`** | `pinned` | *(não comprovada)* | Snapshot congelado; sem origem confiável registrada. |
| **`typescript-engineering`** | `pinned` | *(não comprovada)* | Snapshot congelado; sem origem confiável registrada. |
| **`wrangler`** | `pinned` | *(não comprovada)* | Snapshot congelado; validar comandos na documentação Cloudflare. |
| **`reverse-engineer-anything`** | `pinned` | `morluto/rea` | Engenharia reversa e observação de runtime. |
| **`rea-tool-design`** | `pinned` | `morluto/rea` | Padrões de ferramentas e contratos REA. |
| **`rea-changelog-update`** | `pinned` | `morluto/rea` | Fluxo de changelogs e releases REA. |

---

## 3. Como Operar no Futuro (Casos Semelhantes)

### Validação automática

O workflow `.github/workflows/validate-skills.yml` valida o manifesto, a correspondência entre skills e pastas, os links Markdown locais, os dados/testes do UI/UX Pro Max e os testes offline do Turnstile em cada push e pull request. Para rodar localmente:

```powershell
python scripts/validate-skills.py
python -m unittest discover -s ui-ux-pro-max/scripts/tests -v
python -m unittest discover -s turnstile-spin/tests -v
```

### Caso 1: Atualizar todas as skills clonadas de repositórios externos (`overlay`)
Sempre que quiser trazer as novidades das skills oficiais (Cloudflare, Prisma, Postgres, UI/UX Pro Max, etc.) sem perder suas customizações nem tocar nas skills `local` ou `pinned`:

```powershell
cd C:\Users\Rafa\.codex\skills

# 1. Simular antes para ver o que mudaria (opcional, mas recomendado):
.\sync-skills.ps1 -DryRun

# 2. Aplicar as atualizações:
.\sync-skills.ps1

# 3. Inspecionar as mudanças via Git:
git status
git diff
```
> **O que fazer se um repositório oficial estragar ou deprecar uma skill (como aconteceu com `prisma-postgres`)?**
> Basta reverter a pasta com `git checkout -- nome-da-skill/` e mudar o `"mode"` dela de `"overlay"` para `"pinned"` dentro do [`skills-manifest.json`](skills-manifest.json).

---

### Caso 2: Customizar uma skill clonada sem perder a atualização automática
Se você editar uma skill clonada (por exemplo, adicionar um novo arquivo em `references/` ou alterar o `SKILL.md` de uma skill `"overlay"`):
1. Arquivos **novos** que você criar dentro da pasta da skill **nunca são apagados** pelo `sync-skills.ps1` (pois o modo `overlay` apenas adiciona/atualiza arquivos que existem no upstream).
2. Se você editar um arquivo que **também existe no repositório original** (como o `SKILL.md`), adicione o caminho relativo dele na lista `"protectedFiles"` daquela skill dentro do [`skills-manifest.json`](skills-manifest.json):
   ```json
   "protectedFiles": [
     "SKILL.md",
     "references/meu-arquivo-customizado.md"
   ]
   ```
   Assim, o `sync-skills.ps1` atualizará o restante da skill, mas preservará o seu arquivo intacto.

---

### Caso 3: Adicionar uma nova skill no futuro (Filtro de Decisão)
Antes de instalar qualquer skill nova da internet ou criar uma sua, aplique o **Teste dos 3 Critérios para LLMs Modernos**:

1. **Ela fornece scripts/ferramentas executáveis locais?** (Ex: scripts Playwright, Python, datasets CSV). -> **SIM, instale.**
2. **Ela documenta breaking changes recentes pós-cutoff do modelo?** (Ex: Next.js 16 `proxy.ts`, Prisma 7 `prisma.config.ts`). -> **SIM, instale.**
3. **Ela define padrões arquiteturais/visuais exclusivos seus ou da sua empresa?** (Ex: `docker-caddy-vps`, `audit-logging`, `reverse-engineer-anything`). -> **SIM, crie como `"mode": "local"` ou `"pinned"`.**
4. *Ela apenas explica como programar em uma linguagem, como fazer TDD ou conceitos básicos?* -> **Evite ativar por padrão**, pois o LLM já sabe fazer isso nativamente e consome janela de contexto.

**Passo a passo para registrar uma nova skill:**
1. Coloque a pasta da skill em `C:\Users\Rafa\.codex\skills\<nome-da-skill>\`.
2. Adicione a entrada correspondente no [`skills-manifest.json`](skills-manifest.json) (`"mode": "local"` se for autoral, `"pinned"` se for congelada, ou `"mode": "overlay"` com `repo`, `branch` e `subPath` se vier do GitHub).
3. Adicione 1 bullet objetivo no roteador [`AGENTS.md`](AGENTS.md) explicando exatamente **quando** o agente deve ativá-la.

---

### Caso 4: Revisão Periódica (A cada novo lançamento de geração de LLM)
Quando sair uma nova geração de modelos (ex: GPT-7, Gemini 5, Claude 5):
1. Revise as skills de *"Breaking Changes"* (como `nextjs-16-modern` ou `prisma-upgrade-v7`). Quando o modelo novo já tiver essas versões consolidadas no pré-treinamento dele, você poderá enxugar ou remover essas skills.
2. Mantenha nos arquivos `AGENTS.md` dos seus projetos locais (como em `Desktop\Projetos\*`) apenas referências para as skills que realmente existem no seu [`AGENTS.md`](AGENTS.md) global, evitando referências órfãs.
