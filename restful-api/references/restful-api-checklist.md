# RESTful API checklist

Before finishing API work, verify:

## Route Design

- [ ] Endpoints are resource-oriented.
- [ ] Paths use nouns instead of action verbs.
- [ ] Resource names are consistent.
- [ ] Collection resources are plural unless the project convention differs.
- [ ] No RPC-style endpoint was introduced unless explicitly requested.
- [ ] Trailing slashes follow the project convention.
- [ ] Nested routes are clear and not excessively deep.

## HTTP Methods

- [ ] `GET` only reads or lists data.
- [ ] `POST` creates resources or performs non-idempotent operations.
- [ ] `PUT` replaces or updates entire resources.
- [ ] `PATCH` partially updates resources.
- [ ] `DELETE` removes resources.

## Status Codes

- [ ] `200 OK` is used for successful responses with a body.
- [ ] `201 Created` is used after successful resource creation.
- [ ] `204 No Content` is used only when no response body is returned.
- [ ] `400 Bad Request` is used for malformed or invalid requests.
- [ ] `401 Unauthorized` is used for missing or invalid authentication.
- [ ] `403 Forbidden` is used for authenticated users without permission.
- [ ] `404 Not Found` is used for missing resources.
- [ ] `409 Conflict` is used for state conflicts.
- [ ] `422 Unprocessable Entity` is used only if the project uses this convention.
- [ ] `500 Internal Server Error` is reserved for unexpected server errors.

## Validation

- [ ] Route params are validated.
- [ ] Query params are validated.
- [ ] Request bodies are validated.
- [ ] Important headers are validated when applicable.
- [ ] Invalid input returns a clear client-safe error response.
- [ ] Client-provided data is not trusted blindly.

## Responses

- [ ] Success responses follow the project convention.
- [ ] Error responses follow the project convention.
- [ ] Error messages are useful for API consumers.
- [ ] Internal implementation details are not exposed.
- [ ] Sensitive information is not exposed.
- [ ] The client receives a response for expected failure cases.

## Collections

- [ ] List endpoints use pagination when result sets may grow.
- [ ] Filtering is supported when useful.
- [ ] Sorting is supported when useful.
- [ ] Search is supported when useful.
- [ ] Large unbounded responses are avoided.

## Security

- [ ] Authentication is checked when required.
- [ ] Authorization is checked when required.
- [ ] `401` and `403` are used correctly.
- [ ] Resource ownership or tenant boundaries are enforced when applicable.

## Project Consistency

- [ ] Existing folder structure is followed.
- [ ] Existing validation patterns are followed.
- [ ] Existing error handling patterns are followed.
- [ ] Existing response formats are followed.
- [ ] Existing authentication and authorization patterns are followed.
- [ ] Existing test patterns are followed.
- [ ] Existing documentation patterns are followed.

## Tests and Docs

- [ ] Tests were added or updated when the project has tests.
- [ ] API documentation was added or updated when the project has documentation.
- [ ] Examples were added when helpful.
