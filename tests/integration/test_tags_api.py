"""
Integration tests for Tag API endpoints.

Tests all CRUD operations and edge cases for the /api/tags endpoints.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestTagsAPI:
    """Test suite for Tag API endpoints."""

    async def test_create_tag(self, test_client: AsyncClient):
        """Test creating a new tag."""
        response = await test_client.post(
            "/api/tags",
            json={
                "category": "test_category",
                "value": "test_value",
                "description": "Test description",
                "is_predefined": False,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["category"] == "test_category"
        assert data["value"] == "test_value"
        assert data["description"] == "Test description"
        assert data["is_predefined"] is False
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_create_duplicate_tag(self, test_client: AsyncClient):
        """Test creating a duplicate tag returns 400."""
        tag_data = {
            "category": "test_category",
            "value": "test_value",
            "description": "Test description",
        }

        # Create first tag
        response = await test_client.post("/api/tags", json=tag_data)
        assert response.status_code == 201

        # Try to create duplicate
        response = await test_client.post("/api/tags", json=tag_data)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    async def test_list_tags_empty(self, test_client: AsyncClient):
        """Test listing tags when database is empty."""
        response = await test_client.get("/api/tags")
        assert response.status_code == 200
        data = response.json()
        assert data["tags"] == []
        assert data["total"] == 0
        assert data["skip"] == 0
        assert data["limit"] == 100

    async def test_list_tags_with_pagination(self, test_client: AsyncClient):
        """Test listing tags with pagination."""
        # Create multiple tags
        for i in range(5):
            await test_client.post(
                "/api/tags",
                json={
                    "category": "test_category",
                    "value": f"test_value_{i}",
                    "description": f"Test description {i}",
                },
            )

        # Test pagination
        response = await test_client.get("/api/tags?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["tags"]) == 2
        assert data["total"] == 5
        assert data["skip"] == 2
        assert data["limit"] == 2

    async def test_list_tags_with_category_filter(self, test_client: AsyncClient):
        """Test listing tags with category filter."""
        # Create tags in different categories
        await test_client.post(
            "/api/tags",
            json={"category": "category1", "value": "value1"},
        )
        await test_client.post(
            "/api/tags",
            json={"category": "category2", "value": "value2"},
        )
        await test_client.post(
            "/api/tags",
            json={"category": "category1", "value": "value3"},
        )

        # Filter by category1
        response = await test_client.get("/api/tags?category=category1")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert all(tag["category"] == "category1" for tag in data["tags"])

    async def test_get_tag_by_id(self, test_client: AsyncClient):
        """Test getting a specific tag by ID."""
        # Create a tag
        create_response = await test_client.post(
            "/api/tags",
            json={
                "category": "test_category",
                "value": "test_value",
                "description": "Test description",
            },
        )
        tag_id = create_response.json()["id"]

        # Get the tag
        response = await test_client.get(f"/api/tags/{tag_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == tag_id
        assert data["category"] == "test_category"
        assert data["value"] == "test_value"

    async def test_get_nonexistent_tag(self, test_client: AsyncClient):
        """Test getting a non-existent tag returns 404."""
        response = await test_client.get("/api/tags/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    async def test_list_tag_categories(self, test_client: AsyncClient):
        """Test getting unique tag categories."""
        # Create tags in different categories
        await test_client.post(
            "/api/tags",
            json={"category": "category1", "value": "value1"},
        )
        await test_client.post(
            "/api/tags",
            json={"category": "category2", "value": "value2"},
        )
        await test_client.post(
            "/api/tags",
            json={"category": "category1", "value": "value3"},
        )

        # Get categories
        response = await test_client.get("/api/tags/categories")
        assert response.status_code == 200
        categories = response.json()
        assert len(categories) == 2
        assert "category1" in categories
        assert "category2" in categories

    async def test_update_tag(self, test_client: AsyncClient):
        """Test updating a tag."""
        # Create a tag
        create_response = await test_client.post(
            "/api/tags",
            json={
                "category": "test_category",
                "value": "test_value",
                "description": "Original description",
            },
        )
        tag_id = create_response.json()["id"]

        # Update the tag
        response = await test_client.patch(
            f"/api/tags/{tag_id}",
            json={
                "value": "updated_value",
                "description": "Updated description",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == tag_id
        assert data["category"] == "test_category"  # Unchanged
        assert data["value"] == "updated_value"
        assert data["description"] == "Updated description"

    async def test_update_nonexistent_tag(self, test_client: AsyncClient):
        """Test updating a non-existent tag returns 404."""
        response = await test_client.patch(
            "/api/tags/99999",
            json={"value": "new_value"},
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    async def test_update_tag_creates_duplicate(self, test_client: AsyncClient):
        """Test updating a tag to create a duplicate returns 400."""
        # Create two tags
        await test_client.post(
            "/api/tags",
            json={"category": "category1", "value": "value1"},
        )
        create_response = await test_client.post(
            "/api/tags",
            json={"category": "category1", "value": "value2"},
        )
        tag_id = create_response.json()["id"]

        # Try to update second tag to match first
        response = await test_client.patch(
            f"/api/tags/{tag_id}",
            json={"value": "value1"},
        )
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    async def test_delete_tag(self, test_client: AsyncClient):
        """Test deleting a tag."""
        # Create a tag
        create_response = await test_client.post(
            "/api/tags",
            json={"category": "test_category", "value": "test_value"},
        )
        tag_id = create_response.json()["id"]

        # Delete the tag
        response = await test_client.delete(f"/api/tags/{tag_id}")
        assert response.status_code == 204

        # Verify tag is deleted
        get_response = await test_client.get(f"/api/tags/{tag_id}")
        assert get_response.status_code == 404

    async def test_delete_nonexistent_tag(self, test_client: AsyncClient):
        """Test deleting a non-existent tag returns 404."""
        response = await test_client.delete("/api/tags/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
