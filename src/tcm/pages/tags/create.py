"""
Create tag page.
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


def CreateTagPage(
    categories: list[str],
    error_message: str = "",
    form_data: dict | None = None,
):
    """
    Render the create tag page.

    Args:
        categories: List of existing categories for dropdown
        error_message: Error message to display
        form_data: Previously submitted form data for repopulating fields

    Returns:
        FastHTML page with tag creation form
    """
    form_data = form_data or {}

    # Prepare category options for dropdown with custom input
    category_options = [(cat, cat.replace("_", " ").title()) for cat in categories]

    return PageLayout(
        Div(
            Div(
                H2("Create New Tag", cls="form-title"),
                ErrorMessage(error_message),
                Form(
                    SelectField(
                        name="category",
                        label="Category",
                        options=category_options,
                        required=True,
                        selected_value=form_data.get("category", ""),
                        placeholder="Select or enter a category",
                        allow_custom=True,
                    ),
                    InputField(
                        name="value",
                        label="Value",
                        required=True,
                        placeholder="Enter tag value",
                        value=form_data.get("value", ""),
                    ),
                    TextAreaField(
                        name="description",
                        label="Description",
                        placeholder="Enter tag description (optional)",
                        value=form_data.get("description", ""),
                        rows=3,
                    ),
                    Div(
                        SubmitButton("Create Tag"),
                        ActionButton("Cancel", href="/tags", btn_type="secondary"),
                        cls="form-actions",
                    ),
                    method="post",
                    action="/tags/new",
                ),
                cls="form-card form-card-wide",
            ),
            cls="container",
        ),
        title="Create Tag - Test Case Management",
    )
