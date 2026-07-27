---
name: restful-api
description: Use when creating, reviewing, or refactoring HTTP APIs, REST endpoints, CRUD routes, route handlers, controllers, request/response schemas, API documentation, or backend HTTP interfaces. Guides resource-oriented route design, HTTP method semantics, status codes, validation, errors, pagination, security, tests, and documentation while preserving existing project conventions.
---

# RESTful API

Design HTTP APIs around resources, not actions.

Use the existing project conventions first. Before changing or adding endpoints, inspect nearby routes, controllers, schemas, error handlers, response shapes, authentication middleware, tests, and API documentation.

## Core Rules

- Use nouns in paths and HTTP methods for actions.
- Prefer plural resource names for collections.
- Avoid trailing slashes unless the project already standardizes on them.
- Keep route naming, parameter names, response envelopes, errors, and validation style consistent with the project.
- Do not introduce RPC-style endpoints unless explicitly requested or required by an existing project convention.

Prefer:

```http
GET /clients
GET /clients/:id
POST /clients
PUT /clients/:id
PATCH /clients/:id
DELETE /clients/:id
```

Avoid by default:

```http
GET /getClients
POST /createClient
POST /updateClient
GET /deleteClient/:id
```

## Method Semantics

- `GET`: read or list resources; do not mutate server state.
- `POST`: create a resource or perform a non-idempotent operation.
- `PUT`: replace or update an entire resource.
- `PATCH`: partially update a resource.
- `DELETE`: remove a resource.

## Status Codes

- `200 OK`: successful response with a body.
- `201 Created`: resource created successfully.
- `204 No Content`: successful response without a body.
- `400 Bad Request`: malformed or invalid request.
- `401 Unauthorized`: missing or invalid authentication.
- `403 Forbidden`: authenticated but not allowed.
- `404 Not Found`: resource not found.
- `409 Conflict`: conflict with current system state.
- `422 Unprocessable Entity`: semantic validation error, only if used by the project.
- `500 Internal Server Error`: unexpected server error only.

Do not use `500` for validation errors, authentication errors, authorization errors, or missing resources.

## Implementation Guidance

When creating or changing endpoints:

- Validate route params, query params, request bodies, and important headers.
- Return consistent success and error response formats.
- Avoid exposing internal implementation details in API responses.
- Keep route handlers focused on HTTP concerns.
- Put business logic in the existing service, use-case, model, or domain layer when the project has one.
- Add pagination for collection endpoints when result sets may grow.
- Check authentication and authorization requirements.
- Add or update tests when the project has an existing test structure.
- Add or update API documentation when the project has API docs.

## References

Read these references when useful:

- `references/restful-api-best-practices.md`: concise design guidance and examples.
- `references/restful-api-checklist.md`: review checklist before finishing API work.
