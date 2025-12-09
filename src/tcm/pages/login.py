"""
Login page for user authentication.
"""

from fasthtml.common import *
from tcm.pages.components import PageLayout, InputField, SubmitButton, ErrorMessage


def LoginPage(error_message: str = ""):
    """
    Render the login page with form.

    Args:
        error_message: Error message to display (if any)

    Returns:
        FastHTML page with login form
    """
    return PageLayout(
        Div(
            Div(
                H2("Sign In", cls="form-title"),
                ErrorMessage(error_message),
                Form(
                    InputField(
                        name="username",
                        label="Username",
                        input_type="text",
                        required=True,
                        placeholder="Enter your username",
                        autocomplete="username",
                    ),
                    InputField(
                        name="password",
                        label="Password",
                        input_type="password",
                        required=True,
                        placeholder="Enter your password",
                        autocomplete="current-password",
                    ),
                    SubmitButton("Sign In"),
                    method="post",
                    action="/api/auth/login",
                ),
                cls="form-card",
            ),
            cls="container",
        ),
        title="Sign In - Test Case Management",
    )
