"""
Tag models for metadata categorization.

Tags are used to categorize and filter test cases across various dimensions.
"""

from datetime import datetime

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from tcm.database import Base


class Tag(Base):
    """
    Tag model for categorizing test cases.

    Tags represent metadata categories (e.g., organization, system, priority)
    and their specific values (e.g., "Finance", "CRM", "High").
    """

    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    value: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_predefined: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Tag(category={self.category}, value={self.value})>"
