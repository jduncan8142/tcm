"""
Edit project page.
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


def EditProjectPage(
    project: dict,
    error_message: str = "",
):
    """
    Render the edit project page.

    Args:
        project: Project data dictionary with id, name, description, status, start_date, end_date
        error_message: Error message to display

    Returns:
        FastHTML page with project edit form
    """
    # Status options
    status_options = [
        ("planning", "Planning"),
        ("active", "Active"),
        ("on_hold", "On Hold"),
        ("completed", "Completed"),
        ("archived", "Archived"),
    ]

    # Format dates for input fields (YYYY-MM-DD)
    start_date = ""
    end_date = ""
    if project.get("start_date"):
        start_date = project["start_date"][:10] if len(project["start_date"]) > 10 else project["start_date"]
    if project.get("end_date"):
        end_date = project["end_date"][:10] if len(project["end_date"]) > 10 else project["end_date"]

    return PageLayout(
        Div(
            Div(
                H2("Edit Project", cls="form-title"),
                ErrorMessage(error_message),
                Form(
                    InputField(
                        name="name",
                        label="Project Name",
                        required=True,
                        placeholder="Enter project name",
                        value=project.get("name", ""),
                    ),
                    TextAreaField(
                        name="description",
                        label="Description",
                        placeholder="Enter project description (optional)",
                        value=project.get("description", "") or "",
                        rows=4,
                    ),
                    SelectField(
                        name="status",
                        label="Status",
                        options=status_options,
                        required=True,
                        selected_value=project.get("status", "planning"),
                        placeholder="Select status",
                    ),
                    InputField(
                        name="start_date",
                        label="Start Date",
                        input_type="date",
                        placeholder="Select start date",
                        value=start_date,
                    ),
                    InputField(
                        name="end_date",
                        label="End Date",
                        input_type="date",
                        placeholder="Select end date",
                        value=end_date,
                    ),
                    Div(
                        SubmitButton("Save Changes"),
                        ActionButton("Cancel", href=f"/projects/{project['id']}", btn_type="secondary"),
                        cls="form-actions",
                    ),
                    method="post",
                    action=f"/projects/{project['id']}/edit",
                ),
                cls="form-card form-card-wide",
            ),
            cls="container",
        ),
        title="Edit Project - Test Case Management",
    )


def NotFoundPage():
    """
    Render a 404 page for non-existent projects.

    Returns:
        FastHTML 404 error page
    """
    return PageLayout(
        Div(
            Div(
                H2("Project Not Found", cls="form-title"),
                P("The requested project could not be found."),
                ActionButton("Back to Projects", href="/projects", btn_type="primary"),
                cls="form-card",
            ),
            cls="container",
        ),
        title="Project Not Found - Test Case Management",
    )
