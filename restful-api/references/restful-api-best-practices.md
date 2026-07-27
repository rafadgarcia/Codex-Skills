# RESTful API best practices

## Route Design

Model endpoints around resources.

Good:

```http
GET /clients
POST /clients
GET /clients/:id
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

Use nested resources when the relationship is clear:

```http
GET /clients/:clientId/orders
GET /clients/:clientId/orders/:orderId
```

Avoid excessive nesting:

```http
GET /companies/:companyId/clients/:clientId/orders/:orderId/items/:itemId/payments/:paymentId
```

When nesting becomes hard to read or authorize, consider a top-level resource endpoint with filters.

## Resource Naming

Prefer plural collection names:

```http
/clients
/products
/orders
/users
```

Keep naming consistent across the API. Do not mix singular and plural names for the same resource unless the project already does so intentionally.

Avoid trailing slashes unless the project standardizes on them:

```http
GET /clients
```

## HTTP Methods

Use method semantics consistently:

- `GET` reads or lists data and should not mutate server state.
- `POST` creates a resource or performs a non-idempotent operation.
- `PUT` replaces or updates an entire resource.
- `PATCH` partially updates a resource.
- `DELETE` removes a resource.

## Status Codes

Use status codes intentionally:

- `200 OK`: success with a response body.
- `201 Created`: successful resource creation.
- `204 No Content`: success without a response body.
- `400 Bad Request`: malformed or invalid request.
- `401 Unauthorized`: missing or invalid authentication.
- `403 Forbidden`: authenticated user lacks permission.
- `404 Not Found`: requested resource does not exist.
- `409 Conflict`: request conflicts with current system state.
- `422 Unprocessable Entity`: semantic validation error, only if used by the project.
- `500 Internal Server Error`: unexpected server errors only.

Do not use `500` for expected client, validation, authentication, authorization, or not-found cases.

## Validation

Validate data at the API boundary:

- route params
- query params
- request bodies
- important headers

Validate identifiers, required fields, field types, string lengths, enums, numeric ranges, and cross-field constraints when applicable.

## Response Shape

Follow the existing project response convention. If none exists, keep responses predictable and avoid exposing internal details.

Simple success response:

```json
{
  "id": "10",
  "name": "Maria",
  "email": "maria@email.com"
}
```

Envelope-style success response:

```json
{
  "data": {
    "id": "10",
    "name": "Maria"
  }
}
```

Structured error response:

```json
{
  "error": {
    "code": "CLIENT_NOT_FOUND",
    "message": "Client not found"
  }
}
```

Avoid leaking implementation details:

```json
{
  "error": "Unique constraint failed"
}
```

Prefer a client-safe message:

```json
{
  "error": "Email already in use"
}
```

## Collections

For list endpoints, consider:

- pagination
- filtering
- sorting
- search

Examples:

```http
GET /clients?page=1&limit=20
GET /clients?status=active
GET /clients?sort=createdAt:desc
GET /clients?search=maria
```

Avoid returning unbounded large lists unless the project explicitly allows it.

## Authentication and Authorization

Authentication identifies the caller. Authorization decides whether the caller can perform the action.

Use:

- `401 Unauthorized` for missing or invalid authentication.
- `403 Forbidden` for authenticated users without permission.

Do not expose sensitive data in success or error responses.

## Documentation and Tests

When the project has API documentation, document:

- endpoint path and method
- route params
- query params
- request body
- success responses
- error responses
- authentication requirements
- examples

When the project has tests, cover:

- success case
- invalid input
- not found
- authentication failure, when applicable
- authorization failure, when applicable
- conflict or business rule failure, when applicable

## Project Consistency

Before introducing a new pattern, inspect and follow existing conventions for:

- folder structure
- route naming
- validation
- error handling
- response format
- authentication and authorization
- test style
- documentation style
- dependency usage
