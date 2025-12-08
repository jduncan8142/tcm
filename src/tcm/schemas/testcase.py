"""
Pydantic schemas for TestCase API endpoints.

These schemas handle request/response validation and serialization.
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from tcm.models.testcase import TestCaseStatus, TestCasePriority
from tcm.schemas.tag import TagResponse


class TestCaseBase(BaseModel):
    """Base schema for TestCase with common fields."""

    title: str = Field(..., max_length=200, description="Test case title")
    description: str | None = Field(None, description="Detailed description")
    preconditions: str | None = Field(None, description="Preconditions for the test")
    steps: str = Field(..., description="Test steps to execute")
    expected_results: str = Field(..., description="Expected results")
    actual_results: str | None = Field(None, description="Actual results after execution")
    status: TestCaseStatus = Field(TestCaseStatus.DRAFT, description="Test case status")
    priority: TestCasePriority = Field(TestCasePriority.MEDIUM, description="Test case priority")
    created_by: str | None = Field(None, max_length=100, description="Created by user")
    updated_by: str | None = Field(None, max_length=100, description="Updated by user")


class TestCaseCreate(TestCaseBase):
    """Schema for creating a new test case."""

    tag_ids: list[int] = Field(default_factory=list, description="List of tag IDs to associate")


class TestCaseUpdate(BaseModel):
    """Schema for updating an existing test case."""

    title: str | None = Field(None, max_length=200)
    description: str | None = None
    preconditions: str | None = None
    steps: str | None = None
    expected_results: str | None = None
    actual_results: str | None = None
    status: TestCaseStatus | None = None
    priority: TestCasePriority | None = None
    updated_by: str | None = Field(None, max_length=100)
    tag_ids: list[int] | None = Field(None, description="List of tag IDs to associate")


class TestCaseResponse(TestCaseBase):
    """Schema for test case responses."""

    id: int
    created_at: datetime
    updated_at: datetime
    tags: list[TagResponse] = []

    model_config = ConfigDict(from_attributes=True)


class TestCaseListResponse(BaseModel):
    """Schema for paginated test case list responses."""

    testcases: list[TestCaseResponse]
    total: int
    skip: int
    limit: int
