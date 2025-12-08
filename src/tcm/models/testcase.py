"""
TestCase model for test case management.

TestCases are the central entity in TCM, representing individual test scenarios.
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import String, Text, DateTime, Enum as SQLEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from tcm.database import Base

if TYPE_CHECKING:
    from tcm.models.tag import Tag
    from tcm.models.project import Project


class TestCaseStatus(str, Enum):
    """Status enum for test cases."""

    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class TestCasePriority(str, Enum):
    """Priority enum for test cases."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TestCase(Base):
    """
    TestCase model representing a single test scenario.

    Test cases are created globally and can be associated with multiple projects
    and tagged with various metadata for organization and filtering.
    """

    __tablename__ = "testcases"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Test case details
    preconditions: Mapped[str | None] = mapped_column(Text, nullable=True)
    steps: Mapped[str] = mapped_column(Text, nullable=False)
    expected_results: Mapped[str] = mapped_column(Text, nullable=False)
    actual_results: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Status and metadata
    status: Mapped[TestCaseStatus] = mapped_column(
        SQLEnum(TestCaseStatus, native_enum=False, length=20),
        default=TestCaseStatus.DRAFT,
        nullable=False,
        index=True,
    )
    priority: Mapped[TestCasePriority] = mapped_column(
        SQLEnum(TestCasePriority, native_enum=False, length=20),
        default=TestCasePriority.MEDIUM,
        nullable=False,
        index=True,
    )

    # Audit fields
    created_by: Mapped[str | None] = mapped_column(String(100), nullable=True)
    updated_by: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    tags: Mapped[list["Tag"]] = relationship(
        secondary="testcase_tags", back_populates="testcases", lazy="selectin"
    )
    projects: Mapped[list["Project"]] = relationship(
        secondary="project_testcases", back_populates="testcases", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<TestCase(id={self.id}, title={self.title}, status={self.status})>"
