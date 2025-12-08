"""
Pydantic schemas for Project API endpoints.

These schemas handle request/response validation and serialization.
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from tcm.models.project import ProjectStatus


class ProjectBase(BaseModel):
    """Base schema for Project with common fields."""

    name: str = Field(..., max_length=200, description="Project name (must be unique)")
    description: str | None = Field(None, description="Project description")
    status: ProjectStatus = Field(ProjectStatus.PLANNING, description="Project status")
    start_date: datetime | None = Field(None, description="Project start date")
    end_date: datetime | None = Field(None, description="Project end date")
    created_by: str | None = Field(None, max_length=100, description="Created by user")
    updated_by: str | None = Field(None, max_length=100, description="Updated by user")


class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""

    testcase_ids: list[int] = Field(default_factory=list, description="List of test case IDs to associate")


class ProjectUpdate(BaseModel):
    """Schema for updating an existing project."""

    name: str | None = Field(None, max_length=200)
    description: str | None = None
    status: ProjectStatus | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    updated_by: str | None = Field(None, max_length=100)
    testcase_ids: list[int] | None = Field(None, description="List of test case IDs to associate")


class ProjectResponse(ProjectBase):
    """Schema for project responses."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectListResponse(BaseModel):
    """Schema for paginated project list responses."""

    projects: list[ProjectResponse]
    total: int
    skip: int
    limit: int
