"""
Integration tests for page layout components.

Tests the shared PageLayout component including header, footer, and navigation.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestPageLayout:
    """Test suite for page layout components."""

    async def test_header_title_is_clickable_on_dashboard(self, test_client: AsyncClient):
        """Test that header title is a clickable link on the dashboard page."""
        response = await test_client.get("/dashboard")
        assert response.status_code == 200

        content = response.content.decode()

        # Check that the header contains a link to /dashboard
        assert 'href="/dashboard"' in content

        # Check that the link contains "Test Case Management" text
        assert "Test Case Management" in content

        # Check that the link has the header-title-link class
        assert 'class="header-title-link"' in content

    async def test_header_title_is_clickable_on_testcases_page(self, test_client: AsyncClient):
        """Test that header title is a clickable link on the testcases page."""
        response = await test_client.get("/testcases")
        assert response.status_code == 200

        content = response.content.decode()

        # Check that the header contains a link to /dashboard
        assert 'href="/dashboard"' in content
        assert "Test Case Management" in content

    async def test_header_title_is_clickable_on_projects_page(self, test_client: AsyncClient):
        """Test that header title is a clickable link on the projects page."""
        response = await test_client.get("/projects")
        assert response.status_code == 200

        content = response.content.decode()

        # Check that the header contains a link to /dashboard
        assert 'href="/dashboard"' in content
        assert "Test Case Management" in content

    async def test_header_title_is_clickable_on_tags_page(self, test_client: AsyncClient):
        """Test that header title is a clickable link on the tags page."""
        response = await test_client.get("/tags")
        assert response.status_code == 200

        content = response.content.decode()

        # Check that the header contains a link to /dashboard
        assert 'href="/dashboard"' in content
        assert "Test Case Management" in content

    async def test_header_title_link_structure(self, test_client: AsyncClient):
        """Test that header title link has correct HTML structure."""
        response = await test_client.get("/dashboard")
        assert response.status_code == 200

        content = response.content.decode()

        # Verify the link is inside an H1 element
        assert "<h1>" in content.lower()
        assert "</h1>" in content.lower()

        # Verify the link structure: H1 contains A tag
        # The structure should be: <h1><a href="/dashboard" class="header-title-link">Test Case Management</a></h1>
        assert 'href="/dashboard"' in content
        assert 'class="header-title-link"' in content

    async def test_footer_displays_copyright(self, test_client: AsyncClient):
        """Test that footer displays copyright information."""
        response = await test_client.get("/dashboard")
        assert response.status_code == 200

        content = response.content.decode()

        # Check for copyright text
        assert "©" in content or "&copy;" in content.lower()
        assert "2025" in content
        assert "Test Case Management" in content
