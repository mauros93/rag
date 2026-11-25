# PROJECT CONTEXT — Modular RAG Application

## 1. Project overview

Build a document-based RAG (Retrieval-Augmented Generation) application using Python and FastAPI.

The application will allow users to manage documents, process their content, retrieve relevant information, and interact with an LLM using contextual information extracted from those documents.

The project will be developed incrementally through multiple versions.

**Current development scope: Version 1 — FastAPI + PostgreSQL + CRUD.**

Do not implement future-version functionality until explicitly requested.

## 2. Architectural approach

The application must follow a **Modular Monolithic Architecture**.

This means:

- The application is deployed as one logical application.
- The codebase is divided into independent modules with clearly defined responsibilities.
- Business logic must not depend directly on HTTP or infrastructure details.
- Modules should communicate through explicit interfaces and well-defined dependencies.
- The architecture must allow future functionality without requiring a complete restructuring.

Do not introduce microservices at this stage.

## 3. Engineering principles

Apply industry-standard software engineering practices.

### SOLID principles

- **S — Single Responsibility Principle:** Each module and class must have one clearly defined responsibility.
- **O — Open/Closed Principle:** Components should be extensible without unnecessary modification of existing code.
- **L — Liskov Substitution Principle:** Implementations must be replaceable without breaking expected behavior.
- **I — Interface Segregation Principle:** Avoid unnecessarily large interfaces.
- **D — Dependency Inversion Principle:** High-level business logic should not depend directly on low-level infrastructure implementations.

Apply these principles pragmatically. Do not create unnecessary abstractions just to satisfy a principle.

### Additional principles

- DRY: Avoid unnecessary code duplication.
- KISS: Prefer simple and understandable solutions.
- Separation of Concerns: Keep responsibilities separated.
- Explicit Dependencies: Make component dependencies clear.
- Clean Code: Use descriptive names, small functions and consistent conventions.
- Fail Fast: Detect invalid states and configuration errors early.
- Secure by Default: Never expose secrets or sensitive information.

## 4. Design patterns

Use design patterns when they solve an actual architectural problem.

Patterns that may be useful:

- Repository Pattern: Encapsulate database access.
- Dependency Injection: Manage dependencies between components.
- Service Layer: Centralize business logic.
- Factory Pattern: Introduce only when object creation becomes sufficiently complex.
- Adapter Pattern: Useful later for integrating different embedding providers, vector databases and LLM providers.

Do not implement patterns unnecessarily.

## 5. Technology stack

### Current version

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy 2.x
- Pydantic 2.x
- Psycopg 3
- Alembic
- Pytest
- HTTPX
- Ruff

### Planned future technologies

These technologies are part of the roadmap, not the current implementation:

- Docker and Docker Compose.
- JWT authentication and password hashing.
- Document processing.
- PyMuPDF and Tesseract OCR.
- Chroma vector database.
- Sentence Transformers and embeddings.
- LangChain.
- Ollama or another LLM provider.
- Conversational memory and RAG evaluation.

## 6. Initial project structure

Use the following structure for Version 1:

```text
rag-project/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── base.py
│   │
│   ├── models/
│   │   └── user.py
│   │
│   ├── schemas/
│   │   └── user.py
│   │
│   ├── repositories/
│   │   └── user_repository.py
│   │
│   ├── services/
│   │   └── user_service.py
│   │
│   └── routers/
│       └── users.py
│
├── tests/
│
├── alembic/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

Folders and files must be added progressively as new functionality is implemented.

## 7. Component responsibilities

### main.py
Application entry point. Creates the FastAPI instance and registers routers.

### core/
Global application configuration and cross-cutting concerns.

### db/
Database engine, session management and SQLAlchemy base configuration.

### models/
SQLAlchemy models representing database entities.

### schemas/
Pydantic schemas for request validation and response serialization.

### repositories/
Database access operations. Encapsulate SQLAlchemy queries and persistence logic.

### services/
Business logic. Coordinate operations and enforce application rules.

### routers/
HTTP endpoints. Receive requests, validate input, delegate to services and return responses.

### tests/
Unit tests and integration tests.

### alembic/
Database schema migrations.

## 8. Expected application flow

The preferred flow for a CRUD operation is:

HTTP Client
    ↓
Router
    ↓
Service
    ↓
Repository
    ↓
Database

Responsibilities must remain separated.

Routers must not contain database queries or substantial business logic.

Services must not depend directly on FastAPI request or response objects.

Repositories must not contain HTTP-related logic.

## 9. Development roadmap

### Version 1 — API and CRUD
- Configure FastAPI.
- Configure PostgreSQL.
- Configure SQLAlchemy.
- Implement database models and Pydantic schemas.
- Implement CRUD operations.
- Separate routers, services and repositories.
- Add database migrations.
- Add basic automated tests.

### Version 2 — Authentication and authorization
- User registration and login.
- Secure password hashing.
- JWT authentication.
- Authorization and access control.
- Protect user resources.

### Version 3 — Containerization
- Dockerfile.
- Docker Compose.
- PostgreSQL container.
- Persistent database storage.
- Environment-based configuration.

### Version 4 — Document management
- Document upload.
- File validation.
- File storage.
- Text extraction.
- Document processing workflow.

### Version 5 — RAG
- Text chunking.
- Embedding generation.
- Chroma integration.
- Similarity search.
- Retrieval pipeline.
- LLM integration.
- Context construction and response generation.

### Version 6 — Advanced capabilities
- OCR for scanned documents and images.
- Conversational memory.
- Conversation and message persistence.
- RAG evaluation.
- Retrieval quality improvements.

## 10. Rules for AI-assisted development

Any AI working on this project must follow these rules:

1. Respect the current project version and do not implement future functionality prematurely.
2. Explain architectural decisions and their trade-offs.
3. Follow SOLID principles and separation of concerns.
4. Avoid unnecessary abstractions and overengineering.
5. Preserve the existing folder structure unless there is a justified reason to change it.
6. Do not put business logic in routers.
7. Do not put database queries in services or routers; use repositories.
8. Use SQLAlchemy 2.x conventions.
9. Use Pydantic 2.x conventions.
10. Use environment variables for configuration and never hardcode secrets.
11. Include appropriate error handling and input validation.
12. Write automated tests for relevant functionality.
13. Use type hints and descriptive naming.
14. Prefer maintainable, readable and testable solutions over clever or unnecessarily complex implementations.
15. Before adding a dependency, explain why it is necessary.
16. Implement one logical feature at a time and explain the changes before moving to the next feature.

**Primary objective:** Build a maintainable, testable and extensible modular monolithic application that can progressively evolve into a production-oriented RAG system.