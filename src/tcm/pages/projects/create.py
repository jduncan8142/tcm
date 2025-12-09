"""
Create project page.
"""

from fasthtml.common import *
from tcm.pages.components import (
    PageLayout,
    InputField,
    SelectField,
    TextAreaField,
    SubmitButton,
    ActionButton,
    ErrorMessage,
)


def CreateProjectPage(
    error_message: str = "",
    form_data: dict | None = None,
):
    """
    Render the create project page.

    Args:
        error_message: Error message to display
        form_data: Previously submitted form data for repopulating fields

    Returns:
        FastHTML page with project creation form
    """
    form_data = form_data or {}

    # Status options
    status_options = [
        ("planning", "Planning"),
        ("active", "Active"),
        ("on_hold", "On Hold"),
        ("completed", "Completed"),
        ("archived", "Archived"),
    ]

    return PageLayout(
        Div(
            Div(
                H2("Create New Project", cls="form-title"),
                ErrorMessage(error_message),
                Form(
                    InputField(
                        name="name",
                        label="Project Name",
                        required=True,
                        placeholder="Enter project name",
                        value=form_data.get("name", ""),
                    ),
                    TextAreaField(
                        name="description",
                        label="Description",
                        placeholder="Enter project description (optional)",
                        value=form_data.get("description", ""),
                        rows=4,
                    ),
                    SelectField(
                        name="status",
                        label="Status",
                        options=status_options,
                        required=True,
                        selected_value=form_data.get("status", "planning"),
                        placeholder="Select status",
                    ),
                    InputField(
                        name="start_date",
                        label="Start Date",
                        input_type="date",
                        placeholder="Select start date",
                        value=form_data.get("start_date", ""),
                    ),
                    InputField(
                        name="end_date",
                        label="End Date",
                        input_type="date",
                        placeholder="Select end date",
                        value=form_data.get("end_date", ""),
                    ),
                    Div(
                        SubmitButton("Create Project"),
                        ActionButton("Cancel", href="/projects", btn_type="secondary"),
                        cls="form-actions",
                    ),
                    method="post",
                    action="/projects/new",
                ),
                cls="form-card form-card-wide",
            ),
            cls="container",
        ),
        title="Create Project - Test Case Management",
    )
