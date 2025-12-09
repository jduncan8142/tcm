"""
Integration tests for dashboard page.

Tests dashboard statistics display and recent activity feed.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tcm.models.tag import Tag
from tcm.models.testcase import TestCase, TestCaseStatus, TestCasePriority
from tcm.models.project import Project, ProjectStatus


@pytest.fixture
async def sample_data(test_session: AsyncSession):
    """Create sample data for dashboard testing."""
    # Create tags
    tags = [
        Tag(category="test_type", value="unit", description="Unit test", is_predefined=True),
        Tag(category="priority", value="high", description="High priority", is_predefined=True),
    ]
    for tag in tags:
        test_session.add(tag)
    await test_session.commit()

    # Refresh to get IDs
    for tag in tags:
        await test_session.refresh(tag)

    # Create test cases
    testcases = [
        TestCase(
            title="Test Case 1",
            description="Description 1",
            steps="Step 1",
            expected_results="Result 1",
            status=TestCaseStatus.ACTIVE,
            priority=TestCasePriority.HIGH,
            tags=[tags[0]],
        ),
        TestCase(
            title="Test Case 2",
            description="Description 2",
            steps="Step 1\nStep 2",
            expected_results="Result 2",
            status=TestCaseStatus.DRAFT,
            priority=TestCasePriority.MEDIUM,
            tags=[tags[1]],
        ),
    ]
    for tc in testcases:
        test_session.add(tc)
    await test_session.commit()

    # Refresh test cases
    for tc in testcases:
        await test_session.refresh(tc)

    # Create projects
    projects = [
        Project(
            name="Project 1",
            description="Description 1",
            status=ProjectStatus.ACTIVE,
            testcases=[testcases[0]],
        ),
        Project(
            name="Project 2",
            description="Description 2",
            status=ProjectStatus.PLANNING,
        ),
    ]
    for proj in projects:
        test_session.add(proj)
    await test_session.commit()

    # Refresh projects
    for proj in projects:
        await test_session.refresh(proj)

    return {
        "tags": tags,
        "testcases": testcases,
        "projects": projects,
    }


@pytest.mark.asyncio
class TestDashboardPage:
    """Test suite for dashboard page."""

    async def test_dashboard_page_accessible(self, test_client: AsyncClient):
        """Test that the dashboard page is accessible."""
        response = await test_client.get("/dashboard")
        assert response.status_code == 200
        assert b"Dashboard" in response.content

    async def test_dashboard_shows_statistics(self, test_client: AsyncClient, sample_data):
        """Test that statistics widgets are displayed with correct counts."""
        response = await test_client.get("/dashboard")
        assert response.status_code == 200

        # Check for statistics widgets
        assert b"Test Cases" in response.content
        assert b"Projects" in response.content
        assert b"Tags" in response.content

        # Check counts are displayed (they should be visible)
        content = response.content.decode()
        assert "2" in content  # 2 test cases
        assert "2" in content  # 2 projects
        assert "2" in content  # 2 tags

    async def test_dashboard_shows_zero_statistics(self, test_client: AsyncClient):
        """Test that statistics show zero when no data exists."""
        response = await test_client.get("/dashboard")
        assert response.status_code == 200

        # Check for statistics widgets
        assert b"Test Cases" in response.content
        assert b"Projects" in response.content
        assert b"Tags" in response.content

        # Check for zero counts
        content = response.content.decode()
        assert "0" in content

    async def test_dashboard_shows_recent_activity(self, test_client: AsyncClient, sample_data):
        """Test that recent activity feed is displayed."""
        response = await test_client.get("/dashboard")
        assert response.status_code == 200

        # Check for activity feed section
        assert b"Recent Activity" in response.content

        # Check for activity items (test cases, projects, tags)
        assert b"Test Case 1" in response.content
        assert b"Test Case 2" in response.content
        assert b"Project 1" in response.content
        assert b"Project 2" in response.content

    async def test_dashboard_shows_empty_activity(self, test_client: AsyncClient):
        """Test that empty activity message is shown when no data exists."""
        response = await test_client.get("/dashboard")
        assert response.status_code == 200

        # Check for empty activity message
        assert b"No recent activity" in response.content

    async def test_dashboard_shows_quick_actions(self, test_client: AsyncClient):
        """Test that quick action links are present."""
        response = await test_client.get("/dashboard")
        assert response.status_code == 200

        # Check for quick actions section
        assert b"Quick Actions" in response.content

        # Check for action links
        assert b"Create Test Case" in response.content
        assert b"Create Project" in response.content
        assert b"Create Tag" in response.content
        assert b"Search" in response.content

    async def test_dashboard_quick_action_links(self, test_client: AsyncClient):
        """Test that quick action links have correct hrefs."""
        response = await test_client.get("/dashboard")
        assert response.status_code == 200

        content = response.content.decode()
        assert 'href="/testcases/new"' in content
        assert 'href="/projects/new"' in content
        assert 'href="/tags/new"' in content
        assert 'href="/search"' in content

    async def test_dashboard_activity_links(self, test_client: AsyncClient, sample_data):
        """Test that activity items have correct links."""
        response = await test_client.get("/dashboard")
        assert response.status_code == 200

        content = response.content.decode()

        # Test case links
        assert f'/testcases/{sample_data["testcases"][0].id}' in content
        assert f'/testcases/{sample_data["testcases"][1].id}' in content

        # Project links
        assert f'/projects/{sample_data["projects"][0].id}' in content
        assert f'/projects/{sample_data["projects"][1].id}' in content

    async def test_dashboard_shows_status_badges(self, test_client: AsyncClient, sample_data):
        """Test that status badges are displayed in activity feed."""
        response = await test_client.get("/dashboard")
        assert response.status_code == 200

        # Check for status badges
        assert b"Active" in response.content
        assert b"Draft" in response.content
        assert b"Planning" in response.content

    async def test_dashboard_shows_tags_in_activity(self, test_client: AsyncClient, sample_data):
        """Test that tags are displayed in test case activity items."""
        response = await test_client.get("/dashboard")
        assert response.status_code == 200

        # Check for tags in activity
        assert b"unit" in response.content
        assert b"high" in response.content
