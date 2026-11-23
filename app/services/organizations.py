import re

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Organization
from app.repositories import organizations as repo


class OrganizationConflictError(Exception):
    pass


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug[:80] or "org"


def create_organization(db: Session, name: str, owner_subject: str) -> Organization:
    name = name.strip()
    slug = slugify(name)
    if repo.get_by_name_or_slug(db, name, slug):
        raise OrganizationConflictError("Organization name already in use")
    try:
        org = repo.add_organization(db, name, slug, owner_subject)
        db.commit()
    except IntegrityError as exc:  # concurrent creation race
        db.rollback()
        raise OrganizationConflictError("Organization name already in use") from exc
    db.refresh(org)
    return org
