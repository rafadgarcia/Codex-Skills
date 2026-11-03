# Project instructions

Use the available local Codex skills when applicable:

Use the minimum set of skills necessary for the task. Prefer one primary domain skill, then add cross-cutting skills only when the task materially requires them. Do not invoke a skill merely because the technology appears somewhere in the repository.

- Use `$frontend-design` for frontend interfaces, pages, components, visual systems, motion, layout, accessibility, and production-grade UI polish.
- Use `$ui-ux-pro-max` for UI/UX research, design-system recommendations, product-specific interface guidance, color/type/style selection, stack-specific UI guidance, and searchable design intelligence.
- Use `$nextjs-16-modern` when building, refactoring, or debugging Next.js 16+ App Router applications with React 19, `proxy.ts`, async `params`/`searchParams`/`cookies()`/`headers()`, Tailwind CSS v4 (`@tailwindcss/postcss`), or `output: "standalone"`.
- Use `$site-recreation` when recreating, redesigning, or rebuilding a website faithfully from a local folder of references (screenshots, exports, documents, assets) and performing baseline visual/responsive QA.
- Use `$ui-responsive-audit` for automated, evidence-driven Playwright responsiveness audits across ultrawide, desktop, iPad, tablet, and mobile viewports, including sticky/pinned scroll states and collision detection.
- Use `$playwright-interactive` for persistent browser or Electron UI debugging through `js_repl`.
- Use `$docker-caddy-vps` when writing or reviewing `Dockerfile`, `compose.yaml` / `docker-compose.yml`, container healthchecks, log rotation, `init: true`, or Caddy `edge` reverse proxy deployments.
- Use `$postgres-best-practices` for PostgreSQL schema design, indexing strategies, query optimization (`EXPLAIN ANALYZE`), query patterns, transaction isolation, connection pooling, `pg_dump`/`pg_restore` backups, and database performance diagnostics.
- Use Prisma skills when working with Prisma: `$prisma-cli` for CLI/migrations commands, `$prisma-postgres` for Prisma Postgres provisioning/operations, and `$prisma-upgrade-v7` for Prisma v7 migrations and `prisma.config.ts` / driver adapter changes.
- Use Cloudflare skills when working with Cloudflare: `$cloudflare` for platform tasks (including R2, Workers, KV, D1, Wrangler), `$workers-best-practices` for Workers code/config review, and `$turnstile-spin` for Turnstile setup.
- Use `$webhook-handler-patterns` for webhook receivers, raw body signature verification, retry behavior, idempotency, and Express/Next.js/FastAPI webhook gotchas.
- Use `$audit-logging` when reviewing, designing, implementing, or fixing audit trails for sensitive state changes such as financial operations, permission changes, impersonation, administrative actions, and destructive operations. Do not use it for ordinary application logs, observability, debugging, or routine reads.

For UI implementation tasks, use `$frontend-design` as the primary implementation skill (paired with `$nextjs-16-modern` in Next.js 16 projects). Add `$ui-ux-pro-max` when the task needs design-system research, style exploration, palette/type selection, or product-specific UI guidance. For reference-based rebuilds, use `$site-recreation` (and `$ui-responsive-audit` when full multi-viewport matrix verification is needed).

For audit-trail work, use `$audit-logging` as the primary domain skill.

## Skill maintenance

When working directly inside a skill folder, keep the skill self-contained. Put reusable procedures in `SKILL.md`, detailed supporting guidance in `references/`, executable helpers in `scripts/`, and templates or starter files in `assets/`.

When updating a skill, keep the `SKILL.md` frontmatter concise and accurate so Codex can trigger the skill correctly.

To update cloned skills from their upstream repositories while preserving local customizations, run `.\sync-skills.ps1` (or `.\sync-skills.ps1 -DryRun` to preview changes) based on `skills-manifest.json`.

Do not add extra README, installation, changelog, or quick-reference files inside individual skill folders unless explicitly requested.
