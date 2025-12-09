"""
Integration tests for TestCase API endpoints.

Tests all CRUD operations and tag management for the /api/testcases endpoints.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestTestCasesAPI:
    """Test suite for TestCase API endpoints."""

    async def test_create_testcase(self, test_client: AsyncClient):
        """Test creating a new test case."""
        response = await test_client.post(
            "/api/testcases",
            json={
                "title": "Test user login",
                "description": "Verify user can login with valid credentials",
                "preconditions": "User account exists",
                "steps": "1. Navigate to login\n2. Enter credentials\n3. Click login",
                "expected_results": "User is logged in",
                "status": "active",
                "priority": "high",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test user login"
        assert data["status"] == "active"
        assert data["priority"] == "high"
        assert "id" in data
        assert "created_at" in data

    async def test_create_testcase_with_tags(self, test_client: AsyncClient):
        """Test creating a test case with tag associations."""
        # Create tags first
        tag1_response = await test_client.post(
            "/api/tags",
            json={"category": "test_type", "value": "functional"},
        )
        tag2_response = await test_client.post(
            "/api/tags",
            json={"category": "priority", "value": "high"},
        )
        tag1_id = tag1_response.json()["id"]
        tag2_id = tag2_response.json()["id"]

        # Create test case with tags
        response = await test_client.post(
            "/api/testcases",
            json={
                "title": "Test with tags",
                "steps": "Test steps",
                "expected_results": "Expected results",
                "tag_ids": [tag1_id, tag2_id],
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert len(data["tags"]) == 2
        tag_ids = [tag["id"] for tag in data["tags"]]
        assert tag1_id in tag_ids
        assert tag2_id in tag_ids

    async def test_create_testcase_with_invalid_tags(self, test_client: AsyncClient):
        """Test creating a test case with invalid tag IDs returns 400."""
        response = await test_client.post(
            "/api/testcases",
            json={
                "title": "Test with invalid tags",
                "steps": "Test steps",
                "expected_results": "Expected results",
                "tag_ids": [99999],
            },
        )
        assert response.status_code == 400
        assert "not found" in response.json()["detail"]

    async def test_list_testcases_empty(self, test_client: AsyncClient):
        """Test listing test cases when database is empty."""
        response = await test_client.get("/api/testcases")
        assert response.status_code == 200
        data = response.json()
        assert data["testcases"] == []
        assert data["total"] == 0

    async def test_list_testcases_with_pagination(self, test_client: AsyncClient):
        """Test listing test cases with pagination."""
        # Create multiple test cases
        for i in range(5):
            await test_client.post(
                "/api/testcases",
                json={
                    "title": f"Test case {i}",
                    "steps": f"Steps {i}",
                    "expected_results": f"Results {i}",
                },
            )

        # Test pagination
        response = await test_client.get("/api/testcases?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["testcases"]) == 2
        assert data["total"] == 5
        assert data["skip"] == 2
        assert data["limit"] == 2

    async def test_list_testcases_filter_by_status(self, test_client: AsyncClient):
        """Test filtering test cases by status."""
        # Create test cases with different statuses
        await test_client.post(
            "/api/testcases",
            json={
                "title": "Active test",
                "steps": "Steps",
                "expected_results": "Results",
                "status": "active",
            },
        )
        await test_client.post(
            "/api/testcases",
            json={
                "title": "Draft test",
                "steps": "Steps",
                "expected_results": "Results",
                "status": "draft",
            },
        )

        # Filter by active status
        response = await test_client.get("/api/testcases?status=active")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["testcases"][0]["status"] == "active"

    async def test_list_testcases_filter_by_priority(self, test_client: AsyncClient):
        """Test filtering test cases by priority."""
        # Create test cases with different priorities
        await test_client.post(
            "/api/testcases",
            json={
                "title": "High priority",
                "steps": "Steps",
                "expected_results": "Results",
                "priority": "high",
            },
        )
        await test_client.post(
            "/api/testcases",
            json={
                "title": "Low priority",
                "steps": "Steps",
                "expected_results": "Results",
                "priority": "low",
            },
        )

        # Filter by high priority
        response = await test_client.get("/api/testcases?priority=high")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["testcases"][0]["priority"] == "high"

    async def test_list_testcases_filter_by_tag(self, test_client: AsyncClient):
        """Test filtering test cases by tag."""
        # Create a tag
        tag_response = await test_client.post(
            "/api/tags",
            json={"category": "test_type", "value": "functional"},
        )
        tag_id = tag_response.json()["id"]

        # Create test cases, one with tag and one without
        await test_client.post(
            "/api/testcases",
            json={
                "title": "Test with tag",
                "steps": "Steps",
                "expected_results": "Results",
                "tag_ids": [tag_id],
            },
        )
        await test_client.post(
            "/api/testcases",
            json={
                "title": "Test without tag",
                "steps": "Steps",
                "expected_results": "Results",
            },
        )

        # Filter by tag
        response = await test_client.get(f"/api/testcases?tag_id={tag_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["testcases"][0]["title"] == "Test with tag"

    async def test_get_testcase_by_id(self, test_client: AsyncClient):
        """Test getting a specific test case by ID."""
        # Create a test case
        create_response = await test_client.post(
            "/api/testcases",
            json={
                "title": "Test case",
                "steps": "Test steps",
                "expected_results": "Expected results",
            },
        )
        tc_id = create_response.json()["id"]

        # Get the test case
        response = await test_client.get(f"/api/testcases/{tc_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == tc_id
        assert data["title"] == "Test case"

    async def test_get_nonexistent_testcase(self, test_client: AsyncClient):
        """Test getting a non-existent test case returns 404."""
        response = await test_client.get("/api/testcases/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    async def test_update_testcase(self, test_client: AsyncClient):
        """Test updating a test case."""
        # Create a test case
        create_response = await test_client.post(
            "/api/testcases",
            json={
                "title": "Original title",
                "steps": "Original steps",
                "expected_results": "Original results",
                "status": "draft",
            },
        )
        tc_id = create_response.json()["id"]

        # Update the test case
        response = await test_client.patch(
            f"/api/testcases/{tc_id}",
            json={
                "title": "Updated title",
                "status": "active",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated title"
        assert data["status"] == "active"
        assert data["steps"] == "Original steps"  # Unchanged

    async def test_update_testcase_tags(self, test_client: AsyncClient):
        """Test updating test case tags."""
        # Create tags
        tag1_response = await test_client.post(
            "/api/tags",
            json={"category": "test_type", "value": "functional"},
        )
        tag2_response = await test_client.post(
            "/api/tags",
            json={"category": "test_type", "value": "integration"},
        )
        tag1_id = tag1_response.json()["id"]
        tag2_id = tag2_response.json()["id"]

        # Create test case with tag1
        create_response = await test_client.post(
            "/api/testcases",
            json={
                "title": "Test case",
                "steps": "Steps",
                "expected_results": "Results",
                "tag_ids": [tag1_id],
            },
        )
        tc_id = create_response.json()["id"]

        # Update tags to tag2
        response = await test_client.patch(
            f"/api/testcases/{tc_id}",
            json={"tag_ids": [tag2_id]},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["tags"]) == 1
        assert data["tags"][0]["id"] == tag2_id

    async def test_update_nonexistent_testcase(self, test_client: AsyncClient):
        """Test updating a non-existent test case returns 404."""
        response = await test_client.patch(
            "/api/testcases/99999",
            json={"title": "New title"},
        )
        assert response.status_code == 404

    async def test_delete_testcase(self, test_client: AsyncClient):
        """Test deleting a test case."""
        # Create a test case
        create_response = await test_client.post(
            "/api/testcases",
            json={
                "title": "Test case",
                "steps": "Steps",
                "expected_results": "Results",
            },
        )
        tc_id = create_response.json()["id"]

        # Delete the test case
        response = await test_client.delete(f"/api/testcases/{tc_id}")
        assert response.status_code == 204

        # Verify deleted
        get_response = await test_client.get(f"/api/testcases/{tc_id}")
        assert get_response.status_code == 404

    async def test_delete_nonexistent_testcase(self, test_client: AsyncClient):
        """Test deleting a non-existent test case returns 404."""
        response = await test_client.delete("/api/testcases/99999")
        assert response.status_code == 404

    async def test_add_tag_to_testcase(self, test_client: AsyncClient):
        """Test adding a tag to a test case."""
        # Create tag and test case
        tag_response = await test_client.post(
            "/api/tags",
            json={"category": "test_type", "value": "functional"},
        )
        tc_response = await test_client.post(
            "/api/testcases",
            json={
                "title": "Test case",
                "steps": "Steps",
                "expected_results": "Results",
            },
        )
        tag_id = tag_response.json()["id"]
        tc_id = tc_response.json()["id"]

        # Add tag to test case
        response = await test_client.post(f"/api/testcases/{tc_id}/tags/{tag_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["tags"]) == 1
        assert data["tags"][0]["id"] == tag_id

    async def test_add_duplicate_tag_to_testcase(self, test_client: AsyncClient):
        """Test adding a duplicate tag returns 400."""
        # Create tag and test case with that tag
        tag_response = await test_client.post(
            "/api/tags",
            json={"category": "test_type", "value": "functional"},
        )
        tag_id = tag_response.json()["id"]

        tc_response = await test_client.post(
            "/api/testcases",
            json={
                "title": "Test case",
                "steps": "Steps",
                "expected_results": "Results",
                "tag_ids": [tag_id],
            },
        )
        tc_id = tc_response.json()["id"]

        # Try to add the same tag again
        response = await test_client.post(f"/api/testcases/{tc_id}/tags/{tag_id}")
        assert response.status_code == 400
        assert "already associated" in response.json()["detail"]

    async def test_remove_tag_from_testcase(self, test_client: AsyncClient):
        """Test removing a tag from a test case."""
        # Create tag and test case with that tag
        tag_response = await test_client.post(
            "/api/tags",
            json={"category": "test_type", "value": "functional"},
        )
        tag_id = tag_response.json()["id"]

        tc_response = await test_client.post(
            "/api/testcases",
            json={
                "title": "Test case",
                "steps": "Steps",
                "expected_results": "Results",
                "tag_ids": [tag_id],
            },
        )
        tc_id = tc_response.json()["id"]

        # Remove tag from test case
        response = await test_client.delete(f"/api/testcases/{tc_id}/tags/{tag_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["tags"]) == 0

    async def test_remove_nonexistent_tag_from_testcase(self, test_client: AsyncClient):
        """Test removing a non-existent tag returns 404."""
        # Create test case
        tc_response = await test_client.post(
            "/api/testcases",
            json={
                "title": "Test case",
                "steps": "Steps",
                "expected_results": "Results",
            },
        )
        tc_id = tc_response.json()["id"]

        # Try to remove non-existent tag
        response = await test_client.delete(f"/api/testcases/{tc_id}/tags/99999")
        assert response.status_code == 404
        assert "not associated" in response.json()["detail"]
