import pytest
from sqlalchemy import select

from app.models import Membership, Role
from app.services.organizations import slugify


def test_create_tenant_creates_owner_membership(client, db):
    r = client.post("/tenants", json={"name": "Acme Corp", "owner_subject": "alice"})
    assert r.status_code == 201
    body = r.json()
    assert body["slug"] == "acme-corp"
    assert body["plan"] == "free"
    member = db.scalars(select(Membership).where(Membership.tenant_id == body["id"])).one()
    assert member.subject == "alice"
    assert member.role == Role.owner


def test_duplicate_name_rejected(client):
    payload = {"name": "Acme Corp", "owner_subject": "alice"}
    assert client.post("/tenants", json=payload).status_code == 201
    assert client.post("/tenants", json=payload).status_code == 409


def test_slug_collision_rejected(client):
    assert (
        client.post("/tenants", json={"name": "Acme Corp", "owner_subject": "a"}).status_code == 201
    )
    assert (
        client.post("/tenants", json={"name": "acme  corp!", "owner_subject": "b"}).status_code
        == 409
    )


def test_validation_errors(client):
    assert client.post("/tenants", json={"name": "x", "owner_subject": "a"}).status_code == 422
    assert client.post("/tenants", json={"name": "Valid Name"}).status_code == 422


def test_get_tenant_and_404(client):
    created = client.post("/tenants", json={"name": "Globex", "owner_subject": "bob"}).json()
    assert client.get(f"/tenants/{created['id']}").json()["name"] == "Globex"
    assert client.get("/tenants/9999").status_code == 404


@pytest.mark.parametrize(
    "raw,expected", [("Acme Corp", "acme-corp"), ("  --A_B--  ", "a-b"), ("!!!", "org")]
)
def test_slugify(raw, expected):
    assert slugify(raw) == expected
