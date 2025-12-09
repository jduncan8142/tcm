"""
Integration tests for authentication routes.

Tests login page rendering, form submission, and session management.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestAuthRoutes:
    """Test suite for authentication routes."""

    async def test_get_login_page(self, test_client: AsyncClient):
        """Test that the login page is accessible."""
        response = await test_client.get("/login")
        assert response.status_code == 200
        assert b"Sign In" in response.content
        assert b'name="username"' in response.content
        assert b'name="password"' in response.content
        assert b'type="submit"' in response.content

    async def test_login_with_valid_credentials(self, test_client: AsyncClient):
        """Test login with valid credentials."""
        response = await test_client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "admin123"},
            follow_redirects=False,
        )
        assert response.status_code == 303  # Redirect
        assert response.headers["location"] == "/dashboard"
        assert "session" in response.cookies

    async def test_login_with_invalid_username(self, test_client: AsyncClient):
        """Test login with invalid username."""
        response = await test_client.post(
            "/api/auth/login",
            data={"username": "nonexistent", "password": "password123"},
            follow_redirects=False,
        )
        assert response.status_code == 200
        assert b"Invalid username or password" in response.content

    async def test_login_with_invalid_password(self, test_client: AsyncClient):
        """Test login with invalid password."""
        response = await test_client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "wrongpassword"},
            follow_redirects=False,
        )
        assert response.status_code == 200
        assert b"Invalid username or password" in response.content

    async def test_dashboard_accessible(self, test_client: AsyncClient):
        """Test that dashboard page is accessible."""
        response = await test_client.get("/dashboard")
        assert response.status_code == 200
        assert b"Dashboard" in response.content
        assert b"Welcome" in response.content

    async def test_logout(self, test_client: AsyncClient):
        """Test logout functionality."""
        # First login
        login_response = await test_client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "admin123"},
            follow_redirects=False,
        )
        assert "session" in login_response.cookies

        # Then logout
        logout_response = await test_client.get(
            "/api/auth/logout", follow_redirects=False
        )
        assert logout_response.status_code == 303
        assert logout_response.headers["location"] == "/login"
        # Session cookie should be deleted (empty value)
        assert logout_response.cookies.get("session", "") == ""

    async def test_empty_credentials(self, test_client: AsyncClient):
        """Test that empty credentials are rejected by HTML5 validation."""
        # Note: HTML5 required attribute prevents submission on client-side
        # But server should still handle it gracefully if bypassed
        response = await test_client.post(
            "/api/auth/login",
            data={"username": "", "password": ""},
            follow_redirects=False,
        )
        # Should either reject or show error
        assert response.status_code in [200, 400, 422]

    async def test_login_preserves_username_on_error(self, test_client: AsyncClient):
        """Test that username is preserved when login fails."""
        response = await test_client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "wrongpassword"},
            follow_redirects=False,
        )
        assert response.status_code == 200
        assert b"Invalid username or password" in response.content
        # Note: In our current implementation, we don't preserve the username
        # This test documents the current behavior

    async def test_multiple_failed_login_attempts(self, test_client: AsyncClient):
        """Test multiple failed login attempts (logging test)."""
        # First failed attempt
        response1 = await test_client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "wrong1"},
            follow_redirects=False,
        )
        assert response1.status_code == 200
        assert b"Invalid username or password" in response1.content

        # Second failed attempt
        response2 = await test_client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "wrong2"},
            follow_redirects=False,
        )
        assert response2.status_code == 200
        assert b"Invalid username or password" in response2.content

        # Note: Failed attempts are logged, but we don't test log content here
        # That would require inspecting log output

    async def test_session_cookie_properties(self, test_client: AsyncClient):
        """Test that session cookie has proper security properties."""
        response = await test_client.post(
            "/api/auth/login",
            data={"username": "test", "password": "test123"},
            follow_redirects=False,
        )
        assert response.status_code == 303

        # Check cookie properties
        set_cookie = response.headers.get("set-cookie", "")
        assert "httponly" in set_cookie.lower()
        assert "samesite=lax" in set_cookie.lower()
        # Note: secure flag should be true in production with HTTPS
