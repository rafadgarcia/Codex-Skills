# Runtime Boundaries

TypeScript types end at runtime boundaries. Validate data before treating it as trusted.

## Validate These Boundaries

- HTTP request bodies, params, and query strings
- `fetch().json()` and third-party API responses
- environment variables
- local storage and cookies
- file contents and uploads
- webhook payloads
- database JSON columns
- queue and message payloads
- AI/model/tool output

## Preferred Pattern

Parse once at the boundary, then pass typed values inward:

```ts
import { z } from "zod";

const UserInput = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
});

type UserInput = z.infer<typeof UserInput>;

export function parseUserInput(value: unknown): UserInput {
  return UserInput.parse(value);
}
```

Use `safeParse` when the caller needs to return a controlled validation error.

## API Contracts

Keep request and response schemas close to the route, controller, or contract layer. Avoid duplicating static types and runtime schemas by hand.

Good pattern:

```ts
const CreatePostRequest = z.object({
  title: z.string().min(1),
  body: z.string().min(1),
});

type CreatePostRequest = z.infer<typeof CreatePostRequest>;
```

Avoid:

```ts
type CreatePostRequest = { title: string; body: string };
const body = req.body as CreatePostRequest;
```

## Environment Variables

Validate environment once during startup:

```ts
const Env = z.object({
  DATABASE_URL: z.string().url(),
  NODE_ENV: z.enum(["development", "test", "production"]),
});

export const env = Env.parse(process.env);
```

Do not scatter `process.env.X!` throughout application code.

## Errors

Use `unknown` in catches:

```ts
try {
  await work();
} catch (error: unknown) {
  const message = error instanceof Error ? error.message : "Unknown error";
}
```

Expose safe error messages to users and logs appropriate details internally.

## Security Notes

Types are not authorization. A type-safe `userId` can still be the wrong user's ID.

For security-sensitive boundaries, combine this skill with `$secure-web-apps`.
