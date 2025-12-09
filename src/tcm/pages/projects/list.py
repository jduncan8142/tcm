"""
Projects list page for browsing and managing projects.
"""

from fasthtml.common import *
from tcm.pages.components import (
    PageLayout,
    ActionButton,
    SelectField,
    ErrorMessage,
    SuccessMessage,
)


def StatusBadge(status: str):
    """
    Render a status badge for a project.

    Args:
        status: Project status (planning, active, on_hold, completed, archived)

    Returns:
        FastHTML span element styled as a status badge
    """
    status_map = {
        "planning": "Planning",
        "active": "Active",
        "on_hold": "On Hold",
        "completed": "Completed",
        "archived": "Archived",
    }

    display_text = status_map.get(status, status.replace("_", " ").title())

    return Span(
        display_text,
        cls=f"status-badge status-{status.replace('_', '-')}",
    )


def ProjectRow(project: dict):
    """
    Render a single project row in the list.

    Args:
        project: Project data dictionary

    Returns:
        FastHTML table row element
    """
    # Format dates
    start_date = project.get("start_date", "")
    end_date = project.get("end_date", "")

    if start_date and end_date:
        date_range = f"{start_date[:10]} to {end_date[:10]}"
    elif start_date:
        date_range = f"From {start_date[:10]}"
    elif end_date:
        date_range = f"Until {end_date[:10]}"
    else:
        date_range = "-"

    testcase_count = len(project.get("testcase_ids", []))

    return Tr(
        Td(A(project["name"], href=f"/projects/{project['id']}", cls="project-link")),
        Td(StatusBadge(project["status"])),
        Td(date_range),
        Td(str(testcase_count), cls="text-center"),
        Td(
            Div(
                ActionButton("View", href=f"/projects/{project['id']}", size="small"),
                ActionButton("Edit", href=f"/projects/{project['id']}/edit", size="small"),
                ActionButton(
                    "Delete",
                    onclick=f"confirmDelete({project['id']}, '{project['name']}')",
                    btn_type="danger",
                    size="small",
                ),
                cls="action-buttons",
            )
        ),
        cls="project-row",
    )


def ProjectsTable(projects: list[dict]):
    """
    Render the projects table.

    Args:
        projects: List of project data dictionaries

    Returns:
        FastHTML table element
    """
    if not projects:
        return Div(
            P("No projects found.", cls="empty-message"),
            cls="empty-state",
        )

    return Table(
        Thead(
            Tr(
                Th("Name"),
                Th("Status"),
                Th("Date Range"),
                Th("Test Cases", cls="text-center"),
                Th("Actions"),
            )
        ),
        Tbody(*[ProjectRow(project) for project in projects]),
        cls="data-table",
    )


def ProjectsListPage(
    projects: list[dict],
    statuses: list[str],
    current_status: str = "",
    success_message: str = "",
    error_message: str = "",
):
    """
    Render the projects list page.

    Args:
        projects: List of project data dictionaries
        statuses: List of available statuses for filtering
        current_status: Currently selected status filter
        success_message: Success message to display
        error_message: Error message to display

    Returns:
        FastHTML page with projects list
    """
    # Prepare status options for filter dropdown
    status_options = [("", "All Statuses")] + [
        (status, status.replace("_", " ").title()) for status in statuses
    ]

    return PageLayout(
        Div(
            Div(
                H2("Projects", cls="page-title"),
                Div(
                    ActionButton("Create New Project", href="/projects/new", btn_type="primary"),
                    cls="page-actions",
                ),
                cls="page-header-content",
            ),
            SuccessMessage(success_message),
            ErrorMessage(error_message),
            # Filter section
            Div(
                Form(
                    Div(
                        SelectField(
                            name="status",
                            label="Filter by Status",
                            options=status_options,
                            selected_value=current_status,
                            placeholder="All Statuses",
                        ),
                        cls="filter-field",
                    ),
                    Button("Filter", type="submit", cls="btn btn-secondary btn-small"),
                    Button(
                        "Clear",
                        type="button",
                        onclick="window.location.href='/projects'",
                        cls="btn btn-secondary btn-small",
                    ),
                    method="get",
                    action="/projects",
                    cls="filter-form",
                ),
                cls="filter-section",
            ),
            # Projects content
            Div(
                ProjectsTable(projects),
                cls="projects-content",
            ),
            # Delete confirmation script
            Script("""
                function confirmDelete(projectId, projectName) {
                    if (confirm('Are you sure you want to delete the project "' + projectName + '"?')) {
                        fetch('/api/projects/' + projectId, {
                            method: 'DELETE',
                        }).then(response => {
                            if (response.ok) {
                                window.location.href = '/projects?success=Project deleted successfully';
                            } else {
                                response.json().then(data => {
                                    alert('Error: ' + (data.detail || 'Failed to delete project'));
                                });
                            }
                        }).catch(error => {
                            alert('Error: ' + error.message);
                        });
                    }
                }
            """),
            cls="container container-wide",
        ),
        title="Projects - Test Case Management",
    )
