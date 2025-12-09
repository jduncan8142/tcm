"""
Pytest configuration and shared fixtures for testing.

This module provides test fixtures for database sessions, test clients,
and common test data.
"""

import asyncio
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from tcm.database import Base, get_db
from tcm.main import app

# Import all models to ensure they're registered with Base.metadata
from tcm.models.tag import Tag
from tcm.models.testcase import TestCase
from tcm.models.project import Project
from tcm.models.associations import testcase_tags, project_testcases

# Test database URL (file-based SQLite for testing)
import tempfile
import os

# Create a temporary file for the test database
_temp_db_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
_temp_db_file.close()
TEST_DATABASE_PATH = _temp_db_file.name
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{TEST_DATABASE_PATH}"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_engine():
    """Create a test database engine."""
    # Remove database file if it exists
    if os.path.exists(TEST_DATABASE_PATH):
        os.remove(TEST_DATABASE_PATH)

    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=NullPool,
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Drop all tables and dispose engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()

    # Clean up database file
    if os.path.exists(TEST_DATABASE_PATH):
        os.remove(TEST_DATABASE_PATH)


@pytest.fixture(scope="function")
async def test_session_maker(test_engine):
    """Create a test session maker."""
    return async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


@pytest.fixture(scope="function")
async def test_session(test_session_maker) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async with test_session_maker() as session:
        yield session


@pytest.fixture(scope="function")
async def test_client(test_engine, test_session_maker) -> AsyncGenerator[AsyncClient, None]:
    """
    Create a test client with dependency overrides.

    This fixture overrides the database session dependency to use the test database.
    """

    async def override_get_db():
        async with test_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()
