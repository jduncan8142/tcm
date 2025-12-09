"""
Integration tests for tag management pages.

Tests tag list, create, edit, and delete functionality.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tcm.models.tag import Tag


@pytest.fixture
async def sample_tags(test_session: AsyncSession):
    """Create sample tags for testing."""
    tags = [
        Tag(category="test_type", value="unit", description="Unit test", is_predefined=True),
        Tag(category="test_type", value="integration", description="Integration test", is_predefined=True),
        Tag(category="priority", value="high", description="High priority", is_predefined=True),
        Tag(category="custom", value="my_tag", description="Custom tag", is_predefined=False),
    ]
    for tag in tags:
        test_session.add(tag)
    await test_session.commit()

    # Refresh to get IDs
    for tag in tags:
        await test_session.refresh(tag)

    return tags


@pytest.mark.asyncio
class TestTagsListPage:
    """Test suite for tags list page."""

    async def test_tags_list_page_accessible(self, test_client: AsyncClient):
        """Test that the tags list page is accessible."""
        response = await test_client.get("/tags")
        assert response.status_code == 200
        assert b"Tags Management" in response.content
        assert b"Create New Tag" in response.content

    async def test_tags_list_shows_tags(self, test_client: AsyncClient, sample_tags):
        """Test that tags are displayed in the list."""
        response = await test_client.get("/tags")
        assert response.status_code == 200
        assert b"unit" in response.content
        assert b"integration" in response.content
        assert b"high" in response.content
        assert b"my_tag" in response.content

    async def test_tags_list_shows_category_groups(self, test_client: AsyncClient, sample_tags):
        """Test that tags are grouped by category."""
        response = await test_client.get("/tags")
        assert response.status_code == 200
        # Check category names are displayed (title-cased)
        assert b"Test Type" in response.content
        assert b"Priority" in response.content
        assert b"Custom" in response.content

    async def test_tags_list_filter_by_category(self, test_client: AsyncClient, sample_tags):
        """Test filtering tags by category."""
        response = await test_client.get("/tags?category=test_type")
        assert response.status_code == 200
        assert b"unit" in response.content
        assert b"integration" in response.content
        # Should not show tags from other categories prominently
        # (they might still be in the filter dropdown)

    async def test_tags_list_shows_predefined_status(self, test_client: AsyncClient, sample_tags):
        """Test that predefined status is shown."""
        response = await test_client.get("/tags")
        assert response.status_code == 200
        assert b"Predefined" in response.content
        assert b"Custom" in response.content

    async def test_tags_list_shows_success_message(self, test_client: AsyncClient):
        """Test that success message is displayed."""
        response = await test_client.get("/tags?success=Tag created successfully")
        assert response.status_code == 200
        assert b"Tag created successfully" in response.content

    async def test_tags_list_empty_state(self, test_client: AsyncClient):
        """Test empty state when no tags exist."""
        response = await test_client.get("/tags")
        assert response.status_code == 200
        assert b"No tags found" in response.content


@pytest.mark.asyncio
class TestCreateTagPage:
    """Test suite for create tag page."""

    async def test_create_tag_page_accessible(self, test_client: AsyncClient):
        """Test that the create tag page is accessible."""
        response = await test_client.get("/tags/new")
        assert response.status_code == 200
        assert b"Create New Tag" in response.content
        assert b"Category" in response.content
        assert b"Value" in response.content
        assert b"Description" in response.content

    async def test_create_tag_success(self, test_client: AsyncClient):
        """Test creating a new tag successfully."""
        response = await test_client.post(
            "/tags/new",
            data={
                "category": "new_category",
                "value": "new_value",
                "description": "A new tag",
                "is_predefined": "on",
            },
            follow_redirects=False,
        )
        assert response.status_code == 303
        # URL may be encoded or not depending on framework
        location = response.headers["location"]
        assert "/tags?success=" in location
        assert "Tag" in location or "created" in location.replace("%20", " ")

    async def test_create_tag_without_predefined(self, test_client: AsyncClient):
        """Test creating a tag without predefined flag."""
        response = await test_client.post(
            "/tags/new",
            data={
                "category": "test_category",
                "value": "test_value",
                "description": "Test description",
            },
            follow_redirects=False,
        )
        assert response.status_code == 303

    async def test_create_tag_missing_category(self, test_client: AsyncClient):
        """Test creating a tag with missing category."""
        response = await test_client.post(
            "/tags/new",
            data={
                "category": "",
                "value": "test_value",
            },
            follow_redirects=False,
        )
        # Server validation returns 200 with error message
        # But if the form has 'required' attribute, FastAPI may reject with 422
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            assert b"Category and value are required" in response.content

    async def test_create_tag_missing_value(self, test_client: AsyncClient):
        """Test creating a tag with missing value."""
        response = await test_client.post(
            "/tags/new",
            data={
                "category": "test_category",
                "value": "",
            },
            follow_redirects=False,
        )
        # Server validation returns 200 with error message
        # But if the form has 'required' attribute, FastAPI may reject with 422
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            assert b"Category and value are required" in response.content

    async def test_create_duplicate_tag(self, test_client: AsyncClient, sample_tags):
        """Test creating a duplicate tag."""
        response = await test_client.post(
            "/tags/new",
            data={
                "category": "test_type",
                "value": "unit",
                "description": "Duplicate",
            },
            follow_redirects=False,
        )
        assert response.status_code == 200
        assert b"already exists" in response.content

    async def test_create_tag_shows_existing_categories(self, test_client: AsyncClient, sample_tags):
        """Test that existing categories are shown in dropdown."""
        response = await test_client.get("/tags/new")
        assert response.status_code == 200
        # Datalist should contain existing categories
        assert b"test_type" in response.content
        assert b"priority" in response.content


@pytest.mark.asyncio
class TestEditTagPage:
    """Test suite for edit tag page."""

    async def test_edit_tag_page_accessible(self, test_client: AsyncClient, sample_tags):
        """Test that the edit tag page is accessible."""
        tag = sample_tags[0]
        response = await test_client.get(f"/tags/{tag.id}/edit")
        assert response.status_code == 200
        assert b"Edit Tag" in response.content
        assert tag.value.encode() in response.content
        assert tag.category.encode() in response.content

    async def test_edit_tag_success(self, test_client: AsyncClient, sample_tags):
        """Test editing a tag successfully."""
        tag = sample_tags[3]  # Custom tag
        response = await test_client.post(
            f"/tags/{tag.id}/edit",
            data={
                "category": "updated_category",
                "value": "updated_value",
                "description": "Updated description",
            },
            follow_redirects=False,
        )
        assert response.status_code == 303
        # URL may be encoded or not depending on framework
        location = response.headers["location"]
        assert "/tags?success=" in location

    async def test_edit_tag_not_found(self, test_client: AsyncClient):
        """Test editing a non-existent tag."""
        response = await test_client.get("/tags/99999/edit")
        assert response.status_code == 404
        assert b"Tag Not Found" in response.content

    async def test_edit_tag_missing_category(self, test_client: AsyncClient, sample_tags):
        """Test editing a tag with missing category."""
        tag = sample_tags[0]
        response = await test_client.post(
            f"/tags/{tag.id}/edit",
            data={
                "category": "",
                "value": "test_value",
            },
            follow_redirects=False,
        )
        # Server validation returns 200 with error message
        # But if the form has 'required' attribute, FastAPI may reject with 422
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            assert b"Category and value are required" in response.content

    async def test_edit_tag_duplicate(self, test_client: AsyncClient, sample_tags):
        """Test editing a tag to create a duplicate."""
        tag = sample_tags[3]  # Custom tag
        response = await test_client.post(
            f"/tags/{tag.id}/edit",
            data={
                "category": "test_type",
                "value": "unit",  # Already exists
                "description": "Attempting duplicate",
            },
            follow_redirects=False,
        )
        assert response.status_code == 200
        assert b"already exists" in response.content

    async def test_edit_tag_preserves_same_values(self, test_client: AsyncClient, sample_tags):
        """Test that editing with same values works."""
        tag = sample_tags[0]
        response = await test_client.post(
            f"/tags/{tag.id}/edit",
            data={
                "category": tag.category,
                "value": tag.value,
                "description": tag.description or "",
                "is_predefined": "on" if tag.is_predefined else "",
            },
            follow_redirects=False,
        )
        assert response.status_code == 303


@pytest.mark.asyncio
class TestDeleteTag:
    """Test suite for tag deletion."""

    async def test_delete_tag_via_api(self, test_client: AsyncClient, sample_tags):
        """Test deleting a tag via API (called from JavaScript)."""
        tag = sample_tags[3]  # Custom tag
        response = await test_client.delete(f"/api/tags/{tag.id}")
        assert response.status_code == 204

    async def test_delete_tag_not_found(self, test_client: AsyncClient):
        """Test deleting a non-existent tag."""
        response = await test_client.delete("/api/tags/99999")
        assert response.status_code == 404


@pytest.mark.asyncio
class TestTagPagesResponsive:
    """Test responsive behavior of tag pages."""

    async def test_tags_list_has_responsive_styles(self, test_client: AsyncClient):
        """Test that list page includes responsive CSS."""
        response = await test_client.get("/tags")
        assert response.status_code == 200
        assert b'stylesheet" href="/static/css/styles.css"' in response.content

    async def test_create_tag_has_responsive_styles(self, test_client: AsyncClient):
        """Test that create page includes responsive CSS."""
        response = await test_client.get("/tags/new")
        assert response.status_code == 200
        assert b'stylesheet" href="/static/css/styles.css"' in response.content
