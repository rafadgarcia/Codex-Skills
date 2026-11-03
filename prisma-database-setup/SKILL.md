---
name: prisma-database-setup
description: Compatibility entry for legacy requests that name prisma-database-setup. For new Prisma setup or connection repair, use the version-matched prisma-orm-setup skill from prisma/skills.
license: MIT
metadata:
  author: prisma
  version: "8.0.0-compatibility"
---

# Deprecated compatibility entry

This skill name is retained for existing integrations. The upstream Prisma
skill now routes setup and connection repair through `prisma-orm-setup`, which
covers Prisma 6, 7, and 8 with provider-specific guidance.

Use the host's installed `prisma-orm-setup` skill when available. If it is not
installed, add it from [prisma/skills](https://github.com/prisma/skills) before
continuing with a new setup or a connection repair.

Keep existing projects on their current Prisma major version unless an upgrade
was explicitly requested. Use `prisma-upgrade-v7` for a Prisma 6 to 7
migration, and use `prisma-client-api` for queries and transactions.

This compatibility entry does not authorize database resets, destructive
migrations, or provider changes by itself.
