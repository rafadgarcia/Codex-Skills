# Audit Coverage Review

Review only the requested repository scope. Trace findings to concrete code evidence rather than assuming behavior from names or architecture diagrams.

## Method

1. Locate authoritative endpoints, handlers, services, jobs, consumers, commands, and database paths that mutate sensitive state.
2. Identify existing audit abstractions, database triggers, outbox records, CDC pipelines, security logs, and application logs.
3. Trace actor identity, authorization, previous state, mutation, transaction boundary, emitted event, persistence, and downstream delivery.
4. Check destructive paths, bulk operations, bypasses, administrative tools, imports, retries, and failure handling.
5. Check whether secrets or excessive personal data enter audit payloads and whether tenant isolation is enforced.
6. Report gaps before proposing broad implementation work.

## Evidence requirement

Every code-based finding should, when possible, cite the file path and tight line range or relevant symbol. Do not present a flow as fact unless it can be traced to repository evidence. Clearly label inferences and missing evidence.

## Dimensions

Keep these independent:

- **Business criticality:** `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`.
- **Audit coverage:** `COMPLETE`, `PARTIAL`, `MISSING`, `NOT_APPLICABLE`.
- **Finding severity:** `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO`.

Business criticality measures impact of the flow. Coverage measures current evidence. Finding severity measures a specific weakness. Do not infer one solely from another.

## Finding format

```text
Finding: AUD-004
Flow: Reopen accounting period

Business criticality: CRITICAL
Audit coverage: MISSING
Finding severity: HIGH

Evidence:
- src/services/accounting.ts:184 — AccountingService.reopenPeriod()
- src/policies/accounting.ts:51 — authorization rule

Existing evidence:
- actor ID and affected period are available

Missing or unreliable evidence:
- previous state
- emitted audit event
- approval identity, if approval is required

Risk:
The historical adjustment cannot be reliably reconstructed.

Recommendation:
Capture relevant before/after state in the mutation transaction and emit the domain event from the authoritative service.
```

Prioritize actionable gaps in sensitive flows. Do not inflate the report with trivial CRUD operations. If the code is incomplete, generated, unreachable, or depends on external behavior, state the limitation.
