# Implementation Patterns

Choose the simplest pattern that supplies the required evidence and failure guarantees in the existing architecture.

## Atomic mutation and audit

For a local relational mutation, prefer the business change and audit insert in the same transaction. Capture authoritative values using the ORM or database features such as `RETURNING`, and use optimistic or pessimistic concurrency control when competing updates could make `before` or `after` misleading.

Do not emit a `SUCCEEDED` event before commit when it could survive a rollback. A technical failure can be represented separately without suggesting that the state change occurred.

## Distributed workflows

Use a transactional outbox when the state change and event publication cannot share the final destination but can share a local transaction. Expect at-least-once delivery: use stable event IDs or idempotency keys and idempotent consumers. Preserve correlation across retries and stages.

Consider database triggers when mutations can bypass the application layer and the database has enough trusted actor context. Consider CDC when architectural requirements justify capturing committed changes centrally. Explain loss of domain context or actor identity these mechanisms may introduce.

## Append-only guarantees

Distinguish the actual protection level:

1. The application exposes insert-only audit APIs.
2. Its database role can insert but not normally update or delete audit rows.
3. Audit storage has separate administrative boundaries.
4. Evidence is independently replicated or externally anchored.
5. WORM-capable storage supplies storage-level retention guarantees.

Administrative expiry or legally required erasure must use a separate, authorized, and itself auditable process. Do not call a system tamper-proof unless the threat model supports that statement.

## Hash chaining

Hash chaining is optional. When justified, define canonical serialization, schema and algorithm versions, deterministic ordering, chain scope, concurrency behavior, verification, and external checkpoints. A chain stored only in the same mutable database can be recomputed by a sufficiently privileged administrator.

Global chains can create contention. Per-tenant, partitioned, or time-windowed chains may scale better but provide different guarantees. Document the chosen boundary and how missing or reordered events are detected.

## Deletes and storage independence

Prevent foreign-key cascades or lifecycle cleanup from removing audit history with the business record. Store enough identifying context to understand the deletion without copying unnecessary sensitive data. Treat restoration as a separate audited event.

## Authorization workflows

Do not impose segregation of duties unless the domain requires it. When it does, record immutable stages such as `CHANGE_REQUESTED`, `CHANGE_APPROVED`, `CHANGE_REJECTED`, and `CHANGE_EXECUTED`, with requester and approver represented independently.
