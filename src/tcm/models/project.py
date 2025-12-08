"""
Project model for organizing test case execution efforts.

Projects are organizational units that group test cases for execution tracking.
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import String, Text, DateTime, Enum as SQLEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from tcm.database import Base

if TYPE_CHECKING:
    from tcm.models.testcase import TestCase


class ProjectStatus(str, Enum):
    """Status enum for projects."""

    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Project(Base):
    """
    Project model representing an organizational unit for test execution.

    Projects group test cases together for execution tracking and reporting.
    Test cases can be associated with multiple projects.
    """

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Project metadata
    status: Mapped[ProjectStatus] = mapped_column(
        SQLEnum(ProjectStatus, native_enum=False, length=20),
        default=ProjectStatus.PLANNING,
        nullable=False,
        index=True,
    )

    # Project timeline
    start_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

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
    testcases: Mapped[list["TestCase"]] = relationship(
        secondary="project_testcases", back_populates="projects", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name={self.name}, status={self.status})>"
