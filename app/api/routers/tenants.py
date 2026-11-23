from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories import organizations as repo
from app.schemas.organization import OrganizationCreate, OrganizationOut
from app.services import organizations as service

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("", response_model=OrganizationOut, status_code=201)
def create_tenant(payload: OrganizationCreate, db: Session = Depends(get_db)):
    try:
        return service.create_organization(db, payload.name, payload.owner_subject)
    except service.OrganizationConflictError as exc:
        raise HTTPException(409, str(exc)) from exc


@router.get("/{tenant_id}", response_model=OrganizationOut)
def get_tenant(tenant_id: int, db: Session = Depends(get_db)):
    org = repo.get_by_id(db, tenant_id)
    if org is None:
        raise HTTPException(404, "Tenant not found")
    return org
