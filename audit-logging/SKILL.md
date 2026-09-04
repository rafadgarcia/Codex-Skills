---
name: audit-logging
description: Review, design, or implement audit trails for sensitive business operations such as financial changes, permission changes, administrative actions, impersonation, and destructive operations. Use when the user explicitly requests audit logging or when implementing a clearly sensitive state-changing workflow. Do not use for ordinary application logging, observability, debugging, or routine reads.
---

# Audit Logging

Use this skill to review, design, or implement audit trails for sensitive state-changing operations. The user's explicit request defines the scope. Do not turn an ordinary coding task into a broad audit-logging project merely because the application stores business data.

## Choose the operating mode

- **Review:** Inspect relevant flows and existing evidence, then produce an Audit Coverage Report. Do not modify the project unless implementation was also requested. Read [coverage-review.md](references/coverage-review.md), plus the other references needed to evaluate the evidence.
- **Architecture:** Identify system boundaries, sensitive operations, expected queries, and the relevant threat model. Propose guarantees and trade-offs without inventing legal, retention, approval, or infrastructure requirements. Read [event-model.md](references/event-model.md), [implementation-patterns.md](references/implementation-patterns.md), and [sensitive-data.md](references/sensitive-data.md) as relevant.
- **Implementation:** Limit changes to the requested flows, use the authoritative mutation layer, preserve existing conventions, handle transaction and failure semantics, and add risk-appropriate tests. Read [event-model.md](references/event-model.md), [implementation-patterns.md](references/implementation-patterns.md), [sensitive-data.md](references/sensitive-data.md), and [testing.md](references/testing.md) as relevant.

## Establish context

Before prescribing an implementation, inspect or infer only what matters: language and framework, persistence layer, transaction boundaries, monolith or distributed topology, actor identity, tenant boundaries, existing audit mechanisms, data sensitivity, expected audit queries, and requirements supplied by the user. Do not claim regulatory compliance merely because an audit trail exists.

Prioritize financial changes, permission and privilege changes, administrative actions, impersonation, destructive operations, security-setting changes, privileged jobs, approval workflows, and records whose historical state matters. Routine reads and diagnostics do not automatically require audit events.

## Core invariants

When applicable, evidence must identify what happened, when, the actor, resource, relevant state change, outcome, origin, correlation context, reason, and authorization. Use stable identifiers and distinguish users, impersonators, services, jobs, and API clients.

- Never record a successful mutation when the business operation rolled back.
- Obtain previous state from a trusted server-side source and account for concurrency.
- Avoid secrets, excessive personal data, large blobs, and unrelated fields.
- Keep audit history independent from the lifecycle of the business record.
- Describe the integrity guarantee actually implemented; append-only application behavior alone is not tamper-proof.
- Treat asynchronous workflow stages as distinct events rather than updating historical events.
- Treat `metadata` as optional context, not as a substitute for stable fields needed for queries, security, or reconstruction.

## Finish the task

In implementation mode, inspect the exact flow and its authorization and transaction path, define the minimum event contract, implement at the authoritative mutation layer, verify rollback and sensitive-data behavior, run focused tests, and summarize remaining limitations. Avoid unrelated instrumentation, platform migrations, or approval rules.
