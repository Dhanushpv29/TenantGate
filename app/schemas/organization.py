from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    # Temporary in Week 1: becomes the owner. Replaced by the authenticated subject in Week 2.
    owner_subject: str = Field(min_length=1, max_length=160)


class OrganizationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    plan: str
    is_active: bool
    created_at: datetime
