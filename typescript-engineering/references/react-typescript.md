# React TypeScript

Use this reference for React components, hooks, events, forms, and state.

## Component Props

Type props explicitly:

```tsx
type ButtonProps = {
  children: React.ReactNode;
  variant?: "primary" | "secondary";
  onClick?: () => void;
};

export function Button({ children, variant = "primary", onClick }: ButtonProps) {
  return <button onClick={onClick} data-variant={variant}>{children}</button>;
}
```

Do not use `React.FC` by default. It is acceptable in projects that already standardize on it.

## Discriminated Props

Use discriminated unions when prop combinations change behavior:

```tsx
type LinkButtonProps =
  | { as: "button"; onClick: () => void; href?: never }
  | { as: "link"; href: string; onClick?: never };
```

This is better than many optional props with runtime-only constraints.

## Events

Use specific event types when handlers are exported or reused:

```tsx
function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
  event.preventDefault();
}
```

Inline handlers often infer correctly; avoid adding noise when inference is clear.

## Hooks

Let `useState` infer simple values:

```tsx
const [open, setOpen] = useState(false);
```

Annotate empty collections and nullable state:

```tsx
const [items, setItems] = useState<Item[]>([]);
const [user, setUser] = useState<User | null>(null);
```

Type refs with the target element:

```tsx
const inputRef = useRef<HTMLInputElement>(null);
```

## Context

Avoid unsafe default values:

```tsx
const SessionContext = createContext<Session | null>(null);
```

Expose a hook that throws if the provider is missing.

## Forms

Form values come from runtime. Validate before using them as domain values, especially before API calls.

Prefer schema-backed parsing for non-trivial forms.

## Polymorphic Components

Only use polymorphic `as` components when a design system genuinely needs them. They add type complexity and can harm accessibility if semantics are unclear.

## Server And Client Boundaries

In frameworks with server/client boundaries, keep server-only values, secrets, and database types out of client props. Serialize explicitly and validate incoming client data on the server.
