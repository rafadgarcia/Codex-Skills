# Type System

Use this reference for everyday TypeScript type design and review.

## Principles

- Prefer simple structural types over clever type-level programming.
- Let local implementation details infer naturally.
- Annotate exported contracts, public interfaces, component props, API responses, and reusable helpers.
- Model impossible states with discriminated unions when behavior changes by state.
- Use runtime validation for untrusted values; static types do not prove external data.

## `unknown` vs `any`

Use `unknown` for values whose shape is not proven:

```ts
function parsePayload(value: unknown) {
  if (!value || typeof value !== "object") {
    throw new Error("Expected object");
  }
}
```

Avoid `any` in new code. If unavoidable, keep it local and narrow immediately.

## Type Assertions

Prefer `satisfies`, guards, or schemas over assertions.

```ts
const routes = {
  home: "/",
  settings: "/settings",
} satisfies Record<string, string>;
```

Use assertions only when TypeScript cannot express a fact that the code has already guaranteed.

## Discriminated Unions

Use discriminated unions for state machines and branch-specific data:

```ts
type LoadState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; message: string };
```

This is usually clearer than many optional fields on one interface.

## Interface vs Type Alias

Use `interface` when describing object shapes intended for extension or implementation.

Use `type` for unions, intersections, mapped types, primitives, function types, and discriminated unions.

Follow the project's existing convention when the choice is stylistic.

## Optionality

Do not confuse optional with nullable:

```ts
type UserPatch = {
  displayName?: string;
  avatarUrl?: string | null;
};
```

With `exactOptionalPropertyTypes`, absence and `undefined` behave differently. Preserve this when designing patches and forms.

## Branded Types

Use branded types for domain identifiers that are easy to mix up:

```ts
type Brand<T, Name extends string> = T & { readonly __brand: Name };

type UserId = Brand<string, "UserId">;
type TeamId = Brand<string, "TeamId">;
```

Only introduce brands when they prevent real mixups across boundaries.

## Exhaustiveness

Use `never` for exhaustive switches:

```ts
function assertNever(value: never): never {
  throw new Error(`Unexpected value: ${String(value)}`);
}
```

This is useful for role, status, and event handling.
