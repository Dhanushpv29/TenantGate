from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Membership, Organization, Role


def get_by_id(db: Session, tenant_id: int) -> Organization | None:
    return db.get(Organization, tenant_id)


def get_by_name_or_slug(db: Session, name: str, slug: str) -> Organization | None:
    stmt = select(Organization).where((Organization.name == name) | (Organization.slug == slug))
    return db.scalars(stmt).first()


def add_organization(db: Session, name: str, slug: str, owner_subject: str) -> Organization:
    org = Organization(name=name, slug=slug)
    db.add(org)
    db.flush()  # assigns org.id inside the same transaction
    db.add(Membership(tenant_id=org.id, subject=owner_subject, role=Role.owner))
    return org
