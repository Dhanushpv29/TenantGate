# TenantGate — Multi-Tenant API Platform

A multi-tenant SaaS backend built with FastAPI, PostgreSQL and SQLAlchemy: organizations, role-based access, usage metering, quotas and rate limiting.



## Quick start

```bash
cp .env.example .env
docker compose up --build        # runs migrations, then the API
```
API docs: http://localhost:8000/docs

Local development without Docker (SQLite):
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
alembic upgrade head
uvicorn app.main:app --reload
pytest -q
ruff check app tests migrations
```

## Project layout

```
app/
  api/routers/     HTTP layer
  services/        business rules
  repositories/    database queries
  models/          SQLAlchemy models
  schemas/         Pydantic request/response models
  core/            settings, logging
  db/              engine, session, Base
migrations/        Alembic revisions
docs/              architecture, data model, weekly notes
tests/             pytest suite
```

## Tech stack
FastAPI, Pydantic v2, SQLAlchemy 2, Alembic, PostgreSQL 16, Docker Compose, GitHub Actions, Ruff, pytest.

## License
MIT — © Dhanush
