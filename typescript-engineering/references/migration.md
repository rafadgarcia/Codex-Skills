# Migration

Use this reference when migrating JavaScript to TypeScript or tightening an existing TypeScript codebase.

## Migration Principles

- Migrate in small, testable slices.
- Preserve runtime behavior first.
- Add types at boundaries before deep internals.
- Measure errors before enabling stricter flags.
- Avoid suppressions that hide real design issues.

## JavaScript To TypeScript

Start with project discovery:

- package manager and scripts
- current module system
- test framework
- bundler/framework
- source directories
- generated files

Then migrate incrementally:

1. Add `tsconfig.json` compatible with the current runtime.
2. Enable `allowJs` if needed.
3. Rename leaf files first.
4. Add public function and module boundary types.
5. Replace unsafe imports/exports.
6. Run tests and typecheck after each slice.

## Strictness Rollout

Useful order for existing projects:

1. `strict`
2. `noImplicitAny`
3. `strictNullChecks`
4. `noUncheckedIndexedAccess`
5. `exactOptionalPropertyTypes`
6. project-specific lint rules

The exact order depends on current errors. Do not enable a flag and then silence hundreds of errors.

## Suppression Policy

Prefer:

```ts
// @ts-expect-error: library type is missing overload for documented runtime behavior
```

Avoid:

```ts
// @ts-ignore
```

Every suppression should be narrow, explained, and removable.

## Common Migration Hotspots

- CommonJS and ESM interop
- implicit `any` from untyped callbacks
- JSON imports
- test globals
- DOM vs Node libraries
- path aliases
- environment variables
- generated clients and SDKs

## Stop Conditions

Pause and reassess if type fixes require unrelated architectural rewrites, package upgrades, or large behavior changes.
