# Sensitive Data

Audit storage is a sensitive dataset. Apply minimization, access control, tenant isolation, encryption, retention, and redaction according to requirements supplied by the user and the application's context. Do not claim legal or regulatory compliance from audit logging alone.

## Never store directly

- passwords or password hashes;
- access or refresh tokens;
- session cookies or authorization headers;
- API secrets or private keys;
- MFA and recovery codes;
- CVV or full payment-card authentication data;
- integration secrets.

Reject, omit, or consistently redact forbidden fields before persistence. Account for nested values, metadata, error objects, serialized requests, and changes captured from generic ORM hooks.

## Minimize personal and business data

IP addresses, e-mail addresses, user agents, government identifiers, customer data, reasons, and before/after snapshots may be personal or confidential. Store them only when they serve the audit purpose. Prefer stable identifiers and limited field projections over full object copies.

Define who can query the audit store, which fields are visible, and whether access or export must itself be audited. Do not expose unrestricted raw JSON through administrative interfaces.

## Multi-tenancy

Persist tenant identity when relevant and enforce tenant scope in every audit query, export, retention job, and administrative view. Do not trust tenant IDs supplied only by clients. Test that ordinary administrators cannot cross tenant boundaries unless their role explicitly permits it.

## Retention and deletion

Do not invent a retention period or legal basis. Record the policy supplied by the owner and reconcile evidentiary needs with privacy, contractual, and deletion or anonymization obligations. Keep expiry machinery separate from normal application writes, narrowly authorized, and auditable.

When masking is sufficient, preserve only the minimum useful suffix or classification. Ensure logs, queues, dead-letter storage, SIEM exports, backups, and analytics copies apply compatible protections.
