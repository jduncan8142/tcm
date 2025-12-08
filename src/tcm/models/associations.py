"""
Association tables for many-to-many relationships.

These tables link TestCases with Tags and Projects.
"""

from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime, func

from tcm.database import Base

# Association table for TestCase <-> Tag (many-to-many)
testcase_tags = Table(
    "testcase_tags",
    Base.metadata,
    Column("testcase_id", Integer, ForeignKey("testcases.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
)

# Association table for Project <-> TestCase (many-to-many)
project_testcases = Table(
    "project_testcases",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True),
    Column("testcase_id", Integer, ForeignKey("testcases.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
)
