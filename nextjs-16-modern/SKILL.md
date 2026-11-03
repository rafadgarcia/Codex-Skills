---
name: nextjs-16-modern
description: "Use when building, refactoring, or debugging Next.js 16+ App Router applications with React 19, Tailwind CSS v4 (@tailwindcss/postcss), Prisma v7 driver adapters, or standalone Docker output. Enforces async request APIs, proxy.ts (replacing middleware.ts), Server/Client boundaries, and clean standalone builds."
metadata:
  short-description: "Next.js 16, React 19 & Tailwind v4 modern patterns"
---

# Next.js 16 & React 19 Modern Engineering

Your pre-trained knowledge may default to Next.js 13/14/15 or Tailwind v3 patterns. Enforce these **Next.js 16 + React 19 + Tailwind v4** rules whenever working in a modern Next.js repository.

## 1. Breaking Changes in Next.js 16

### A. `proxy.ts` replaces `middleware.ts`
- In Next.js 16, request interception uses **`proxy.ts`** (or `src/proxy.ts`) exporting `export function proxy(request: NextRequest)`.
- **Before creating `middleware.ts`**, check if the project uses Next.js 16 or already has `proxy.ts`. Never create both `middleware.ts` and `proxy.ts` in the same project.

```ts
// proxy.ts (Next.js 16)
import { NextResponse, type NextRequest } from "next/server";

export function proxy(request: NextRequest) {
  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
```

### B. Asynchronous Request & Route APIs (Mandatory `await`)
- `params` and `searchParams` in `page.tsx`, `layout.tsx`, and `route.ts` are **Promises**.
- `cookies()`, `headers()`, and `draftMode()` from `next/headers` are **asynchronous** and MUST be awaited.

```tsx
// Correct Next.js 16 Page signature
export default async function Page({
  params,
  searchParams,
}: {
  params: Promise<{ slug: string }>;
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const { slug } = await params;
  const query = await searchParams;
  // ...
}
```

```ts
// Correct Next.js 16 Dynamic Route Handler signature
export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  return Response.json({ id });
}
```

### C. Caching & Rendering Semantics
- `fetch()` requests and `GET` Route Handlers are **uncached by default** (`no-store` behavior unless configured otherwise).
- When local `node_modules/next/dist/docs/` exists (injected by `next-agent-rules`), consult it for version-exact caching or configuration APIs.

## 2. Server vs. Client Boundaries & Security

- Use `import "server-only"` in modules that touch database clients (`pg`, `@prisma/client`), SMTP (`nodemailer`), S3/R2 secrets, or internal environment variables.
- Never pass event handlers, functions, or non-serializable class instances from a Server Component to a Client Component.
- Validate all incoming data in Route Handlers (`app/api/**/route.ts`) and Server Actions at the boundary using `zod` before passing to Prisma or SQL queries.
- Sanitize rich HTML (e.g., from `@tiptap/*` editors) server-side using `sanitize-html` or `isomorphic-dompurify` before persisting or rendering with `dangerouslySetInnerHTML`.

## 3. Tailwind CSS v4 (`@tailwindcss/postcss`)

- Check `package.json` and `postcss.config.mjs` before editing styles.
- If the project uses `@tailwindcss/postcss` (Tailwind v4):
  - Configuration is CSS-first inside `globals.css` using `@import "tailwindcss";` and `@theme { ... }` (unless an explicit `@config` directive or legacy `tailwind.config.ts` is already wired in the project).
  - Do not create a redundant `tailwind.config.js` if the project already defines tokens in CSS.
  - Respect existing project design tokens and fluid typography utilities.

## 4. Standalone Build Readiness (`output: "standalone"`)

- Ensure `next.config.ts` preserves `output: "standalone"` when targeting containerized deployments.
- Guard build-time environment evaluation so `npm run build` inside Docker can succeed with build-time placeholder URLs (`SKIP_ENV_VALIDATION=1` or lazy connection initialization) without requiring a live production database during `next build`.
