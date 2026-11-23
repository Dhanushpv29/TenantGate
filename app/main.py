from fastapi import FastAPI

from app.api.routers import health, tenants
from app.core.config import settings
from app.core.logging import configure_logging

configure_logging(settings.log_level)

app = FastAPI(
    title="TenantGate API",
    version="0.1.0",
    description="Multi-tenant SaaS API platform. Schema is managed with Alembic migrations.",
)
app.include_router(health.router)
app.include_router(tenants.router)
