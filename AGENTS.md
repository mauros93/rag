# AGENTS.md — Engineering Guidelines

## 1. Project Context

This project is a modular monolithic REST API built with:

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy 2.x
- Alembic
- Pydantic
- Argon2id for password hashing
- JWT for authentication and authorization

The project follows a modular architecture using:

**Router → Service → Repository → Database**

The objective is to maintain clean, readable, secure, maintainable, and production-oriented code without introducing unnecessary abstractions.

## 2. General Coding Principles

- Follow PEP 8 and Python best practices.
- Prioritize readability, simplicity, and maintainability.
- Apply SOLID principles when they provide a concrete benefit.
- Avoid unnecessary complexity, premature abstractions, and overengineering.
- Prefer explicit code over clever or unnecessarily compact implementations.
- Use descriptive names for variables, functions, classes, and modules.
- Keep functions focused on a single responsibility.
- Avoid duplicated logic.
- Use Python type hints consistently.
- Use modern Python syntax and features compatible with the project's configured version.
- Do not introduce dependencies without a clear technical justification.

## 3. Documentation and Comments

This is an educational engineering project. Documentation must help developers understand the purpose of each component and how it relates to the application architecture.

- Write all comments and docstrings in Spanish, using clear, concise, and technically accurate language.
- Add concise docstrings to important classes, methods, and functions.
- Explain what a component does, why it exists, and how it interacts with other layers.
- For exceptions, explain when they are raised, which layer raises them, and who handles them.
- For Services and Repositories, explain their responsibilities and interactions.
- For models and relationships, explain their database purpose.
- Explain non-obvious business rules and design decisions.
- Avoid comments that simply repeat the code.
- Do not omit useful documentation just to keep code minimal.
- Avoid excessive comments, long explanations, and comments on every line.
- Update existing documentation whenever its implementation changes.

**Goal:** Code should be understandable both to experienced developers and to someone learning the project's architecture.

## 4. Architecture and Responsibilities

Maintain the existing modular architecture.

### Routers

- Handle HTTP requests and responses.
- Declare endpoints, dependencies, status codes, and response schemas.
- Delegate business logic to Services.
- Avoid direct database queries.
- Avoid implementing business rules.

### Services

- Implement business rules and coordinate application operations.
- Use Repositories for database access.
- Avoid direct SQLAlchemy queries.
- Avoid HTTP-specific logic whenever practical.
- Raise meaningful application or business exceptions.

### Repositories

- Encapsulate database access.
- Use SQLAlchemy 2.x query patterns.
- Keep database operations focused and reusable.
- Avoid business rules and HTTP-specific logic.
- Handle persistence operations and transaction boundaries consistently.

### Models

- Define database tables, columns, relationships, constraints, and indexes.
- Use SQLAlchemy 2.x declarative mappings with `Mapped` and `mapped_column`.
- Keep persistence concerns separate from API validation.

### Schemas

- Use Pydantic for request and response validation.
- Never expose password hashes, secrets, or internal sensitive fields.
- Reject unexpected input fields when appropriate.
- Keep API schemas separate from SQLAlchemy models.

### Core

- Centralize application configuration, security utilities, dependencies, and shared exceptions.
- Do not turn Core into a container for unrelated application logic.

## 5. SQLAlchemy 2.x Requirements

Always use modern SQLAlchemy 2.x APIs.

Preferred query patterns:

```python
from sqlalchemy import select

statement = select(User).where(User.id == user_id)
user = db.scalars(statement).first()
```

Use:

- `select()`
- `Session.scalars()`
- `Session.scalar()`
- `Session.execute()`
- `Mapped`
- `mapped_column()`
- `relationship()`

Never use legacy query patterns such as:

```python
db.query(User).filter(User.id == user_id).first()
```

Do not introduce legacy SQLAlchemy APIs.

## 6. Security Requirements

- Never store plaintext passwords.
- Use the existing Argon2id password hashing implementation.
- Never expose password hashes in API responses.
- Never hardcode secrets, passwords, tokens, or credentials.
- Load sensitive configuration from environment variables.
- Validate JWT signatures and expiration.
- Enforce authorization on protected operations.
- Never trust user-provided ownership identifiers when the authenticated identity is available.
- Prevent users from accessing or modifying resources belonging to other users.
- Never allow public registration to assign administrative roles.
- Validate uploaded files, including file size, extension, and content type.
- Avoid logging passwords, tokens, or sensitive personal information.

