"""
Search page for global search across all entities.
"""

from fasthtml.common import *
from tcm.pages.components import (
    PageLayout,
    ActionButton,
    TagBadge,
    SelectField,
)


def SearchForm(
    query: str = "",
    entity_type: str = "",
    status_filter: str = "",
    category_filter: str = "",
):
    """
    Render the search form with filters.

    Args:
        query: Current search query
        entity_type: Current entity type filter
        status_filter: Current status filter
        category_filter: Current category filter (for tags)

    Returns:
        FastHTML form element
    """
    entity_type_options = [
        ("", "All Types"),
        ("testcase", "Test Cases"),
        ("project", "Projects"),
        ("tag", "Tags"),
    ]

    status_options = [
        ("", "Any Status"),
        ("draft", "Draft"),
        ("active", "Active"),
        ("deprecated", "Deprecated"),
        ("archived", "Archived"),
        ("planning", "Planning"),
        ("on_hold", "On Hold"),
        ("completed", "Completed"),
    ]

    return Div(
        Form(
            Div(
                Div(
                    Label("Search", **{"for": "query"}),
                    Input(
                        type="text",
                        name="query",
                        id="query",
                        placeholder="Search for test cases, projects, or tags...",
                        value=query,
                        cls="form-input form-input-large",
                        autofocus=True,
                    ),
                    cls="search-input-container",
                ),
                Div(
                    SelectField(
                        name="entity_type",
                        label="Type",
                        options=entity_type_options,
                        selected_value=entity_type,
                        placeholder="All Types",
                    ),
                    cls="search-filter",
                ),
                Div(
                    SelectField(
                        name="status",
                        label="Status",
                        options=status_options,
                        selected_value=status_filter,
                        placeholder="Any Status",
                    ),
                    cls="search-filter",
                ),
                cls="search-form-fields",
            ),
            Div(
                Button("Search", type="submit", cls="btn btn-primary btn-medium"),
                Button(
                    "Clear",
                    type="button",
                    onclick="window.location.href='/search'",
                    cls="btn btn-secondary btn-medium",
                ),
                cls="search-form-actions",
            ),
            method="get",
            action="/search",
            cls="search-form",
        ),
        cls="search-form-container",
    )


def SearchResultItem(result: dict):
    """
    Render a single search result item.

    Args:
        result: Result dict with entity information

    Returns:
        FastHTML div element for result item
    """
    entity_type = result["entity_type"]

    # Different layouts based on entity type
    if entity_type == "testcase":
        return Div(
            Div(
                Div(
                    A(result["title"], href=result["link"], cls="result-title"),
                    Span(
                        result["status"].replace("_", " ").title(),
                        cls=f"status-badge status-{result['status']}",
                    ),
                    cls="result-header",
                ),
                (
                    P(result.get("description", ""), cls="result-description")
                    if result.get("description")
                    else None
                ),
                Div(
                    Span(f"Priority: {result.get('priority', 'N/A').title()}", cls="result-meta-item"),
                    (
                        Div(
                            Span("Tags: ", cls="result-meta-label"),
                            *[
                                TagBadge(
                                    tag["value"],
                                    tag["category"],
                                    tag.get("is_predefined", False),
                                )
                                for tag in result.get("tags", [])[:5]
                            ],
                            cls="result-tags",
                        )
                        if result.get("tags")
                        else None
                    ),
                    cls="result-meta",
                ),
                cls="result-content",
            ),
            cls="search-result-item result-testcase",
        )
    elif entity_type == "project":
        return Div(
            Div(
                Div(
                    A(result["title"], href=result["link"], cls="result-title"),
                    Span(
                        result["status"].replace("_", " ").title(),
                        cls=f"status-badge status-{result['status']}",
                    ),
                    cls="result-header",
                ),
                (
                    P(result.get("description", ""), cls="result-description")
                    if result.get("description")
                    else None
                ),
                Div(
                    Span(f"Test Cases: {result.get('testcase_count', 0)}", cls="result-meta-item"),
                    (
                        Span(f"Start: {result.get('start_date', 'N/A')}", cls="result-meta-item")
                        if result.get("start_date")
                        else None
                    ),
                    (
                        Span(f"End: {result.get('end_date', 'N/A')}", cls="result-meta-item")
                        if result.get("end_date")
                        else None
                    ),
                    cls="result-meta",
                ),
                cls="result-content",
            ),
            cls="search-result-item result-project",
        )
    elif entity_type == "tag":
        return Div(
            Div(
                Div(
                    A(result["title"], href=result["link"], cls="result-title"),
                    Span(
                        "Predefined" if result.get("is_predefined") else "Custom",
                        cls=f"status-badge {'status-predefined' if result.get('is_predefined') else 'status-custom'}",
                    ),
                    cls="result-header",
                ),
                (
                    P(result.get("description", ""), cls="result-description")
                    if result.get("description")
                    else None
                ),
                Div(
                    Span(f"Category: {result['category'].replace('_', ' ').title()}", cls="result-meta-item"),
                    Span(f"Test Cases: {result.get('testcase_count', 0)}", cls="result-meta-item"),
                    cls="result-meta",
                ),
                cls="result-content",
            ),
            cls="search-result-item result-tag",
        )
    else:
        return Div()


def SearchResultsSection(entity_type: str, results: list[dict], query: str = ""):
    """
    Render a section of search results grouped by entity type.

    Args:
        entity_type: Type of entity (testcase, project, tag)
        results: List of result dicts
        query: Search query for highlighting

    Returns:
        FastHTML div element with results section
    """
    entity_type_labels = {
        "testcase": "Test Cases",
        "project": "Projects",
        "tag": "Tags",
    }

    if not results:
        return None

    return Div(
        Div(
            H3(
                f"{entity_type_labels.get(entity_type, entity_type.title())} ({len(results)})",
                cls="results-section-title",
            ),
            cls="results-section-header",
        ),
        Div(
            *[SearchResultItem(result) for result in results],
            cls="results-section-content",
        ),
        cls="search-results-section",
    )


def SearchPage(
    query: str = "",
    entity_type: str = "",
    status_filter: str = "",
    category_filter: str = "",
    results: dict = None,
    total_count: int = 0,
):
    """
    Render the search page with form and results.

    Args:
        query: Current search query
        entity_type: Current entity type filter
        status_filter: Current status filter
        category_filter: Current category filter
        results: Dictionary of results grouped by entity type
        total_count: Total number of results across all types

    Returns:
        FastHTML page with search interface
    """
    results = results or {}

    # Show results summary if there's a query
    results_summary = None
    if query:
        if total_count == 0:
            results_summary = Div(
                P(f'No results found for "{query}".', cls="empty-message"),
                cls="empty-state",
            )
        else:
            results_summary = Div(
                P(
                    f'Found {total_count} result{"s" if total_count != 1 else ""} for "{query}"',
                    cls="results-summary",
                ),
                cls="results-summary-container",
            )

    # Build results sections
    result_sections = []
    for etype in ["testcase", "project", "tag"]:
        if etype in results and results[etype]:
            section = SearchResultsSection(etype, results[etype], query)
            if section:
                result_sections.append(section)

    return PageLayout(
        Div(
            # Header
            Div(
                H2("Search", cls="page-title"),
                cls="page-header-content",
            ),
            # Search form
            SearchForm(
                query=query,
                entity_type=entity_type,
                status_filter=status_filter,
                category_filter=category_filter,
            ),
            # Results summary
            results_summary,
            # Results sections
            Div(
                *result_sections if result_sections else [],
                cls="search-results",
            ),
            cls="container container-wide",
        ),
        title="Search - Test Case Management",
    )
