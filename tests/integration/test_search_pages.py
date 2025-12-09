"""
Integration tests for search page.

Tests global search across test cases, projects, and tags.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tcm.models.tag import Tag
from tcm.models.testcase import TestCase, TestCaseStatus, TestCasePriority
from tcm.models.project import Project, ProjectStatus


@pytest.fixture
async def sample_data(test_session: AsyncSession):
    """Create sample data for search testing."""
    # Create tags
    tags = [
        Tag(category="test_type", value="unit", description="Unit test description", is_predefined=True),
        Tag(category="priority", value="high", description="High priority item", is_predefined=True),
        Tag(category="category", value="search", description="Search feature", is_predefined=False),
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
            title="Search Functionality Test",
            description="Test the search feature",
            steps="1. Open search\n2. Enter query\n3. Verify results",
            expected_results="Results displayed correctly",
            status=TestCaseStatus.ACTIVE,
            priority=TestCasePriority.HIGH,
            tags=[tags[0], tags[2]],
        ),
        TestCase(
            title="Login Test Case",
            description="Test login functionality",
            steps="1. Enter credentials\n2. Click login",
            expected_results="User logged in",
            status=TestCaseStatus.DRAFT,
            priority=TestCasePriority.MEDIUM,
            tags=[tags[1]],
        ),
        TestCase(
            title="Dashboard Display",
            description="Verify dashboard displays correctly",
            steps="1. Navigate to dashboard",
            expected_results="Dashboard shown",
            status=TestCaseStatus.ACTIVE,
            priority=TestCasePriority.LOW,
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
            name="Search Feature Project",
            description="Project for search functionality",
            status=ProjectStatus.ACTIVE,
            testcases=[testcases[0]],
        ),
        Project(
            name="Authentication System",
            description="User authentication project",
            status=ProjectStatus.PLANNING,
            testcases=[testcases[1]],
        ),
        Project(
            name="Dashboard UI",
            description="Dashboard user interface",
            status=ProjectStatus.COMPLETED,
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
class TestSearchPage:
    """Test suite for search page."""

    async def test_search_page_accessible(self, test_client: AsyncClient):
        """Test that the search page is accessible."""
        response = await test_client.get("/search")
        assert response.status_code == 200
        assert b"Search" in response.content

    async def test_search_page_shows_form(self, test_client: AsyncClient):
        """Test that search form is displayed."""
        response = await test_client.get("/search")
        assert response.status_code == 200

        # Check for form elements
        assert b'name="q"' in response.content or b'name="query"' in response.content
        assert b"All Types" in response.content
        assert b"Any Status" in response.content

    async def test_search_empty_query(self, test_client: AsyncClient, sample_data):
        """Test search with empty query shows no results."""
        response = await test_client.get("/search")
        assert response.status_code == 200

        # Should not show results
        assert b"No results found" not in response.content
        # Should show empty search state

    async def test_search_finds_test_cases(self, test_client: AsyncClient, sample_data):
        """Test searching for test cases."""
        response = await test_client.get("/search?q=search")
        assert response.status_code == 200

        # Should find the "Search Functionality Test" test case
        assert b"Search Functionality Test" in response.content
        assert b"Test Cases" in response.content

    async def test_search_finds_projects(self, test_client: AsyncClient, sample_data):
        """Test searching for projects."""
        response = await test_client.get("/search?q=search")
        assert response.status_code == 200

        # Should find the "Search Feature Project" project
        assert b"Search Feature Project" in response.content
        assert b"Projects" in response.content

    async def test_search_finds_tags(self, test_client: AsyncClient, sample_data):
        """Test searching for tags."""
        response = await test_client.get("/search?q=search")
        assert response.status_code == 200

        # Should find the "search" tag
        assert b"search" in response.content
        assert b"Tags" in response.content

    async def test_search_with_entity_type_filter(self, test_client: AsyncClient, sample_data):
        """Test searching with entity type filter."""
        # Search only test cases
        response = await test_client.get("/search?q=test&entity_type=testcase")
        assert response.status_code == 200

        # Should find test cases
        assert b"Login Test Case" in response.content or b"Search Functionality Test" in response.content

        # Should NOT find projects section (or it should be empty)
        # We're filtering to testcases only

    async def test_search_with_status_filter(self, test_client: AsyncClient, sample_data):
        """Test searching with status filter."""
        # Search for active items
        response = await test_client.get("/search?q=test&status=active")
        assert response.status_code == 200

        # Should find active test cases
        assert b"Search Functionality Test" in response.content

    async def test_search_no_results(self, test_client: AsyncClient, sample_data):
        """Test search with no matching results."""
        response = await test_client.get("/search?q=nonexistentquery12345")
        assert response.status_code == 200

        # Should show no results message
        assert b"No results found" in response.content or b"0 result" in response.content

    async def test_search_results_grouped_by_type(self, test_client: AsyncClient, sample_data):
        """Test that results are grouped by entity type."""
        response = await test_client.get("/search?q=dashboard")
        assert response.status_code == 200

        content = response.content.decode()

        # Should have sections for different entity types
        # Check for section headers or grouped results
        if "Dashboard Display" in content:
            assert "Test Cases" in content
        if "Dashboard UI" in content:
            assert "Projects" in content

    async def test_search_shows_result_count(self, test_client: AsyncClient, sample_data):
        """Test that search shows total result count."""
        response = await test_client.get("/search?q=test")
        assert response.status_code == 200

        content = response.content.decode()

        # Should show result count
        assert "result" in content.lower()

    async def test_search_case_insensitive(self, test_client: AsyncClient, sample_data):
        """Test that search is case insensitive."""
        response_lower = await test_client.get("/search?q=search")
        response_upper = await test_client.get("/search?q=SEARCH")

        assert response_lower.status_code == 200
        assert response_upper.status_code == 200

        # Both should find the same items
        assert b"Search Functionality Test" in response_lower.content
        assert b"Search Functionality Test" in response_upper.content

    async def test_search_result_links(self, test_client: AsyncClient, sample_data):
        """Test that search results have correct links."""
        response = await test_client.get("/search?q=search")
        assert response.status_code == 200

        content = response.content.decode()

        # Check for links to entities
        assert f'/testcases/{sample_data["testcases"][0].id}' in content
        assert f'/projects/{sample_data["projects"][0].id}' in content

    async def test_search_shows_metadata(self, test_client: AsyncClient, sample_data):
        """Test that search results show entity metadata."""
        response = await test_client.get("/search?q=search")
        assert response.status_code == 200

        # Should show status badges
        assert b"Active" in response.content

        # Should show tags for test cases
        assert b"unit" in response.content or b"search" in response.content

    async def test_search_description_search(self, test_client: AsyncClient, sample_data):
        """Test searching in descriptions."""
        response = await test_client.get("/search?q=functionality")
        assert response.status_code == 200

        # Should find test case with "functionality" in description
        assert b"Search Functionality Test" in response.content or b"Login Test Case" in response.content

    async def test_search_multiple_entities(self, test_client: AsyncClient, sample_data):
        """Test that search can find multiple types of entities."""
        response = await test_client.get("/search?q=search")
        assert response.status_code == 200

        content = response.content.decode()

        # Should find results across multiple entity types
        found_types = 0
        if "Search Functionality Test" in content:
            found_types += 1
        if "Search Feature Project" in content:
            found_types += 1
        if "category: search" in content or 'value="search"' in content:
            found_types += 1

        # Should find at least 2 different types
        assert found_types >= 2
