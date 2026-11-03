---
name: docker-caddy-vps
description: "Use when writing or reviewing Dockerfiles, compose.yaml / docker-compose.yml files, container healthchecks, Caddy reverse proxy configs, or VPS deployment workflows for Node.js, Fastify, Vite/Nginx, or Next.js standalone applications."
metadata:
  short-description: "Docker Compose, Next.js Standalone & Caddy edge patterns"
---

# Docker, Caddy & VPS Deployment Patterns

Use this skill when creating, reviewing, or troubleshooting `Dockerfile`, `docker-compose*.yml` / `compose.yaml`, container healthchecks, or Caddy edge routing for production and staging VPS environments.

## 1. Core Infrastructure Invariants

1. **PID 1 & Zombie Process Prevention (`init: true`):**
   - Always set `init: true` on Node.js, Next.js, Fastify, and worker services in Docker Compose so signal forwarding (`SIGTERM`) and child process reaping work cleanly.
2. **Network Isolation (`edge` + internal bridge):**
   - Connect public-facing application containers to both the external `edge` network (shared with Caddy) and a project-scoped internal bridge network (e.g., `jbc_internal`).
   - Database containers (`postgres:16` / `postgres:16-alpine`) MUST only attach to the internal bridge network—never expose production database ports (`5432`) to `0.0.0.0` on the public host or the `edge` network.
   - Use `expose: ["3000"]` instead of `ports: ["3000:3000"]` for apps proxied by Caddy over the `edge` network.
3. **Log Rotation Protection:**
   - Prevent runaway container logs from exhausting NVMe disk space by configuring `logging` limits on long-running services when not already enforced globally:
     ```yaml
     logging:
       driver: "json-file"
       options:
         max-size: "10m"
         max-file: "3"
     ```
4. **Healthchecks & Startup Ordering:**
   - Every app and database service must define a deterministic `healthcheck`.
   - Use `depends_on` with `condition: service_healthy` so the application waits for PostgreSQL before running migrations or accepting traffic.
   - Provide a lightweight `/api/health` (or `/health`) endpoint in HTTP services for Docker and Uptime Kuma monitoring.

## 2. Reference Templates

### A. Multi-Stage `Dockerfile` for Next.js Standalone + Prisma

```dockerfile
# Stage 1: Dependencies
FROM node:22-bookworm-slim AS deps
RUN apt-get update \
  && apt-get install -y --no-install-recommends openssl libc6 \
  && rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

# Stage 2: Builder
FROM node:22-bookworm-slim AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production
ENV SKIP_ENV_VALIDATION=1

# If Prisma is used, generate client before build
RUN npx prisma generate
RUN npm run build

# Stage 3: Production Runner
FROM node:22-bookworm-slim AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

RUN apt-get update \
  && apt-get install -y --no-install-recommends openssl libc6 \
  && rm -rf /var/lib/apt/lists/* \
  && addgroup --system --gid 1001 nodejs \
  && adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
```

### B. Production `compose.yaml` Pattern (App + Isolated Postgres + Caddy `edge`)

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    init: true
    restart: unless-stopped
    env_file:
      - .env.production
    depends_on:
      postgres:
        condition: service_healthy
    expose:
      - "3000"
    healthcheck:
      test:
        [
          "CMD-SHELL",
          "node -e \"fetch('http://127.0.0.1:3000/api/health').then((r)=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))\"",
        ]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    networks:
      - internal_net
      - edge

  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    env_file:
      - .env.production
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB"]
      interval: 10s
      timeout: 5s
      retries: 5
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    networks:
      - internal_net

volumes:
  postgres_data:

networks:
  internal_net:
    driver: bridge
  edge:
    external: true
```

## 3. Pre-Deploy Verification Checklist

- Confirm `.dockerignore` excludes `node_modules`, `.next`, `.git`, `.env*` (except `.env.example`), and local logs.
- Confirm `output: "standalone"` is set in `next.config.ts` when using the standalone runner stage.
- Ensure uploaded files or persistent user assets go to object storage (Cloudflare R2 via S3 SDK) rather than ephemeral container filesystems.