## 7. Error Handling

- Use meaningful custom exceptions for application and business errors.
- Keep HTTP-specific exception translation in FastAPI exception handlers or the Router layer.
- Avoid returning raw database or internal exception messages to clients.
- Preserve useful error context for debugging without exposing sensitive information.
- Handle database transactions and rollbacks consistently.
- Never silently ignore unexpected exceptions.

## 8. Database and Migrations

- Use Alembic for schema changes.
- Never modify an already-applied migration to change an existing database schema.
- Generate new migrations for schema modifications.
- Review autogenerated migrations before applying them.
- Avoid destructive database operations unless explicitly authorized.
- Preserve existing data during refactoring.
- Never execute `docker compose down -v` or other commands that delete persistent volumes.

## 9. Refactoring Rules

When refactoring existing code:

- Preserve existing API behavior unless a change is explicitly requested.
- Preserve endpoint paths, HTTP methods, response schemas, and status codes.
- Avoid unrelated modifications.
- Do not rewrite entire modules when a focused change is sufficient.
- Respect the current architecture.
- Identify duplicated logic and inconsistencies before introducing abstractions.
- Explain important architectural changes.
- Do not remove existing functionality without explicit authorization.
- Review imports and dependencies after each modification.

## 10. AI Agent Workflow

Before making changes:

1. Inspect the relevant files and understand their responsibilities.
2. Identify dependencies and affected components.
3. Check whether an equivalent implementation already exists.
4. Propose the smallest appropriate change.
5. Follow the existing project conventions.

After making changes:

1. Review all modified files.
2. Check imports, type hints, and formatting.
3. Verify that the architecture remains consistent.
4. Identify potential security or data-integrity issues.
5. Report which files were modified and why.
6. Explain any assumptions or unresolved concerns.
7. Do not claim that code works unless it has been verified.

Do not run destructive commands or modify environment configuration without explicit authorization.

## 11. Communication

When explaining code changes:

- Be technically precise.
- Explain why a change is necessary.
- Distinguish between required changes and optional improvements.
- Avoid unnecessary abstractions and speculative optimizations.
- Explicitly identify potential breaking changes.
- Do not hide limitations or unverified assumptions.

The priority is correctness, security, maintainability, and architectural consistency—not the amount of code generated.



## 12. Database Transaction Management

- Maintain consistent transaction boundaries across the application.
- Follow the existing Repository transaction management strategy.
- Avoid unnecessary or duplicated commits.
- Use rollback when a database transaction fails.
- Do not mix transaction management responsibilities across multiple layers without a clear justification.
- Ensure database operations preserve data integrity, especially when multiple operations must succeed or fail together.

## 13. Document Ownership and Data Isolation

- Every document operation must enforce ownership using the authenticated user's identity.
- Never trust client-provided `owner_id` when the authenticated identity is available.
- Users must never access, modify, or delete documents belonging to other users unless explicitly authorized.
- Apply ownership validation consistently across all document endpoints and services.
- Prevent cross-user data leakage in document retrieval, processing, and future RAG queries.

## 14. File Upload and Storage Security

- Never use the original uploaded filename directly as a filesystem path.
- Sanitize filenames and prevent path traversal attacks.
- Generate unique storage identifiers to prevent filename collisions.
- Validate file extensions, MIME types, and actual file content when appropriate.
- Enforce maximum upload size limits.
- Never trust client-provided content types without additional validation.
- Prevent unauthorized access to stored files.
- Handle file cleanup consistently when documents are deleted or storage operations fail.

## 15. Dependency Management

- Reuse existing dependencies whenever possible.
- Do not introduce new packages when existing project dependencies provide an adequate solution.
- Do not upgrade, downgrade, or replace package versions without explicit technical justification.
- Keep dependency declarations synchronized with the project's dependency management files.
- Avoid unnecessary dependencies that increase maintenance, security, or compatibility risks.
- Explain the purpose and impact of every newly introduced dependency.

## 16. Incremental Refactoring

- Refactor one module or responsibility at a time.
- Understand the existing implementation before modifying it.
- Preserve existing behavior unless a change is explicitly requested.
- Avoid large architectural changes without first explaining their scope and impact.
- Do not mix unrelated improvements in the same refactoring operation.
- Review all affected imports, dependencies, and component interactions.
- Identify potential breaking changes before applying them.
- Prefer small, verifiable changes over complete rewrites.