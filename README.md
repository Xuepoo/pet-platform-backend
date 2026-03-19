# Pet Platform - Backend 🐍

The backend API service built with FastAPI and SQLAlchemy.

## Overview

This service provides the REST API for the Pet Platform, handling user authentication, pet management, adoption applications, and lost & found reports.

## Setup

1.  **Install `uv`**:
    This project uses `uv` for fast package management.
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Install Dependencies**:
    ```bash
    cd backend
    uv sync
    ```

3.  **Environment Variables**:
    Copy `.env.example` to `.env` and configure your environment variables:
    ```bash
    cp .env.example .env
    ```
    
    Key variables:
    - `DATABASE_URL`: Connection string for PostgreSQL (e.g., `postgresql+asyncpg://user:pass@localhost:5432/petdb`)
    - `SECRET_KEY`: Secret key for JWT token generation.
    - `ALGORITHM`: Algorithm for JWT (default: `HS256`).
    - `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time.

## Running Locally

1.  **Start Infrastructure**:
    You need Postgres, Redis, and Minio running.
    ```bash
    # Run only infrastructure services from the root directory
    docker compose -f ../deploy/docker-compose.dev.yml up -d postgres redis minio
    ```

2.  **Run Server**:
    ```bash
    # From backend directory
    uv run uvicorn app.main:app --reload
    ```
    The API will be available at [http://localhost:8000](http://localhost:8000).

3.  **API Documentation**:
    - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
    - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Database Migrations

We use Alembic for database migrations.

-   **Create a migration**:
    ```bash
    uv run alembic revision --autogenerate -m "description of changes"
    ```

-   **Apply migrations**:
    ```bash
    uv run alembic upgrade head
    ```

## Testing

Run tests with `pytest`:
```bash
uv run pytest
```

### End-to-End Verification

To verify the critical paths of the system (Register -> Login -> Create Pet -> List Pets), run:
```bash
python verify_system.py
```

## Project Structure

```
backend/
├── alembic/          # Database migration scripts
├── app/
│   ├── api/          # API route handlers (v1/)
│   ├── core/         # Config, security, database setup
│   ├── models/       # SQLAlchemy database models
│   ├── schemas/      # Pydantic schemas for request/response
│   ├── services/     # Business logic services
│   └── main.py       # Application entry point
├── scripts/          # Utility scripts (seeding, maintenance, manual tests)
├── tests/            # Pytest test suite
├── pyproject.toml    # Project dependencies and config
└── uv.lock           # Dependency lock file
```

## Utility Scripts

The `scripts/` directory contains useful tools for managing the application:

- `reseed_data.py`: Resets and seeds the database with initial data.
- `create_test_users.py`: Creates test users for development.
- `verify_system.py`: Checks system health and configuration.

To run a script:
```bash
uv run python scripts/reseed_data.py
```
