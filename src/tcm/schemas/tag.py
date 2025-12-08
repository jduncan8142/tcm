"""
Pydantic schemas for Tag API endpoints.

These schemas handle request/response validation and serialization.
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class TagBase(BaseModel):
    """Base schema for Tag with common fields."""

    category: str = Field(..., max_length=50, description="Tag category (e.g., organization, system)")
    value: str = Field(..., max_length=100, description="Tag value")
    description: str | None = Field(None, max_length=500, description="Optional tag description")
    is_predefined: bool = Field(True, description="Whether this is a predefined tag")


class TagCreate(TagBase):
    """Schema for creating a new tag."""

    pass


class TagUpdate(BaseModel):
    """Schema for updating an existing tag."""

    category: str | None = Field(None, max_length=50)
    value: str | None = Field(None, max_length=100)
    description: str | None = Field(None, max_length=500)
    is_predefined: bool | None = None


class TagResponse(TagBase):
    """Schema for tag responses."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TagListResponse(BaseModel):
    """Schema for paginated tag list responses."""

    tags: list[TagResponse]
    total: int
    skip: int
    limit: int
