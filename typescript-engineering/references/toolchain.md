# Toolchain

Use this reference for TypeScript config, linting, testing, and build setup.

## Configuration First

Read all local configs before editing:

- `package.json`
- `tsconfig.json`
- `tsconfig.*.json`
- `eslint.config.*` or `.eslintrc*`
- framework config
- test config
- lockfile

Do not replace a working project config with a generic template.

## Compiler Options

Good defaults for many projects:

- `strict`
- `noUncheckedIndexedAccess`
- `exactOptionalPropertyTypes`
- `noFallthroughCasesInSwitch`
- `forceConsistentCasingInFileNames`
- `skipLibCheck` for practical build performance

Use with care:

- `noPropertyAccessFromIndexSignature`: good for dictionary-heavy code, noisy in some projects
- `verbatimModuleSyntax`: useful for modern ESM, can expose interop issues
- `isolatedModules`: required by many transpiler-based builds

## Module Resolution

Match the runtime and framework:

- Browser bundlers and modern frontend frameworks often use `moduleResolution: "Bundler"`.
- Node ESM often uses `module: "NodeNext"` and `moduleResolution: "NodeNext"`.
- Existing CommonJS projects may need a more gradual migration.

Do not force ESM or bundler resolution into projects that are not ready for it.

## Typed Linting

Typed linting catches important issues such as floating promises and unsafe assignments, but it is slower and needs project-aware parser setup.

Apply typed linting first to source files, then widen coverage if performance is acceptable.

Rules worth considering:

- no floating promises
- no unsafe assignment/member access
- consistent type imports
- no unnecessary type assertions
- no explicit `any`

Tune generated files, config files, and test files separately.

## Testing

Use the project's existing test runner. Do not switch to Vitest or Jest unless asked.

For type-level behavior, prefer small compile-time examples or package-level type tests only when the project already supports them.

## Assets

`../assets/tsconfig-strict.json` and `../assets/eslint-flat-config.js` are starting points. Adapt them to the local runtime, framework, package manager, and module system.
