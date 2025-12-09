"""
Authentication routes for user login and session management.
"""

import logging
from datetime import datetime, UTC
from typing import Annotated

from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.status import HTTP_302_FOUND, HTTP_303_SEE_OTHER

from tcm.config import settings
from tcm.pages.login import LoginPage

# Configure logger for authentication events
logger = logging.getLogger("tcm.auth")

router = APIRouter(tags=["authentication"])

# Placeholder user database (to be replaced with actual database)
PLACEHOLDER_USERS = {
    "admin": "admin123",  # username: password
    "test": "test123",
}


def log_failed_login(
    username: str, ip_address: str, reason: str, request: Request
):
    """
    Log failed login attempts for security monitoring.

    Args:
        username: Username attempted (sanitized)
        ip_address: IP address of the request
        reason: Reason for failure
        request: The FastAPI request object
    """
    if not settings.log_failed_logins:
        return

    # Sanitize username to prevent log injection
    safe_username = username.replace("\n", "").replace("\r", "")[:100]

    user_agent = request.headers.get("user-agent", "Unknown")

    logger.warning(
        f"Failed login attempt - "
        f"timestamp={datetime.now(UTC).isoformat()} "
        f"username={safe_username} "
        f"ip={ip_address} "
        f"reason={reason} "
        f"user_agent={user_agent}"
    )


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    """
    Render the login page.

    Returns:
        HTML response with login form
    """
    from fasthtml.common import to_xml

    # TODO: Check if user is already authenticated, redirect to dashboard if yes
    return HTMLResponse(content=to_xml(LoginPage()))


@router.post("/api/auth/login")
async def post_login(
    request: Request,
    response: Response,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    """
    Handle login form submission.

    Args:
        request: FastAPI request object
        response: FastAPI response object
        username: Username from form
        password: Password from form

    Returns:
        Redirect to dashboard on success, or login page with error on failure
    """
    # Get client IP address
    client_ip = request.client.host if request.client else "unknown"

    from fasthtml.common import to_xml

    # Validate credentials (placeholder logic)
    if username not in PLACEHOLDER_USERS:
        log_failed_login(username, client_ip, "invalid_username", request)
        return HTMLResponse(
            content=to_xml(LoginPage(error_message="Invalid username or password")),
            status_code=200,
        )

    if PLACEHOLDER_USERS[username] != password:
        log_failed_login(username, client_ip, "invalid_password", request)
        return HTMLResponse(
            content=to_xml(LoginPage(error_message="Invalid username or password")),
            status_code=200,
        )

    # Successful login - set session cookie
    # TODO: Implement proper session management with signed cookies
    logger.info(f"Successful login - username={username} ip={client_ip}")

    # For now, just redirect to dashboard
    # In future, set secure session cookie here
    response = RedirectResponse(url="/dashboard", status_code=HTTP_303_SEE_OTHER)

    # Placeholder session cookie (to be replaced with proper session management)
    response.set_cookie(
        key="session",
        value=f"user_{username}",
        max_age=settings.session_timeout,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
    )

    return response


# Dashboard route is now handled by dashboard_pages.py


@router.get("/api/auth/logout")
async def get_logout(response: Response):
    """
    Handle user logout.

    Returns:
        Redirect to login page and clear session cookie
    """
    response = RedirectResponse(url="/login", status_code=HTTP_303_SEE_OTHER)
    response.delete_cookie(key="session")
    return response
