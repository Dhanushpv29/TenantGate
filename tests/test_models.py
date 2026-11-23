import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Membership, Organization, Role


def test_membership_unique_per_tenant_subject(db):
    org = Organization(name="Acme", slug="acme")
    db.add(org)
    db.flush()
    db.add(Membership(tenant_id=org.id, subject="alice", role=Role.owner))
    db.commit()
    db.add(Membership(tenant_id=org.id, subject="alice", role=Role.viewer))
    with pytest.raises(IntegrityError):
        db.commit()


def test_same_subject_can_join_different_tenants(db):
    a, b = Organization(name="A Co", slug="a-co"), Organization(name="B Co", slug="b-co")
    db.add_all([a, b])
    db.flush()
    db.add_all(
        [
            Membership(tenant_id=a.id, subject="alice", role=Role.owner),
            Membership(tenant_id=b.id, subject="alice", role=Role.viewer),
        ]
    )
    db.commit()
