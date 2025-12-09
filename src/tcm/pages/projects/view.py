"""
View project details page.
"""

from fasthtml.common import *
from tcm.pages.components import (
    PageLayout,
    ActionButton,
    ErrorMessage,
    SuccessMessage,
)
from tcm.pages.projects.list import StatusBadge


def TestCaseRow(testcase: dict, project_id: int):
    """
    Render a single test case row in the project view.

    Args:
        testcase: Test case data dictionary
        project_id: Project ID for the remove action

    Returns:
        FastHTML table row element
    """
    # Status and priority badges
    status = testcase.get("status", "draft")
    priority = testcase.get("priority", "medium")

    return Tr(
        Td(A(testcase.get("title", ""), href=f"/testcases/{testcase['id']}", cls="testcase-link")),
        Td(Span(status.replace("_", " ").title(), cls=f"status-badge status-{status}")),
        Td(Span(priority.title(), cls=f"priority-badge priority-{priority}")),
        Td(
            ActionButton(
                "Remove",
                onclick=f"confirmRemoveTestCase({project_id}, {testcase['id']}, '{testcase.get('title', '')}')",
                btn_type="danger",
                size="small",
            ),
            cls="text-right",
        ),
        cls="testcase-row",
    )


def TestCasesTable(testcases: list[dict], project_id: int):
    """
    Render the test cases table.

    Args:
        testcases: List of test case data dictionaries
        project_id: Project ID

    Returns:
        FastHTML table element
    """
    if not testcases:
        return Div(
            P("No test cases in this project.", cls="empty-message"),
            cls="empty-state",
        )

    return Table(
        Thead(
            Tr(
                Th("Title"),
                Th("Status"),
                Th("Priority"),
                Th("Actions", cls="text-right"),
            )
        ),
        Tbody(*[TestCaseRow(tc, project_id) for tc in testcases]),
        cls="data-table",
    )


