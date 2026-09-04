---
name: typescript-engineering
description: "Use for TypeScript engineering work: type design, tsconfig/compiler options, strictness, JavaScript-to-TypeScript migration, runtime validation boundaries, unknown vs any, type guards, discriminated unions, generics, utility types, React TypeScript patterns, Node/browser toolchains, ESLint, Vitest, and type-safe API contracts."
---

# TypeScript Engineering

## Overview

Use TypeScript to make invalid states harder to express while keeping code readable, local, and aligned with the existing project. Prefer practical type safety over type cleverness.

## First Checks

Before changing TypeScript code or configuration:

- Inspect the local `package.json`, `tsconfig*.json`, lockfile, framework, runtime, and existing style.
- Prefer the package manager and scripts already used by the project.
- Use installed package types and local docs first. For version-sensitive compiler, framework, or lint behavior, verify against current official documentation.
- Do not upgrade TypeScript, Node, React, framework versions, or lint tooling unless the task requires it.
- Avoid repository-wide strictness changes unless the user asked for a migration or the blast radius is small and tested.

## Working Rules

- Treat external data as `unknown` until validated or narrowed.
- Prefer runtime validation at boundaries: HTTP bodies, `fetch().json()`, environment variables, local storage, third-party SDK payloads, webhooks, and AI/model output.
- Prefer `satisfies`, type guards, discriminated unions, and inferred schema types over broad `as` assertions.
- Avoid `any` in new code. If compatibility requires it, isolate it, narrow quickly, and explain why.
- Keep advanced types proportional. If a type makes normal maintenance harder, simplify the model or move complexity behind a small helper.
- Preserve local conventions unless they are directly causing incorrectness or unsafe typing.

## Task Routing

- **Type system design**: Read `references/type-system.md`.
- **Runtime boundaries, validation, env, API contracts**: Read `references/runtime-boundaries.md`; apply the project's existing security requirements when user data, authentication, payments, webhooks, or abuse resistance are involved.
- **Generics, mapped types, conditional types, utility types**: Read `references/generics-and-utility-types.md`.
- **React TypeScript components, hooks, events, forms, state**: Read `references/react-typescript.md`; combine with `$frontend-design` for UI implementation.
- **JS-to-TS migration or strictness rollout**: Read `references/migration.md`.
- **tsconfig, ESLint, tests, package scripts, build tooling**: Read `references/toolchain.md`.

## Implementation Workflow

1. Locate the boundary: public API, component props, domain model, data fetch, config, or internal helper.
2. Prefer making the boundary explicit before adding deeper internal types.
3. Let TypeScript infer obvious local values; annotate public contracts, exported functions, reusable helpers, and non-obvious generics.
4. Replace assertions with narrowing or validation where data is not trusted.
5. Run the existing typecheck, lint, and tests when available.
6. If errors are numerous, fix by category and avoid hiding them with blanket suppressions.

## Config Guidance

Use strictness as a ratchet:

- New projects: prefer `strict`, `noUncheckedIndexedAccess`, and `exactOptionalPropertyTypes` when compatible.
- Existing projects: enable stricter flags incrementally and measure error count first.
- Libraries: consider declarations, `declarationMap`, public API stability, and consumer module formats.
- Apps: optimize for framework compatibility and build reliability before idealized config.

Use `assets/tsconfig-strict.json` and `assets/eslint-flat-config.js` as starting points, not universal drop-ins.

## Anti-Patterns

- Using `as SomeType` on parsed JSON, request bodies, env vars, or local storage without validation.
- Replacing unknown errors with `catch (e: any)`.
- Adding generic parameters that can be inferred.
- Encoding business rules only in types when runtime validation is still required.
- Using enums for simple string states when literal unions are enough.
- Exporting deep utility types that couple unrelated modules.
- Silencing errors with `// @ts-ignore`, `skipLibCheck`, or broad `any` instead of isolating the real issue.

## Assets

- `assets/tsconfig-strict.json`: strict baseline to adapt to the project's runtime and framework.
- `assets/eslint-flat-config.js`: ESLint flat config baseline for typed linting.
