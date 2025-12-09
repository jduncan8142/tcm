"""
Integration tests for test case management pages.

Tests test case list, create, edit, view, and delete functionality.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tcm.models.testcase import TestCase, TestCaseStatus, TestCasePriority
from tcm.models.tag import Tag


@pytest.fixture
async def sample_testcases(test_session: AsyncSession):
    """Create sample test cases for testing."""
    testcases = [
        TestCase(
            title="Test User Login",
            description="Verify user can log in successfully",
            preconditions="User account exists",
            steps="1. Navigate to login page\n2. Enter credentials\n3. Click login",
            expected_results="User is logged in and redirected to dashboard",
            status=TestCaseStatus.ACTIVE,
            priority=TestCasePriority.HIGH,
        ),
        TestCase(
            title="Test Password Reset",
            description="Verify password reset functionality",
            steps="1. Click forgot password\n2. Enter email\n3. Check email for reset link",
            expected_results="User receives password reset email",
            status=TestCaseStatus.DRAFT,
            priority=TestCasePriority.MEDIUM,
        ),
        TestCase(
            title="Test User Registration",
            description="Verify new user registration",
            steps="1. Navigate to registration page\n2. Fill form\n3. Submit",
            expected_results="User account is created",
            status=TestCaseStatus.ACTIVE,
            priority=TestCasePriority.CRITICAL,
        ),
    ]
    for tc in testcases:
        test_session.add(tc)
    await test_session.commit()

    # Refresh to get IDs
    for tc in testcases:
        await test_session.refresh(tc)

    return testcases


@pytest.fixture
async def sample_tags(test_session: AsyncSession):
    """Create sample tags for testing."""
    tags = [
        Tag(category="test_type", value="functional", description="Functional test", is_predefined=True),
        Tag(category="test_type", value="security", description="Security test", is_predefined=True),
        Tag(category="priority", value="smoke", description="Smoke test", is_predefined=True),
    ]
    for tag in tags:
        test_session.add(tag)
    await test_session.commit()

    # Refresh to get IDs
    for tag in tags:
        await test_session.refresh(tag)

    return tags


@pytest.mark.asyncio
class TestTestCasesListPage:
    """Test suite for test cases list page."""

    async def test_testcases_list_page_accessible(self, test_client: AsyncClient):
        """Test that the test cases list page is accessible."""
        response = await test_client.get("/testcases")
        assert response.status_code == 200
        assert b"Test Cases" in response.content
        assert b"Create New Test Case" in response.content

    async def test_testcases_list_shows_testcases(self, test_client: AsyncClient, sample_testcases):
        """Test that test cases are displayed in the list."""
        response = await test_client.get("/testcases")
        assert response.status_code == 200
        assert b"Test User Login" in response.content
        assert b"Test Password Reset" in response.content
        assert b"Test User Registration" in response.content

    async def test_testcases_list_shows_status_and_priority(self, test_client: AsyncClient, sample_testcases):
        """Test that status and priority are displayed."""
        response = await test_client.get("/testcases")
        assert response.status_code == 200
        assert b"Active" in response.content
        assert b"Draft" in response.content
        assert b"High" in response.content
        assert b"Critical" in response.content

    async def test_testcases_list_filter_by_status(self, test_client: AsyncClient, sample_testcases):
        """Test filtering test cases by status."""
        response = await test_client.get("/testcases?status=active")
        assert response.status_code == 200
        assert b"Test User Login" in response.content
        assert b"Test User Registration" in response.content
        # Draft test case should not be prominently shown

    async def test_testcases_list_filter_by_priority(self, test_client: AsyncClient, sample_testcases):
        """Test filtering test cases by priority."""
        response = await test_client.get("/testcases?priority=high")
        assert response.status_code == 200
        assert b"Test User Login" in response.content

    async def test_testcases_list_search(self, test_client: AsyncClient, sample_testcases):
        """Test searching test cases."""
        response = await test_client.get("/testcases?search=login")
        assert response.status_code == 200
        assert b"Test User Login" in response.content

    async def test_testcases_list_pagination(self, test_client: AsyncClient, sample_testcases):
        """Test pagination controls are shown."""
        response = await test_client.get("/testcases?page_size=2")
        assert response.status_code == 200
        # Should show pagination if we have more than 2 items
        assert b"Showing" in response.content

    async def test_testcases_list_shows_success_message(self, test_client: AsyncClient):
        """Test that success message is displayed."""
        response = await test_client.get("/testcases?success=Test case created successfully")
        assert response.status_code == 200
        assert b"Test case created successfully" in response.content

    async def test_testcases_list_empty_state(self, test_client: AsyncClient):
        """Test empty state when no test cases exist."""
        response = await test_client.get("/testcases")
        assert response.status_code == 200
        assert b"No test cases found" in response.content


@pytest.mark.asyncio
class TestCreateTestCasePage:
    """Test suite for create test case page."""

    async def test_create_testcase_page_accessible(self, test_client: AsyncClient):
        """Test that the create test case page is accessible."""
        response = await test_client.get("/testcases/new")
        assert response.status_code == 200
        assert b"Create New Test Case" in response.content
        assert b"Title" in response.content
        assert b"Steps" in response.content
        assert b"Expected Results" in response.content

    async def test_create_testcase_success(self, test_client: AsyncClient, sample_tags):
        """Test creating a new test case successfully."""
        response = await test_client.post(
            "/testcases/new",
            data={
                "title": "New Test Case",
                "description": "Test description",
                "preconditions": "Some preconditions",
                "steps": "1. Step one\n2. Step two",
                "expected_results": "Expected result",
                "status": "draft",
                "priority": "medium",
                "tag_ids": [str(sample_tags[0].id)],
            },
            follow_redirects=False,
        )
        assert response.status_code == 303
        location = response.headers["location"]
        assert "/testcases/" in location
        assert "success=" in location

    async def test_create_testcase_without_tags(self, test_client: AsyncClient):
        """Test creating a test case without tags."""
        response = await test_client.post(
            "/testcases/new",
            data={
                "title": "Test Without Tags",
                "steps": "1. Do something",
                "expected_results": "Something happens",
                "status": "draft",
                "priority": "low",
            },
            follow_redirects=False,
        )
        assert response.status_code == 303

    async def test_create_testcase_missing_title(self, test_client: AsyncClient):
        """Test creating a test case with missing title."""
        response = await test_client.post(
            "/testcases/new",
            data={
                "title": "",
                "steps": "1. Do something",
                "expected_results": "Something happens",
                "status": "draft",
                "priority": "low",
            },
            follow_redirects=False,
        )
        # Server validation returns 200 with error message
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            assert b"required" in response.content.lower()

    async def test_create_testcase_missing_steps(self, test_client: AsyncClient):
        """Test creating a test case with missing steps."""
        response = await test_client.post(
            "/testcases/new",
            data={
                "title": "Test",
                "steps": "",
                "expected_results": "Something happens",
                "status": "draft",
                "priority": "low",
            },
            follow_redirects=False,
        )
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            assert b"required" in response.content.lower()

    async def test_create_testcase_shows_available_tags(self, test_client: AsyncClient, sample_tags):
        """Test that available tags are shown in the form."""
        response = await test_client.get("/testcases/new")
        assert response.status_code == 200
        assert b"functional" in response.content
        assert b"security" in response.content


@pytest.mark.asyncio
class TestEditTestCasePage:
    """Test suite for edit test case page."""

    async def test_edit_testcase_page_accessible(self, test_client: AsyncClient, sample_testcases):
        """Test that the edit test case page is accessible."""
        tc = sample_testcases[0]
        response = await test_client.get(f"/testcases/{tc.id}/edit")
        assert response.status_code == 200
        assert b"Edit Test Case" in response.content
        assert tc.title.encode() in response.content

    async def test_edit_testcase_success(self, test_client: AsyncClient, sample_testcases):
        """Test editing a test case successfully."""
        tc = sample_testcases[0]
        response = await test_client.post(
            f"/testcases/{tc.id}/edit",
            data={
                "title": "Updated Test Title",
                "description": "Updated description",
                "preconditions": "Updated preconditions",
                "steps": "1. Updated step",
                "expected_results": "Updated results",
                "status": "active",
                "priority": "critical",
            },
            follow_redirects=False,
        )
        assert response.status_code == 303
        location = response.headers["location"]
        assert f"/testcases/{tc.id}?success=" in location

    async def test_edit_testcase_not_found(self, test_client: AsyncClient):
        """Test editing a non-existent test case."""
        response = await test_client.get("/testcases/99999/edit")
        assert response.status_code == 404
        assert b"Test Case Not Found" in response.content

    async def test_edit_testcase_missing_title(self, test_client: AsyncClient, sample_testcases):
        """Test editing a test case with missing title."""
        tc = sample_testcases[0]
        response = await test_client.post(
            f"/testcases/{tc.id}/edit",
            data={
                "title": "",
                "steps": "1. Step",
                "expected_results": "Result",
                "status": "draft",
                "priority": "low",
            },
            follow_redirects=False,
        )
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            assert b"required" in response.content.lower()

    async def test_edit_testcase_with_tags(self, test_client: AsyncClient, sample_testcases, sample_tags):
        """Test editing a test case with tag assignment."""
        tc = sample_testcases[0]
        response = await test_client.post(
            f"/testcases/{tc.id}/edit",
            data={
                "title": "Test with Tags",
                "steps": "1. Step",
                "expected_results": "Result",
                "status": "active",
                "priority": "high",
                "tag_ids": [str(sample_tags[0].id), str(sample_tags[1].id)],
            },
            follow_redirects=False,
        )
        assert response.status_code == 303


@pytest.mark.asyncio
class TestViewTestCasePage:
    """Test suite for view test case details page."""

    async def test_view_testcase_page_accessible(self, test_client: AsyncClient, sample_testcases):
        """Test that the view test case page is accessible."""
        tc = sample_testcases[0]
        response = await test_client.get(f"/testcases/{tc.id}")
        assert response.status_code == 200
        assert tc.title.encode() in response.content
        assert b"Edit" in response.content
        assert b"Delete" in response.content

    async def test_view_testcase_shows_all_fields(self, test_client: AsyncClient, sample_testcases):
        """Test that all test case fields are displayed."""
        tc = sample_testcases[0]
        response = await test_client.get(f"/testcases/{tc.id}")
        assert response.status_code == 200
        assert tc.title.encode() in response.content
        assert tc.description.encode() in response.content
        assert tc.steps.encode() in response.content
        assert tc.expected_results.encode() in response.content

    async def test_view_testcase_shows_status_and_priority(self, test_client: AsyncClient, sample_testcases):
        """Test that status and priority are displayed."""
        tc = sample_testcases[0]
        response = await test_client.get(f"/testcases/{tc.id}")
        assert response.status_code == 200
        assert b"Active" in response.content
        assert b"High" in response.content

    async def test_view_testcase_shows_audit_info(self, test_client: AsyncClient, sample_testcases):
        """Test that audit information is displayed."""
        tc = sample_testcases[0]
        response = await test_client.get(f"/testcases/{tc.id}")
        assert response.status_code == 200
        assert b"Created At" in response.content
        assert b"Updated At" in response.content

    async def test_view_testcase_not_found(self, test_client: AsyncClient):
        """Test viewing a non-existent test case."""
        response = await test_client.get("/testcases/99999")
        assert response.status_code == 404
        assert b"Test Case Not Found" in response.content

    async def test_view_testcase_shows_success_message(self, test_client: AsyncClient, sample_testcases):
        """Test that success message is displayed."""
        tc = sample_testcases[0]
        response = await test_client.get(f"/testcases/{tc.id}?success=Test case updated successfully")
        assert response.status_code == 200
        assert b"Test case updated successfully" in response.content


@pytest.mark.asyncio
class TestDeleteTestCase:
    """Test suite for test case deletion."""

    async def test_delete_testcase_via_api(self, test_client: AsyncClient, sample_testcases):
        """Test deleting a test case via API (called from JavaScript)."""
        tc = sample_testcases[0]
        response = await test_client.delete(f"/api/testcases/{tc.id}")
        assert response.status_code == 204

    async def test_delete_testcase_not_found(self, test_client: AsyncClient):
        """Test deleting a non-existent test case."""
        response = await test_client.delete("/api/testcases/99999")
        assert response.status_code == 404


@pytest.mark.asyncio
class TestTestCasePagesResponsive:
    """Test responsive behavior of test case pages."""

    async def test_testcases_list_has_responsive_styles(self, test_client: AsyncClient):
        """Test that list page includes responsive CSS."""
        response = await test_client.get("/testcases")
        assert response.status_code == 200
        assert b'stylesheet" href="/static/css/styles.css"' in response.content

    async def test_create_testcase_has_responsive_styles(self, test_client: AsyncClient):
        """Test that create page includes responsive CSS."""
        response = await test_client.get("/testcases/new")
        assert response.status_code == 200
        assert b'stylesheet" href="/static/css/styles.css"' in response.content

    async def test_view_testcase_has_responsive_styles(self, test_client: AsyncClient, sample_testcases):
        """Test that view page includes responsive CSS."""
        tc = sample_testcases[0]
        response = await test_client.get(f"/testcases/{tc.id}")
        assert response.status_code == 200
        assert b'stylesheet" href="/static/css/styles.css"' in response.content


@pytest.mark.asyncio
class TestTestCasePageIntegration:
    """Test integration between test case pages and API."""

    async def test_create_and_view_testcase(self, test_client: AsyncClient):
        """Test creating a test case and then viewing it."""
        # Create test case
        create_response = await test_client.post(
            "/testcases/new",
            data={
                "title": "Integration Test Case",
                "steps": "1. Integration step",
                "expected_results": "Integration result",
                "status": "active",
                "priority": "medium",
            },
            follow_redirects=False,
        )
        assert create_response.status_code == 303

        # Extract ID from redirect location
        location = create_response.headers["location"]
        testcase_id = location.split("/testcases/")[1].split("?")[0]

        # View the created test case
        view_response = await test_client.get(f"/testcases/{testcase_id}")
        assert view_response.status_code == 200
        assert b"Integration Test Case" in view_response.content

    async def test_create_edit_and_view_testcase(self, test_client: AsyncClient):
        """Test creating, editing, and viewing a test case."""
        # Create test case
        create_response = await test_client.post(
            "/testcases/new",
            data={
                "title": "Original Title",
                "steps": "1. Original step",
                "expected_results": "Original result",
                "status": "draft",
                "priority": "low",
            },
            follow_redirects=False,
        )
        assert create_response.status_code == 303

        # Extract ID from redirect location
        location = create_response.headers["location"]
        testcase_id = location.split("/testcases/")[1].split("?")[0]

        # Edit the test case
        edit_response = await test_client.post(
            f"/testcases/{testcase_id}/edit",
            data={
                "title": "Updated Title",
                "steps": "1. Updated step",
                "expected_results": "Updated result",
                "status": "active",
                "priority": "high",
            },
            follow_redirects=False,
        )
        assert edit_response.status_code == 303

        # View the updated test case
        view_response = await test_client.get(f"/testcases/{testcase_id}")
        assert view_response.status_code == 200
        assert b"Updated Title" in view_response.content
        assert b"Active" in view_response.content
        assert b"High" in view_response.content
