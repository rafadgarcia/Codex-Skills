# Audit Logging Tests

Select tests according to the risks and architecture of the implemented flow. Do not require every case for every change, and do not write tests that merely mirror field assignments.

## Core correctness

- A committed mutation emits the intended event exactly once at the relevant logical boundary.
- Actor, resource, event type, outcome, and timestamps are correct.
- `before`, `after`, and `changed_fields` match authoritative persisted state.
- A rollback does not leave a false `SUCCEEDED` event.
- A denied action is represented as `DENIED` without implying mutation.
- A technical failure uses `FAILED` only when recording the attempt is intentional and semantically accurate.

## Identity and authorization

- Automated jobs and services have distinguishable stable identities.
- Impersonated identity and impersonator are both preserved.
- Requester and approver are correct when approval exists.
- Client-provided identity or previous state cannot override trusted server context.

## Sensitive data and access

- Forbidden secrets are absent from top-level fields, nested changes, metadata, and error context.
- Redaction and field-size controls cover bulk and malformed inputs.
- Audit queries and exports enforce authorization.
- Tenant isolation is tested in multi-tenant systems; omit this test for genuinely single-tenant systems.

## Transactions and delivery

- Concurrent mutations do not produce misleading previous or resulting state.
- Outbox records share the business transaction where intended.
- Duplicate queue delivery is deduplicated by event ID or idempotency key.
- Retries preserve correlation and do not create logically duplicated events.
- Asynchronous stages produce distinct immutable events with accurate outcomes.

## Lifecycle and scale

- Deleting a resource does not cascade into its audit history.
- Batch operations follow the selected aggregate, per-resource, or combined policy without oversized payloads.
- Retention or expiry processes cannot be invoked through ordinary application permissions and are auditable when required.

Run the smallest relevant tests first, then the project's normal checks appropriate to the changed components. Report untested guarantees when required infrastructure is unavailable.
