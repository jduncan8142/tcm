"""
Test cases list page for browsing and managing test cases.
"""

from fasthtml.common import *
from tcm.pages.components import (
    PageLayout,
    TagBadge,
    ActionButton,
    SelectField,
    InputField,
    ErrorMessage,
    SuccessMessage,
)


def TestCaseRow(testcase: dict):
    """
    Render a single test case row in the list.

    Args:
        testcase: Test case data dictionary

    Returns:
        FastHTML table row element
    """
    # Format priority and status for display
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

    # Count tags
    tag_count = len(testcase.get("tags", []))

    return Tr(
        Td(A(testcase["title"], href=f"/testcases/{testcase['id']}", cls="testcase-title-link")),
        Td(Span(status_display, cls=status_cls)),
        Td(Span(priority_display, cls=priority_cls)),
        Td(str(tag_count)),
        Td(
            Div(
                ActionButton("View", href=f"/testcases/{testcase['id']}", size="small"),
                ActionButton("Edit", href=f"/testcases/{testcase['id']}/edit", size="small"),
                ActionButton(
                    "Delete",
                    onclick=f"confirmDelete({testcase['id']}, '{testcase['title'].replace(chr(39), chr(92)+chr(39))}')",
                    btn_type="danger",
                    size="small",
                ),
                cls="action-buttons",
            )
        ),
        cls="testcase-row",
    )


def TestCasesTable(testcases: list[dict]):
    """
    Render the test cases table.

    Args:
        testcases: List of test case data dictionaries

    Returns:
        FastHTML table element
    """
    if not testcases:
        return Div(
            P("No test cases found.", cls="empty-message"),
            cls="empty-state",
        )

    return Table(
        Thead(
            Tr(
                Th("Title"),
                Th("Status"),
                Th("Priority"),
                Th("Tags"),
                Th("Actions"),
            )
        ),
        Tbody(*[TestCaseRow(tc) for tc in testcases]),
        cls="data-table",
    )


def PaginationControls(current_page: int, total_pages: int, base_url: str):
    """
    Render pagination controls.

    Args:
        current_page: Current page number (1-indexed)
        total_pages: Total number of pages
        base_url: Base URL for pagination links (with existing query params)

    Returns:
        FastHTML pagination element
    """
    if total_pages <= 1:
        return None

    # Add page separator if base_url has query params
    separator = "&" if "?" in base_url else "?"

    controls = []

    # Previous button
    if current_page > 1:
        controls.append(
            A("Previous", href=f"{base_url}{separator}page={current_page - 1}", cls="btn btn-secondary btn-small")
        )
    else:
        controls.append(
            Span("Previous", cls="btn btn-secondary btn-small btn-disabled")
        )

    # Page info
    controls.append(
        Span(f"Page {current_page} of {total_pages}", cls="page-info")
    )

    # Next button
    if current_page < total_pages:
        controls.append(
            A("Next", href=f"{base_url}{separator}page={current_page + 1}", cls="btn btn-secondary btn-small")
        )
    else:
        controls.append(
            Span("Next", cls="btn btn-secondary btn-small btn-disabled")
        )

    return Div(*controls, cls="pagination-controls")


def TestCasesListPage(
    testcases: list[dict],
    total: int,
    page: int = 1,
    page_size: int = 20,
    search: str = "",
    status_filter: str = "",
    priority_filter: str = "",
    tag_filter: str = "",
    available_tags: list[dict] = None,
    success_message: str = "",
    error_message: str = "",
):
    """
    Render the test cases list page.

    Args:
        testcases: List of test case data dictionaries
        total: Total number of test cases (before pagination)
        page: Current page number (1-indexed)
        page_size: Number of items per page
        search: Search query
        status_filter: Status filter value
        priority_filter: Priority filter value
        tag_filter: Tag filter value (tag ID)
        available_tags: List of available tags for filtering
        success_message: Success message to display
        error_message: Error message to display

    Returns:
        FastHTML page with test cases list
    """
    available_tags = available_tags or []

    # Calculate pagination
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1

    # Build base URL for pagination (preserving filters)
    base_url_parts = ["/testcases?"]
    url_params = []
    if search:
        url_params.append(f"search={search}")
    if status_filter:
        url_params.append(f"status={status_filter}")
    if priority_filter:
        url_params.append(f"priority={priority_filter}")
    if tag_filter:
        url_params.append(f"tag_id={tag_filter}")
    base_url = "/testcases?" + "&".join(url_params) if url_params else "/testcases"

    # Status options
    status_options = [
        ("", "All Statuses"),
        ("draft", "Draft"),
        ("active", "Active"),
        ("deprecated", "Deprecated"),
        ("archived", "Archived"),
    ]

    # Priority options
    priority_options = [
        ("", "All Priorities"),
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    # Tag options
    tag_options = [("", "All Tags")] + [
        (str(tag["id"]), f"{tag['category']}: {tag['value']}")
        for tag in available_tags
    ]

    return PageLayout(
        Div(
            Div(
                H2("Test Cases", cls="page-title"),
                Div(
                    ActionButton("Create New Test Case", href="/testcases/new", btn_type="primary"),
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
                        Div(
                            InputField(
                                name="search",
                                label="Search",
                                placeholder="Search by title or description...",
                                value=search,
                            ),
                            cls="filter-field filter-field-wide",
                        ),
                        Div(
                            SelectField(
                                name="status",
                                label="Status",
                                options=status_options,
                                selected_value=status_filter,
                            ),
                            cls="filter-field",
                        ),
                        Div(
                            SelectField(
                                name="priority",
                                label="Priority",
                                options=priority_options,
                                selected_value=priority_filter,
                            ),
                            cls="filter-field",
                        ),
                        Div(
                            SelectField(
                                name="tag_id",
                                label="Tag",
                                options=tag_options,
                                selected_value=tag_filter,
                            ),
                            cls="filter-field",
                        ),
                        cls="filter-fields",
                    ),
                    Div(
                        Button("Filter", type="submit", cls="btn btn-secondary btn-small"),
                        Button(
                            "Clear",
                            type="button",
                            onclick="window.location.href='/testcases'",
                            cls="btn btn-secondary btn-small",
                        ),
                        cls="filter-actions",
                    ),
                    method="get",
                    action="/testcases",
                    cls="filter-form",
                ),
                cls="filter-section",
            ),
            # Results summary
            Div(
                P(f"Showing {len(testcases)} of {total} test cases", cls="results-summary"),
                cls="results-info",
            ),
            # Test cases content
            Div(
                TestCasesTable(testcases),
                cls="testcases-content",
            ),
            # Pagination
            PaginationControls(page, total_pages, base_url),
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
        title="Test Cases - Test Case Management",
    )