def ViewProjectPage(
    project: dict,
    testcases: list[dict],
    available_testcases: list[dict],
    success_message: str = "",
    error_message: str = "",
):
    """
    Render the project details view page.

    Args:
        project: Project data dictionary
        testcases: List of test cases in the project
        available_testcases: List of all available test cases (for adding)
        success_message: Success message to display
        error_message: Error message to display

    Returns:
        FastHTML page with project details
    """
    # Format dates
    start_date = project.get("start_date", "")
    end_date = project.get("end_date", "")

    if start_date:
        start_date_display = start_date[:10] if len(start_date) > 10 else start_date
    else:
        start_date_display = "Not set"

    if end_date:
        end_date_display = end_date[:10] if len(end_date) > 10 else end_date
    else:
        end_date_display = "Not set"

    # Filter available test cases (exclude already added ones)
    testcase_ids = {tc["id"] for tc in testcases}
    remaining_testcases = [tc for tc in available_testcases if tc["id"] not in testcase_ids]

    return PageLayout(
        Div(
            # Header section
            Div(
                H2(project["name"], cls="page-title"),
                Div(
                    ActionButton("Back to Projects", href="/projects", btn_type="secondary"),
                    ActionButton("Edit", href=f"/projects/{project['id']}/edit", btn_type="secondary"),
                    ActionButton(
                        "Delete",
                        onclick=f"confirmDelete({project['id']}, '{project['name']}')",
                        btn_type="danger",
                    ),
                    cls="page-actions",
                ),
                cls="page-header-content",
            ),
            SuccessMessage(success_message),
            ErrorMessage(error_message),
            # Project details section
            Div(
                H3("Project Details", cls="section-title"),
                Div(
                    Div(
                        Strong("Status:"),
                        Span(" "),
                        StatusBadge(project["status"]),
                        cls="detail-item",
                    ),
                    Div(
                        Strong("Description:"),
                        P(project.get("description") or "No description provided", cls="detail-text"),
                        cls="detail-item",
                    ),
                    Div(
                        Strong("Start Date:"),
                        Span(f" {start_date_display}"),
                        cls="detail-item",
                    ),
                    Div(
                        Strong("End Date:"),
                        Span(f" {end_date_display}"),
                        cls="detail-item",
                    ),
                    Div(
                        Strong("Test Cases:"),
                        Span(f" {len(testcases)}"),
                        cls="detail-item",
                    ),
                    cls="details-grid",
                ),
                cls="details-section",
            ),
            # Test cases section
            Div(
                Div(
                    H3("Test Cases", cls="section-title"),
                    Div(
                        Button(
                            "Add Test Cases",
                            type="button",
                            onclick="showAddTestCaseModal()",
                            cls="btn btn-primary btn-small",
                        ),
                        cls="section-actions",
                    ),
                    cls="section-header",
                ),
                TestCasesTable(testcases, project["id"]),
                cls="testcases-section",
            ),
            # Add test case modal
            Div(
                Div(
                    Div(
                        H3("Add Test Cases to Project"),
                        Button(
                            "×",
                            type="button",
                            onclick="hideAddTestCaseModal()",
                            cls="modal-close",
                        ),
                        cls="modal-header",
                    ),
                    Div(
                        P("Select test cases to add to this project:", cls="modal-description") if remaining_testcases else P("All available test cases have been added to this project.", cls="modal-description"),
                        Div(
                            *[
                                Div(
                                    Label(
                                        Input(
                                            type="checkbox",
                                            name="testcase_ids",
                                            value=str(tc["id"]),
                                            cls="testcase-checkbox",
                                        ),
                                        Span(tc["title"], cls="testcase-label"),
                                        cls="testcase-option",
                                    ),
                                    cls="testcase-item",
                                )
                                for tc in remaining_testcases
                            ] if remaining_testcases else [],
                            cls="testcase-list",
                            id="testcase-list",
                        ),
                        cls="modal-body",
                    ),
                    Div(
                        Button("Cancel", type="button", onclick="hideAddTestCaseModal()", cls="btn btn-secondary"),
                        Button("Add Selected", type="button", onclick=f"addSelectedTestCases({project['id']})", cls="btn btn-primary", disabled=not remaining_testcases),
                        cls="modal-footer",
                    ),
                    cls="modal-content",
                ),
                id="add-testcase-modal",
                cls="modal",
                style="display: none;",
            ),
            # Scripts
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

                function confirmRemoveTestCase(projectId, testcaseId, testcaseTitle) {
                    if (confirm('Are you sure you want to remove "' + testcaseTitle + '" from this project?')) {
                        fetch('/api/projects/' + projectId + '/testcases/' + testcaseId, {
                            method: 'DELETE',
                        }).then(response => {
                            if (response.ok) {
                                window.location.href = '/projects/' + projectId + '?success=Test case removed successfully';
                            } else {
                                response.json().then(data => {
                                    alert('Error: ' + (data.detail || 'Failed to remove test case'));
                                });
                            }
                        }).catch(error => {
                            alert('Error: ' + error.message);
                        });
                    }
                }

                function showAddTestCaseModal() {
                    document.getElementById('add-testcase-modal').style.display = 'flex';
                }

                function hideAddTestCaseModal() {
                    document.getElementById('add-testcase-modal').style.display = 'none';
                }

                function addSelectedTestCases(projectId) {
                    const checkboxes = document.querySelectorAll('.testcase-checkbox:checked');
                    const testcaseIds = Array.from(checkboxes).map(cb => cb.value);

                    if (testcaseIds.length === 0) {
                        alert('Please select at least one test case to add.');
                        return;
                    }

                    // Add test cases one by one
                    let promises = testcaseIds.map(testcaseId =>
                        fetch('/api/projects/' + projectId + '/testcases/' + testcaseId, {
                            method: 'POST',
                        })
                    );

                    Promise.all(promises).then(responses => {
                        const allOk = responses.every(r => r.ok);
                        if (allOk) {
                            window.location.href = '/projects/' + projectId + '?success=Test cases added successfully';
                        } else {
                            alert('Some test cases could not be added. Please try again.');
                        }
                    }).catch(error => {
                        alert('Error: ' + error.message);
                    });
                }

                // Close modal when clicking outside
                window.onclick = function(event) {
                    const modal = document.getElementById('add-testcase-modal');
                    if (event.target === modal) {
                        hideAddTestCaseModal();
                    }
                }
            """),
            cls="container container-wide",
        ),
        title=f"{project['name']} - Test Case Management",
    )
