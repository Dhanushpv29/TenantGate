import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models._common import utcnow


class Role(enum.StrEnum):
    owner = "owner"
    admin = "admin"
    developer = "developer"
    viewer = "viewer"


class Membership(Base):
    """Maps an authenticated subject (user id / email) to a role inside one tenant."""

    __tablename__ = "memberships"
    __table_args__ = (
        UniqueConstraint("tenant_id", "subject", name="uq_membership_tenant_subject"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), index=True)
    subject: Mapped[str] = mapped_column(String(160), index=True)
    role: Mapped[Role] = mapped_column(
        Enum(Role, native_enum=False, length=20), default=Role.viewer
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
