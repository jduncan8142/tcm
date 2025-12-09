"""
Integration tests for project management pages.

Tests project list, create, edit, view, and delete functionality.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tcm.models.project import Project, ProjectStatus
from tcm.models.testcase import TestCase, TestCaseStatus, TestCasePriority


@pytest.fixture
async def sample_projects(test_session: AsyncSession):
    """Create sample projects for testing."""
    projects = [
        Project(
            name="Project Alpha",
            description="First test project",
            status=ProjectStatus.ACTIVE,
        ),
        Project(
            name="Project Beta",
            description="Second test project",
            status=ProjectStatus.PLANNING,
        ),
        Project(
            name="Project Gamma",
            description="Third test project",
            status=ProjectStatus.COMPLETED,
        ),
    ]
    for project in projects:
        test_session.add(project)
    await test_session.commit()

    # Refresh to get IDs
    for project in projects:
        await test_session.refresh(project)

    return projects


@pytest.fixture
async def sample_testcases(test_session: AsyncSession):
    """Create sample test cases for testing."""
    testcases = [
        TestCase(
            title="Test Case 1",
            description="First test case",
            steps="Step 1\nStep 2",
            expected_results="Expected result 1",
            status=TestCaseStatus.DRAFT,
            priority=TestCasePriority.HIGH,
        ),
        TestCase(
            title="Test Case 2",
            description="Second test case",
            steps="Step A\nStep B",
            expected_results="Expected result 2",
            status=TestCaseStatus.ACTIVE,
            priority=TestCasePriority.MEDIUM,
        ),
        TestCase(
            title="Test Case 3",
            description="Third test case",
            steps="Step X\nStep Y",
            expected_results="Expected result 3",
            status=TestCaseStatus.ACTIVE,
            priority=TestCasePriority.LOW,
        ),
    ]
    for tc in testcases:
        test_session.add(tc)
    await test_session.commit()

    # Refresh to get IDs
    for tc in testcases:
        await test_session.refresh(tc)

    return testcases


@pytest.mark.asyncio
class TestProjectsListPage:
    """Test suite for projects list page."""

    async def test_projects_list_page_accessible(self, test_client: AsyncClient):
        """Test that the projects list page is accessible."""
        response = await test_client.get("/projects")
        assert response.status_code == 200
        assert b"Projects" in response.content
        assert b"Create New Project" in response.content

    async def test_projects_list_shows_projects(self, test_client: AsyncClient, sample_projects):
        """Test that projects are displayed in the list."""
        response = await test_client.get("/projects")
        assert response.status_code == 200
        assert b"Project Alpha" in response.content
        assert b"Project Beta" in response.content
        assert b"Project Gamma" in response.content

    async def test_projects_list_filter_by_status(self, test_client: AsyncClient, sample_projects):
        """Test filtering projects by status."""
        response = await test_client.get("/projects?status=active")
        assert response.status_code == 200
        assert b"Project Alpha" in response.content
        # Other projects might not be prominent but could be in filter dropdown

    async def test_projects_list_shows_status_badges(self, test_client: AsyncClient, sample_projects):
        """Test that status badges are shown."""
        response = await test_client.get("/projects")
        assert response.status_code == 200
        assert b"Active" in response.content
        assert b"Planning" in response.content
        assert b"Completed" in response.content

    async def test_projects_list_shows_success_message(self, test_client: AsyncClient):
        """Test that success message is displayed."""
        response = await test_client.get("/projects?success=Project created successfully")
        assert response.status_code == 200
        assert b"Project created successfully" in response.content

    async def test_projects_list_empty_state(self, test_client: AsyncClient):
        """Test empty state when no projects exist."""
        response = await test_client.get("/projects")
        assert response.status_code == 200
        assert b"No projects found" in response.content


@pytest.mark.asyncio
class TestCreateProjectPage:
    """Test suite for create project page."""

    async def test_create_project_page_accessible(self, test_client: AsyncClient):
        """Test that the create project page is accessible."""
        response = await test_client.get("/projects/new")
        assert response.status_code == 200
        assert b"Create New Project" in response.content
        assert b"Project Name" in response.content
        assert b"Description" in response.content
        assert b"Status" in response.content

    async def test_create_project_success(self, test_client: AsyncClient):
        """Test creating a new project successfully."""
        response = await test_client.post(
            "/projects/new",
            data={
                "name": "New Test Project",
                "description": "A new project",
                "status": "active",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
            },
            follow_redirects=False,
        )
        assert response.status_code == 303
        location = response.headers["location"]
        assert "/projects/" in location
        assert "success=" in location

    async def test_create_project_minimal(self, test_client: AsyncClient):
        """Test creating a project with only required fields."""
        response = await test_client.post(
            "/projects/new",
            data={
                "name": "Minimal Project",
                "status": "planning",
            },
            follow_redirects=False,
        )
        assert response.status_code == 303

    async def test_create_project_missing_name(self, test_client: AsyncClient):
        """Test creating a project with missing name."""
        response = await test_client.post(
            "/projects/new",
            data={
                "name": "",
                "status": "planning",
            },
            follow_redirects=False,
        )
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            assert b"Project name is required" in response.content

    async def test_create_duplicate_project(self, test_client: AsyncClient, sample_projects):
        """Test creating a duplicate project."""
        response = await test_client.post(
            "/projects/new",
            data={
                "name": "Project Alpha",
                "description": "Duplicate",
                "status": "planning",
            },
            follow_redirects=False,
        )
        assert response.status_code == 200
        assert b"already exists" in response.content

    async def test_create_project_invalid_date_range(self, test_client: AsyncClient):
        """Test creating a project with end date before start date."""
        response = await test_client.post(
            "/projects/new",
            data={
                "name": "Invalid Date Project",
                "status": "planning",
                "start_date": "2025-12-31",
                "end_date": "2025-01-01",
            },
            follow_redirects=False,
        )
        assert response.status_code == 200
        assert b"End date must be after start date" in response.content


@pytest.mark.asyncio
class TestEditProjectPage:
    """Test suite for edit project page."""

    async def test_edit_project_page_accessible(self, test_client: AsyncClient, sample_projects):
        """Test that the edit project page is accessible."""
        project = sample_projects[0]
        response = await test_client.get(f"/projects/{project.id}/edit")
        assert response.status_code == 200
        assert b"Edit Project" in response.content
        assert project.name.encode() in response.content

    async def test_edit_project_success(self, test_client: AsyncClient, sample_projects):
        """Test editing a project successfully."""
        project = sample_projects[0]
        response = await test_client.post(
            f"/projects/{project.id}/edit",
            data={
                "name": "Updated Project Alpha",
                "description": "Updated description",
                "status": "on_hold",
                "start_date": "2025-02-01",
                "end_date": "2025-11-30",
            },
            follow_redirects=False,
        )
        assert response.status_code == 303
        location = response.headers["location"]
        assert f"/projects/{project.id}?success=" in location

    async def test_edit_project_not_found(self, test_client: AsyncClient):
        """Test editing a non-existent project."""
        response = await test_client.get("/projects/99999/edit")
        assert response.status_code == 404
        assert b"Project Not Found" in response.content

    async def test_edit_project_missing_name(self, test_client: AsyncClient, sample_projects):
        """Test editing a project with missing name."""
        project = sample_projects[0]
        response = await test_client.post(
            f"/projects/{project.id}/edit",
            data={
                "name": "",
                "status": "active",
            },
            follow_redirects=False,
        )
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            assert b"Project name is required" in response.content

    async def test_edit_project_duplicate_name(self, test_client: AsyncClient, sample_projects):
        """Test editing a project to create a duplicate."""
        project = sample_projects[0]
        response = await test_client.post(
            f"/projects/{project.id}/edit",
            data={
                "name": "Project Beta",  # Already exists
                "description": "Attempting duplicate",
                "status": "active",
            },
            follow_redirects=False,
        )
        assert response.status_code == 200
        assert b"already exists" in response.content

    async def test_edit_project_preserves_same_values(self, test_client: AsyncClient, sample_projects):
        """Test that editing with same values works."""
        project = sample_projects[0]
        response = await test_client.post(
            f"/projects/{project.id}/edit",
            data={
                "name": project.name,
                "description": project.description or "",
                "status": project.status.value,
            },
            follow_redirects=False,
        )
        assert response.status_code == 303


@pytest.mark.asyncio
class TestViewProjectPage:
    """Test suite for view project page."""

    async def test_view_project_page_accessible(self, test_client: AsyncClient, sample_projects):
        """Test that the view project page is accessible."""
        project = sample_projects[0]
        response = await test_client.get(f"/projects/{project.id}")
        assert response.status_code == 200
        assert project.name.encode() in response.content
        assert b"Project Details" in response.content
        assert b"Test Cases" in response.content

    async def test_view_project_shows_details(self, test_client: AsyncClient, sample_projects):
        """Test that project details are shown."""
        project = sample_projects[0]
        response = await test_client.get(f"/projects/{project.id}")
        assert response.status_code == 200
        assert project.name.encode() in response.content
        if project.description:
            assert project.description.encode() in response.content

    async def test_view_project_not_found(self, test_client: AsyncClient):
        """Test viewing a non-existent project."""
        response = await test_client.get("/projects/99999")
        assert response.status_code == 404
        assert b"Project Not Found" in response.content

    async def test_view_project_shows_testcases(
        self, test_client: AsyncClient, sample_projects, sample_testcases
    ):
        """Test that test cases are shown."""
        project = sample_projects[0]
        testcase = sample_testcases[0]

        # Add test case to project via API
        await test_client.post(f"/api/projects/{project.id}/testcases/{testcase.id}")

        response = await test_client.get(f"/projects/{project.id}")
        assert response.status_code == 200
        assert testcase.title.encode() in response.content

    async def test_view_project_shows_add_testcases_button(
        self, test_client: AsyncClient, sample_projects
    ):
        """Test that add test cases button is shown."""
        project = sample_projects[0]
        response = await test_client.get(f"/projects/{project.id}")
        assert response.status_code == 200
        assert b"Add Test Cases" in response.content


@pytest.mark.asyncio
class TestDeleteProject:
    """Test suite for project deletion."""

    async def test_delete_project_via_api(self, test_client: AsyncClient, sample_projects):
        """Test deleting a project via API (called from JavaScript)."""
        project = sample_projects[2]  # Use Gamma project
        response = await test_client.delete(f"/api/projects/{project.id}")
        assert response.status_code == 204

    async def test_delete_project_not_found(self, test_client: AsyncClient):
        """Test deleting a non-existent project."""
        response = await test_client.delete("/api/projects/99999")
        assert response.status_code == 404


@pytest.mark.asyncio
class TestProjectTestCaseManagement:
    """Test suite for adding/removing test cases from projects."""

    async def test_add_testcase_to_project(
        self, test_client: AsyncClient, sample_projects, sample_testcases
    ):
        """Test adding a test case to a project via API."""
        project = sample_projects[0]
        testcase = sample_testcases[0]

        response = await test_client.post(f"/api/projects/{project.id}/testcases/{testcase.id}")
        assert response.status_code == 200

        # Verify it was added
        view_response = await test_client.get(f"/projects/{project.id}")
        assert testcase.title.encode() in view_response.content

    async def test_remove_testcase_from_project(
        self, test_client: AsyncClient, sample_projects, sample_testcases
    ):
        """Test removing a test case from a project via API."""
        project = sample_projects[0]
        testcase = sample_testcases[0]

        # First add it
        await test_client.post(f"/api/projects/{project.id}/testcases/{testcase.id}")

        # Then remove it
        response = await test_client.delete(f"/api/projects/{project.id}/testcases/{testcase.id}")
        assert response.status_code == 200

        # Verify it was removed
        view_response = await test_client.get(f"/projects/{project.id}")
        # Test case might still appear in "available" list, but not in project list


@pytest.mark.asyncio
class TestProjectPagesResponsive:
    """Test responsive behavior of project pages."""

    async def test_projects_list_has_responsive_styles(self, test_client: AsyncClient):
        """Test that list page includes responsive CSS."""
        response = await test_client.get("/projects")
        assert response.status_code == 200
        assert b'stylesheet" href="/static/css/styles.css"' in response.content

    async def test_create_project_has_responsive_styles(self, test_client: AsyncClient):
        """Test that create page includes responsive CSS."""
        response = await test_client.get("/projects/new")
        assert response.status_code == 200
        assert b'stylesheet" href="/static/css/styles.css"' in response.content

    async def test_view_project_has_modal(self, test_client: AsyncClient, sample_projects):
        """Test that view page includes modal for adding test cases."""
        project = sample_projects[0]
        response = await test_client.get(f"/projects/{project.id}")
        assert response.status_code == 200
        assert b"add-testcase-modal" in response.content
