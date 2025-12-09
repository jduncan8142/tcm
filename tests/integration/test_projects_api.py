"""
Integration tests for Project API endpoints.

Tests all CRUD operations and test case management for the /api/projects endpoints.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestProjectsAPI:
    """Test suite for Project API endpoints."""

    async def test_create_project(self, test_client: AsyncClient):
        """Test creating a new project."""
        response = await test_client.post(
            "/api/projects",
            json={
                "name": "Q1 2025 Release",
                "description": "Test cases for Q1 release",
                "status": "active",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Q1 2025 Release"
        assert data["status"] == "active"
        assert "id" in data
        assert "created_at" in data

    async def test_create_project_with_testcases(self, test_client: AsyncClient):
        """Test creating a project with test case associations."""
        # Create test cases first
        tc1_response = await test_client.post(
            "/api/testcases",
            json={
                "title": "Test case 1",
                "steps": "Steps",
                "expected_results": "Results",
            },
        )
        tc2_response = await test_client.post(
            "/api/testcases",
            json={
                "title": "Test case 2",
                "steps": "Steps",
                "expected_results": "Results",
            },
        )
        tc1_id = tc1_response.json()["id"]
        tc2_id = tc2_response.json()["id"]

        # Create project with test cases
        response = await test_client.post(
            "/api/projects",
            json={
                "name": "Project with test cases",
                "status": "active",
                "testcase_ids": [tc1_id, tc2_id],
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Project with test cases"

        # Verify test cases are associated
        tc_response = await test_client.get(f"/api/projects/{data['id']}/testcases")
        assert tc_response.status_code == 200
        testcases = tc_response.json()
        assert len(testcases) == 2

    async def test_create_project_with_invalid_testcases(self, test_client: AsyncClient):
        """Test creating a project with invalid test case IDs returns 400."""
        response = await test_client.post(
            "/api/projects",
            json={
                "name": "Invalid project",
                "testcase_ids": [99999],
            },
        )
        assert response.status_code == 400
        assert "not found" in response.json()["detail"]

    async def test_create_duplicate_project_name(self, test_client: AsyncClient):
        """Test creating a project with duplicate name returns 400."""
        project_data = {
            "name": "Duplicate Project",
            "status": "active",
        }

        # Create first project
        response = await test_client.post("/api/projects", json=project_data)
        assert response.status_code == 201

        # Try to create duplicate
        response = await test_client.post("/api/projects", json=project_data)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    async def test_list_projects_empty(self, test_client: AsyncClient):
        """Test listing projects when database is empty."""
        response = await test_client.get("/api/projects")
        assert response.status_code == 200
        data = response.json()
        assert data["projects"] == []
        assert data["total"] == 0

    async def test_list_projects_with_pagination(self, test_client: AsyncClient):
        """Test listing projects with pagination."""
        # Create multiple projects
        for i in range(5):
            await test_client.post(
                "/api/projects",
                json={
                    "name": f"Project {i}",
                    "status": "active",
                },
            )

        # Test pagination
        response = await test_client.get("/api/projects?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["projects"]) == 2
        assert data["total"] == 5
        assert data["skip"] == 2
        assert data["limit"] == 2

    async def test_list_projects_filter_by_status(self, test_client: AsyncClient):
        """Test filtering projects by status."""
        # Create projects with different statuses
        await test_client.post(
            "/api/projects",
            json={
                "name": "Active project",
                "status": "active",
            },
        )
        await test_client.post(
            "/api/projects",
            json={
                "name": "Planning project",
                "status": "planning",
            },
        )

        # Filter by active status
        response = await test_client.get("/api/projects?status=active")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["projects"][0]["status"] == "active"

    async def test_get_project_by_id(self, test_client: AsyncClient):
        """Test getting a specific project by ID."""
        # Create a project
        create_response = await test_client.post(
            "/api/projects",
            json={
                "name": "Test project",
                "description": "Test description",
                "status": "active",
            },
        )
        project_id = create_response.json()["id"]

        # Get the project
        response = await test_client.get(f"/api/projects/{project_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == project_id
        assert data["name"] == "Test project"

    async def test_get_nonexistent_project(self, test_client: AsyncClient):
        """Test getting a non-existent project returns 404."""
        response = await test_client.get("/api/projects/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    async def test_update_project(self, test_client: AsyncClient):
        """Test updating a project."""
        # Create a project
        create_response = await test_client.post(
            "/api/projects",
            json={
                "name": "Original name",
                "description": "Original description",
                "status": "planning",
            },
        )
        project_id = create_response.json()["id"]

        # Update the project
        response = await test_client.patch(
            f"/api/projects/{project_id}",
            json={
                "name": "Updated name",
                "status": "active",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated name"
        assert data["status"] == "active"
        assert data["description"] == "Original description"  # Unchanged

    async def test_update_project_testcases(self, test_client: AsyncClient):
        """Test updating project test cases."""
        # Create test cases
        tc1_response = await test_client.post(
            "/api/testcases",
            json={"title": "TC1", "steps": "Steps", "expected_results": "Results"},
        )
        tc2_response = await test_client.post(
            "/api/testcases",
            json={"title": "TC2", "steps": "Steps", "expected_results": "Results"},
        )
        tc1_id = tc1_response.json()["id"]
        tc2_id = tc2_response.json()["id"]

        # Create project with tc1
        create_response = await test_client.post(
            "/api/projects",
            json={
                "name": "Test project",
                "testcase_ids": [tc1_id],
            },
        )
        project_id = create_response.json()["id"]

        # Update to tc2
        response = await test_client.patch(
            f"/api/projects/{project_id}",
            json={"testcase_ids": [tc2_id]},
        )
        assert response.status_code == 200

        # Verify test cases updated
        tc_response = await test_client.get(f"/api/projects/{project_id}/testcases")
        testcases = tc_response.json()
        assert len(testcases) == 1
        assert testcases[0]["id"] == tc2_id

    async def test_update_project_duplicate_name(self, test_client: AsyncClient):
        """Test updating a project to a duplicate name returns 400."""
        # Create two projects
        await test_client.post(
            "/api/projects",
            json={"name": "Project 1"},
        )
        create_response = await test_client.post(
            "/api/projects",
            json={"name": "Project 2"},
        )
        project_id = create_response.json()["id"]

        # Try to update to duplicate name
        response = await test_client.patch(
            f"/api/projects/{project_id}",
            json={"name": "Project 1"},
        )
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    async def test_update_nonexistent_project(self, test_client: AsyncClient):
        """Test updating a non-existent project returns 404."""
        response = await test_client.patch(
            "/api/projects/99999",
            json={"name": "New name"},
        )
        assert response.status_code == 404

    async def test_delete_project(self, test_client: AsyncClient):
        """Test deleting a project."""
        # Create a project
        create_response = await test_client.post(
            "/api/projects",
            json={"name": "Test project"},
        )
        project_id = create_response.json()["id"]

        # Delete the project
        response = await test_client.delete(f"/api/projects/{project_id}")
        assert response.status_code == 204

        # Verify deleted
        get_response = await test_client.get(f"/api/projects/{project_id}")
        assert get_response.status_code == 404

    async def test_delete_nonexistent_project(self, test_client: AsyncClient):
        """Test deleting a non-existent project returns 404."""
        response = await test_client.delete("/api/projects/99999")
        assert response.status_code == 404

    async def test_get_project_testcases(self, test_client: AsyncClient):
        """Test getting all test cases in a project."""
        # Create test cases with tags
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

        # Create project with test case
        proj_response = await test_client.post(
            "/api/projects",
            json={
                "name": "Test project",
                "testcase_ids": [tc_id],
            },
        )
        project_id = proj_response.json()["id"]

        # Get project test cases
        response = await test_client.get(f"/api/projects/{project_id}/testcases")
        assert response.status_code == 200
        testcases = response.json()
        assert len(testcases) == 1
        assert testcases[0]["id"] == tc_id
        assert len(testcases[0]["tags"]) == 1

    async def test_add_testcase_to_project(self, test_client: AsyncClient):
        """Test adding a test case to a project."""
        # Create test case and project
        tc_response = await test_client.post(
            "/api/testcases",
            json={
                "title": "Test case",
                "steps": "Steps",
                "expected_results": "Results",
            },
        )
        proj_response = await test_client.post(
            "/api/projects",
            json={"name": "Test project"},
        )
        tc_id = tc_response.json()["id"]
        project_id = proj_response.json()["id"]

        # Add test case to project
        response = await test_client.post(
            f"/api/projects/{project_id}/testcases/{tc_id}"
        )
        assert response.status_code == 200

        # Verify test case added
        tc_list = await test_client.get(f"/api/projects/{project_id}/testcases")
        testcases = tc_list.json()
        assert len(testcases) == 1
        assert testcases[0]["id"] == tc_id

    async def test_add_duplicate_testcase_to_project(self, test_client: AsyncClient):
        """Test adding a duplicate test case returns 400."""
        # Create test case and project with that test case
        tc_response = await test_client.post(
            "/api/testcases",
            json={
                "title": "Test case",
                "steps": "Steps",
                "expected_results": "Results",
            },
        )
        tc_id = tc_response.json()["id"]

        proj_response = await test_client.post(
            "/api/projects",
            json={
                "name": "Test project",
                "testcase_ids": [tc_id],
            },
        )
        project_id = proj_response.json()["id"]

        # Try to add the same test case again
        response = await test_client.post(
            f"/api/projects/{project_id}/testcases/{tc_id}"
        )
        assert response.status_code == 400
        assert "already associated" in response.json()["detail"]

    async def test_remove_testcase_from_project(self, test_client: AsyncClient):
        """Test removing a test case from a project."""
        # Create test case and project with that test case
        tc_response = await test_client.post(
            "/api/testcases",
            json={
                "title": "Test case",
                "steps": "Steps",
                "expected_results": "Results",
            },
        )
        tc_id = tc_response.json()["id"]

        proj_response = await test_client.post(
            "/api/projects",
            json={
                "name": "Test project",
                "testcase_ids": [tc_id],
            },
        )
        project_id = proj_response.json()["id"]

        # Remove test case from project
        response = await test_client.delete(
            f"/api/projects/{project_id}/testcases/{tc_id}"
        )
        assert response.status_code == 200

        # Verify test case removed
        tc_list = await test_client.get(f"/api/projects/{project_id}/testcases")
        testcases = tc_list.json()
        assert len(testcases) == 0

    async def test_remove_nonexistent_testcase_from_project(
        self, test_client: AsyncClient
    ):
        """Test removing a non-existent test case returns 404."""
        # Create project
        proj_response = await test_client.post(
            "/api/projects",
            json={"name": "Test project"},
        )
        project_id = proj_response.json()["id"]

        # Try to remove non-existent test case
        response = await test_client.delete(
            f"/api/projects/{project_id}/testcases/99999"
        )
        assert response.status_code == 404
        assert "not associated" in response.json()["detail"]
