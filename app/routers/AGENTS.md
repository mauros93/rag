# Router Documentation Guidelines

## 1. Endpoint Documentation

Every endpoint must include:

- A concise and descriptive `summary`.
- A meaningful `description` explaining its purpose and behavior.
- The appropriate HTTP status code.
- The correct Pydantic `response_model`.
- Relevant response descriptions when necessary.

## 2. Description Content

Descriptions should explain:

- What the endpoint does.
- What information it receives.
- What operation it performs.
- What information it returns.
- Relevant permissions or authentication requirements.
- Important business rules or restrictions.

## 3. Error Responses

Document relevant HTTP error responses using `responses`.

Include only errors that the endpoint can realistically produce, such as:

- 400: Invalid request or business rule violation.
- 401: Authentication required or invalid credentials.
- 403: Insufficient permissions.
- 404: Requested resource not found.
- 409: Resource conflict.

## 4. FastAPI Conventions

- Use FastAPI's `summary`, `description`, `response_description`, and `responses` parameters appropriately.
- Use Pydantic schemas to document request bodies and response structures.
- Use `tags` to organize related endpoints.
- Avoid duplicating information already documented by Pydantic schemas.
- Keep descriptions concise, precise, and useful for API consumers.

## 5. Language and Style

- Write endpoint summaries and descriptions in Spanish.
- Use professional and technically accurate language.
- Avoid unnecessary explanations and redundant documentation.
- Ensure documentation is understandable through Swagger UI and ReDoc.