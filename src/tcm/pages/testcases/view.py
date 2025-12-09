"""
View test case details page.
"""

from fasthtml.common import *
from tcm.pages.components import (
    PageLayout,
    TagBadge,
    ActionButton,
    SuccessMessage,
)


def DetailRow(label: str, value: str | None, value_cls: str = ""):
    """
    Render a detail row with label and value.

    Args:
        label: Field label
        value: Field value
        value_cls: Additional CSS classes for value

    Returns:
        FastHTML div element
    """
    display_value = value if value else "-"
    return Div(
        Div(Strong(label), cls="detail-label"),
        Div(display_value, cls=f"detail-value {value_cls}"),
        cls="detail-row",
    )


def DetailSection(title: str, *children):
    """
    Render a detail section with title and children.

    Args:
        title: Section title
        children: Section content elements

    Returns:
        FastHTML div element
    """
    return Div(
        H3(title, cls="detail-section-title"),
        Div(*children, cls="detail-section-content"),
        cls="detail-section",
    )


def ViewTestCasePage(
    testcase: dict,
    success_message: str = "",
):
    """
    Render the view test case details page.

    Args:
        testcase: Test case data dictionary with all fields
        success_message: Success message to display

    Returns:
        FastHTML page with test case details
    """
    # Format status and priority for display
    status_display = testcase["status"].replace("_", " ").title()
    priority_display = testcase["priority"].replace("_", " ").title()

    # Status badge styling
    status_class_map = {
        "draft": "status-badge-draft",
        "active": "status-badge-active",
        "deprecated": "status-badge-deprecated",
        "archived": "status-badge-archived",
    }
    status_cls = f"status-badge {status_class_map.get(testcase['status'], '')}"

    # Priority badge styling
    priority_class_map = {
        "low": "priority-badge-low",
        "medium": "priority-badge-medium",
        "high": "priority-badge-high",
        "critical": "priority-badge-critical",
    }
    priority_cls = f"priority-badge {priority_class_map.get(testcase['priority'], '')}"

    # Format timestamps
    created_at = testcase.get("created_at", "")
    updated_at = testcase.get("updated_at", "")

    # Extract tags
    tags = testcase.get("tags", [])

    # Extract projects
    projects = testcase.get("projects", [])

    # Build tags display
    tags_display = Div(
        *[
            TagBadge(
                tag["value"],
                tag["category"],
                tag.get("is_predefined", False),
                show_category=True
            )
            for tag in tags
        ],
        cls="tags-display",
    ) if tags else P("No tags assigned", cls="empty-message")

    # Build projects display
    projects_display = Div(
        *[
            Div(
                A(project["name"], href=f"/projects/{project['id']}", cls="project-link"),
                cls="project-item",
            )
            for project in projects
        ],
        cls="projects-display",
    ) if projects else P("Not used in any projects", cls="empty-message")

    return PageLayout(
        Div(
            Div(
                Div(
                    H2(testcase["title"], cls="page-title"),
                    Div(
                        ActionButton("Edit", href=f"/testcases/{testcase['id']}/edit", btn_type="primary"),
                        ActionButton(
                            "Delete",
                            onclick=f"confirmDelete({testcase['id']}, '{testcase['title'].replace(chr(39), chr(92)+chr(39))}')",
                            btn_type="danger",
                        ),
                        ActionButton("Back to List", href="/testcases", btn_type="secondary"),
                        cls="page-actions",
                    ),
                    cls="page-header-content",
                ),
                cls="page-header",
            ),
            SuccessMessage(success_message),
            # Main details
            DetailSection(
                "Basic Information",
                DetailRow("ID", str(testcase["id"])),
                DetailRow("Status", Span(status_display, cls=status_cls)),
                DetailRow("Priority", Span(priority_display, cls=priority_cls)),
                DetailRow("Description", testcase.get("description")),
            ),
            # Test case details
            DetailSection(
                "Test Details",
                DetailRow("Preconditions", testcase.get("preconditions")),
                Div(
                    Div(Strong("Steps"), cls="detail-label"),
                    Div(
                        Pre(testcase["steps"], cls="code-block"),
                        cls="detail-value",
                    ),
                    cls="detail-row",
                ),
                Div(
                    Div(Strong("Expected Results"), cls="detail-label"),
                    Div(
                        Pre(testcase["expected_results"], cls="code-block"),
                        cls="detail-value",
                    ),
                    cls="detail-row",
                ),
                DetailRow("Actual Results", testcase.get("actual_results")),
            ),
            # Tags and associations
            DetailSection(
                "Tags",
                tags_display,
            ),
            DetailSection(
                "Projects Using This Test Case",
                projects_display,
            ),
            # Audit information
            DetailSection(
                "Audit Information",
                DetailRow("Created At", created_at),
                DetailRow("Updated At", updated_at),
                DetailRow("Created By", testcase.get("created_by")),
                DetailRow("Updated By", testcase.get("updated_by")),
            ),
            # Delete confirmation script
            Script("""
                function confirmDelete(testcaseId, testcaseTitle) {
                    if (confirm('Are you sure you want to delete the test case "' + testcaseTitle + '"?')) {
                        fetch('/api/testcases/' + testcaseId, {
                            method: 'DELETE',
                        }).then(response => {
                            if (response.ok || response.status === 204) {
                                window.location.href = '/testcases?success=Test case deleted successfully';
                            } else {
                                response.json().then(data => {
                                    alert('Error: ' + (data.detail || 'Failed to delete test case'));
                                }).catch(() => {
                                    alert('Error: Failed to delete test case');
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
        title=f"{testcase['title']} - Test Case Management",
    )


def NotFoundPage():
    """
    Render a 404 page for non-existent test cases.

    Returns:
        FastHTML 404 error page
    """
    return PageLayout(
        Div(
            Div(
                H2("Test Case Not Found", cls="form-title"),
                P("The requested test case could not be found."),
                ActionButton("Back to Test Cases", href="/testcases", btn_type="primary"),
                cls="form-card",
            ),
            cls="container",
        ),
        title="Test Case Not Found - Test Case Management",
    )
