"""
Edit test case page.
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
    TagPickerField,
)


def MultiSelectTagField(
    name: str,
    label: str,
    available_tags: list[dict],
    selected_tag_ids: list[int] = None,
):
    """
    Multi-select tag field component.

    Args:
        name: Field name attribute
        label: Label text for the field
        available_tags: List of available tag dictionaries
        selected_tag_ids: List of selected tag IDs

    Returns:
        FastHTML div containing label and multi-select
    """
    selected_tag_ids = selected_tag_ids or []

    # Group tags by category for better organization
    tags_by_category = {}
    for tag in available_tags:
        cat = tag["category"]
        if cat not in tags_by_category:
            tags_by_category[cat] = []
        tags_by_category[cat].append(tag)

    # Create optgroup elements
    optgroups = []
    for category in sorted(tags_by_category.keys()):
        category_tags = tags_by_category[category]
        options = []
        for tag in category_tags:
            opt_attrs = {"value": str(tag["id"])}
            if tag["id"] in selected_tag_ids:
                opt_attrs["selected"] = True
            options.append(
                Option(tag["value"], **opt_attrs)
            )
        optgroups.append(
            Optgroup(*options, label=category.replace("_", " ").title())
        )

    return Div(
        Label(label, fr=name, cls="form-label"),
        Select(
            *optgroups,
            id=name,
            name=name,
            multiple=True,
            cls="form-input form-select form-select-multiple",
        ),
        P("Hold Ctrl/Cmd to select multiple tags", cls="form-help-text"),
        cls="form-group",
    )


def EditTestCasePage(
    testcase: dict,
    available_tags: list[dict] = None,
    error_message: str = "",
):
    """
    Render the edit test case page.

    Args:
        testcase: Test case data dictionary
        available_tags: List of available tags for selection
        error_message: Error message to display

    Returns:
        FastHTML page with test case edit form
    """
    available_tags = available_tags or []

    # Get selected tag IDs from testcase
    selected_tag_ids = [tag["id"] for tag in testcase.get("tags", [])]

    # Status options
    status_options = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("deprecated", "Deprecated"),
        ("archived", "Archived"),
    ]

    # Priority options
    priority_options = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    return PageLayout(
        Div(
            Div(
                H2("Edit Test Case", cls="form-title"),
                ErrorMessage(error_message),
                Form(
                    InputField(
                        name="title",
                        label="Title",
                        required=True,
                        placeholder="Enter test case title",
                        value=testcase.get("title", ""),
                    ),
                    TextAreaField(
                        name="description",
                        label="Description",
                        placeholder="Enter test case description (optional)",
                        value=testcase.get("description", "") or "",
                        rows=3,
                    ),
                    TextAreaField(
                        name="preconditions",
                        label="Preconditions",
                        placeholder="Enter preconditions (optional)",
                        value=testcase.get("preconditions", "") or "",
                        rows=3,
                    ),
                    TextAreaField(
                        name="steps",
                        label="Steps",
                        required=True,
                        placeholder="Enter test steps (one per line)",
                        value=testcase.get("steps", ""),
                        rows=5,
                    ),
                    TextAreaField(
                        name="expected_results",
                        label="Expected Results",
                        required=True,
                        placeholder="Enter expected results",
                        value=testcase.get("expected_results", ""),
                        rows=5,
                    ),
                    SelectField(
                        name="status",
                        label="Status",
                        options=status_options,
                        required=True,
                        selected_value=testcase.get("status", "draft"),
                    ),
                    SelectField(
                        name="priority",
                        label="Priority",
                        options=priority_options,
                        required=True,
                        selected_value=testcase.get("priority", "medium"),
                    ),
                    TagPickerField(
                        name="tag_ids",
                        label="Tags",
                        available_tags=available_tags,
                        selected_tag_ids=selected_tag_ids,
                    ),
                    Div(
                        SubmitButton("Save Changes"),
                        ActionButton("Cancel", href=f"/testcases/{testcase['id']}", btn_type="secondary"),
                        cls="form-actions",
                    ),
                    method="post",
                    action=f"/testcases/{testcase['id']}/edit",
                ),
                cls="form-card form-card-wide",
            ),
            cls="container container-wide",
        ),
        title="Edit Test Case - Test Case Management",
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
