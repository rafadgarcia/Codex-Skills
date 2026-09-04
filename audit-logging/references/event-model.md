# Audit Event Model

Use a structured, versioned event contract. Adapt optional fields to the domain instead of creating empty placeholders.

```text
AuditEvent
├── id
├── schema_version
├── event_type
├── occurred_at
├── recorded_at?
├── outcome
├── failure_code?
├── actor
│   ├── type
│   ├── id
│   └── impersonator_id?
├── tenant_id?
├── resource
│   ├── type
│   └── id
├── change?
│   ├── before
│   ├── after
│   └── changed_fields
├── authorization?
│   ├── requested_by
│   ├── approved_by
│   └── approved_at
├── context
│   ├── reason?
│   ├── request_id?
│   ├── correlation_id?
│   ├── trace_id?
│   ├── job_id?
│   └── idempotency_key?
└── metadata
```

## Time and identity

Persist timestamps in UTC from a trusted server clock. `occurred_at` is when the audited event occurred; `recorded_at` is when it was persisted or ingested when those moments can differ.

Use immutable actor and resource identifiers where possible. Actor types may include `USER`, `SYSTEM`, `SERVICE`, `JOB`, and `API_KEY`. Record an impersonated identity and its impersonator separately. Human-readable names or e-mail addresses are optional snapshots, never the sole identity.

## Outcome

- `SUCCEEDED`: the audited operation reached its intended business state.
- `DENIED`: authorization, policy, or a business control prevented execution.
- `FAILED`: a technical or operational attempt did not reach the intended state.

Use a stable, machine-readable `failure_code` when useful. A `FAILED` event must not imply that a reverted mutation was applied. For asynchronous workflows, emit immutable stage events such as `EXPORT_REQUESTED`, `EXPORT_STARTED`, `EXPORT_COMPLETED`, and `EXPORT_FAILED`; do not update an earlier event into a new status.

## Event names and changes

Use specific, stable past-tense names such as `PAYMENT_CANCELLED`, `PERIOD_REOPENED`, or `USER_ROLE_CHANGED`. Avoid vague types such as `UPDATED`, `CHANGE`, and `ADMIN_EVENT`. Version the schema independently from event names.

For important mutations, capture the minimum relevant `before`, `after`, and `changed_fields`. Read previous state from the authoritative server-side source. Do not blindly snapshot whole rows or accept client-supplied `oldValue` as evidence.

## Correlation and idempotency

Use `request_id`, `correlation_id`, `trace_id`, and `job_id` only when the architecture provides them. Propagate identifiers across derived jobs and downstream calls when practical. For outbox or at-least-once delivery, use a stable event ID or idempotency key and enforce deduplication at the appropriate boundary.

## Batch operations

- Emit individual events when each resource must be reconstructed.
- Emit an aggregate event when the collective action has business meaning.
- Emit both when both perspectives matter, sharing a correlation ID.

Never place thousands of resources in one `before` or `after`. For example, `BULK_PRICE_UPDATE_STARTED` may correlate with many `PRODUCT_PRICE_CHANGED` events.

## Metadata

Keep fields required for querying, access control, integrity, or reconstruction in the stable schema. Use `metadata` only for non-essential supplemental context, with the same redaction and size controls as the rest of the event.
