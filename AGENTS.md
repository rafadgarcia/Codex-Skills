# Project instructions

Use the available local Codex skills when applicable:

Use the minimum set of skills necessary for the task. Prefer one primary domain skill, then add cross-cutting skills only when the task materially requires them. Do not invoke a skill merely because the technology appears somewhere in the repository.

- Use `$frontend-design` for frontend interfaces, pages, components, visual systems, motion, layout, accessibility, and production-grade UI polish.
- Use `$ui-ux-pro-max` for UI/UX research, design-system recommendations, product-specific interface guidance, color/type/style selection, stack-specific UI guidance, and searchable design intelligence.
- Use `$restful-api` for HTTP APIs, REST endpoints, CRUD routes, route handlers, controllers, request/response schemas, API documentation, and backend HTTP interfaces.
- Use `$typescript-engineering` for TypeScript type design, tsconfig/compiler options, strictness, JavaScript-to-TypeScript migration, runtime validation boundaries, unknown vs any, type guards, discriminated unions, generics, utility types, React TypeScript patterns, and TypeScript tooling.
- Use `$secure-web-apps` for web application security, including authentication, authorization, input validation, XSS/injection, CSRF, CORS, CSP/security headers, JWT/OAuth/tokens, SSRF, redirects, sensitive data, secrets, uploads, storage, database exposure, supply chain, deployment hardening, audit logs, rate limits, and abuse prevention.
- Use `$check-my-vibe` for authorized passive public-site scans through Check My Vibe, especially for security headers, exposed secrets, source maps, public files, and deployment mistakes.
- Use `$supabase` for Supabase Database, Auth, Storage, Edge Functions, Realtime, RLS, migrations, CLI, SSR clients, and Supabase-specific troubleshooting.
- Use `$supabase-postgres-best-practices` for Supabase/Postgres schema, query, index, connection, locking, and performance work.
- Use Prisma skills when working with Prisma: `$prisma-client-api` for queries and transactions, `$prisma-cli` for CLI/migrations commands, `$prisma-database-setup` for provider setup, `$prisma-postgres` for Prisma Postgres, and `$prisma-upgrade-v7` for Prisma v7 migrations.
- Use Cloudflare skills when working with Cloudflare: `$cloudflare` for platform tasks, `$workers-best-practices` for Workers code/config review, `$wrangler` for CLI commands, and `$turnstile-spin` for Turnstile setup.
- Use `$webhook-handler-patterns` for webhook receivers, raw body signature verification, retry behavior, idempotency, and Express/Next.js/FastAPI webhook gotchas.
- Use `$test-driven-development` when implementing logic, fixing bugs, changing behavior, or adding regression coverage.
- Use `$debugging-and-error-recovery` when tests fail, builds break, runtime behavior is unexpected, or a bug needs root-cause diagnosis.
- Use `$source-driven-development` when framework/library correctness depends on current official documentation or the user asks for verified/source-backed implementation.
- Use `$observability-and-instrumentation` when adding logs, metrics, tracing, alerts, or production diagnostics for endpoints, jobs, integrations, queues, or services.
- Use `$shipping-and-launch` when preparing production deploys, staged rollouts, launch checklists, monitoring, or rollback plans.

For UI implementation tasks, use `$frontend-design` as the primary implementation skill. Add `$ui-ux-pro-max` when the task needs design-system research, style exploration, palette/type selection, or product-specific UI guidance.

For security-sensitive API endpoints, use `$restful-api` as the primary API skill and add `$secure-web-apps` when auth, authorization, sensitive data, public exposure, uploads, payments, tokens, abuse resistance, or security headers are materially involved.

For TypeScript API, frontend, Prisma, Supabase, Cloudflare, or webhook work, add `$typescript-engineering` only when the task touches type contracts, runtime validation, generated types, compiler errors, migration, or strictness.

For public deployed-site posture checks, use `$check-my-vibe` for the passive external scan and `$secure-web-apps` to interpret broader security implications or plan code fixes.

For Supabase, Prisma, Cloudflare, or webhook work, add `$secure-web-apps` only when the task touches auth, authorization, tenant scope, secrets, user data, payments, uploads, storage, public exposure, or abuse resistance.

For bug fixes, use `$debugging-and-error-recovery` as the primary skill. Add `$test-driven-development` when implementing a fix needs regression coverage. For production launches, use `$shipping-and-launch` as the primary skill and add `$observability-and-instrumentation` or `$secure-web-apps` only when monitoring, rollback, risk, or user data are materially involved.

## Skill maintenance

When working directly inside a skill folder, keep the skill self-contained. Put reusable procedures in `SKILL.md`, detailed supporting guidance in `references/`, executable helpers in `scripts/`, and templates or starter files in `assets/`.

When updating a skill, keep the `SKILL.md` frontmatter concise and accurate so Codex can trigger the skill correctly.

Do not add extra README, installation, changelog, or quick-reference files unless explicitly requested.
