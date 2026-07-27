# Generics And Utility Types

Use advanced types to preserve relationships between values. Do not use them to impress the compiler.

## When Generics Help

Use generics when:

- input and output types are related
- a helper works over many shapes but preserves each shape
- a component or hook should infer caller-provided data
- a library API needs stable public contracts

Avoid generics when a concrete type is clearer.

## Generic Constraints

Constrain only what the function actually uses:

```ts
function byId<T extends { id: string }>(items: T[]): Record<string, T> {
  return Object.fromEntries(items.map((item) => [item.id, item]));
}
```

Do not add generic parameters that can be removed without losing information.

## Mapped Types

Use mapped types for mechanical transformations:

```ts
type Nullable<T> = {
  [K in keyof T]: T[K] | null;
};
```

Keep exported mapped types small and named by domain intent.

## Conditional Types

Use conditional types when a type relationship cannot be represented directly:

```ts
type AwaitedValue<T> = T extends Promise<infer R> ? R : T;
```

If a conditional type takes more time to understand than duplicated simple types, prefer clarity.

## Utility Types

Common choices:

- `Pick<T, K>` for public subsets
- `Omit<T, K>` for internal-to-public transformations
- `Partial<T>` for patches, not complete domain objects
- `Required<T>` when normalizing optional inputs
- `Record<K, V>` for known key sets or dictionary-like maps
- `ReturnType<F>` and `Parameters<F>` for derived function contracts

Avoid stacking many utility types in exported signatures.

## Template Literal Types

Use template literal types for constrained strings that are truly patterned:

```ts
type EventName<Entity extends string> = `${Entity}:created` | `${Entity}:updated`;
```

Do not encode a full parser in types.

## Public API Rule

For exported helpers and packages, favor understandable types over maximum inference. Consumers should understand compiler errors without reading the implementation.
