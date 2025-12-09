"""
Edit tag page.
"""

from fasthtml.common import *
from tcm.pages.components import (
    PageLayout,
    InputField,
    SelectField,
    TextAreaField,
    CheckboxField,
    SubmitButton,
    ActionButton,
    ErrorMessage,
)


def EditTagPage(
    tag: dict,
    categories: list[str],
    error_message: str = "",
):
    """
    Render the edit tag page.

    Args:
        tag: Tag data dictionary with id, category, value, description, is_predefined
        categories: List of existing categories for dropdown
        error_message: Error message to display

    Returns:
        FastHTML page with tag edit form
    """
    # Prepare category options for dropdown with custom input
    category_options = [(cat, cat.replace("_", " ").title()) for cat in categories]

    return PageLayout(
        Div(
            Div(
                H2("Edit Tag", cls="form-title"),
                ErrorMessage(error_message),
                Form(
                    SelectField(
                        name="category",
                        label="Category",
                        options=category_options,
                        required=True,
                        selected_value=tag.get("category", ""),
                        placeholder="Select or enter a category",
                        allow_custom=True,
                    ),
                    InputField(
                        name="value",
                        label="Value",
                        required=True,
                        placeholder="Enter tag value",
                        value=tag.get("value", ""),
                    ),
                    TextAreaField(
                        name="description",
                        label="Description",
                        placeholder="Enter tag description (optional)",
                        value=tag.get("description", "") or "",
                        rows=3,
                    ),
                    CheckboxField(
                        name="is_predefined",
                        label="Mark as predefined tag",
                        checked=tag.get("is_predefined", False),
                    ),
                    Div(
                        SubmitButton("Save Changes"),
                        ActionButton("Cancel", href="/tags", btn_type="secondary"),
                        cls="form-actions",
                    ),
                    method="post",
                    action=f"/tags/{tag['id']}/edit",
                ),
                cls="form-card form-card-wide",
            ),
            cls="container",
        ),
        title="Edit Tag - Test Case Management",
    )


def NotFoundPage():
    """
    Render a 404 page for non-existent tags.

    Returns:
        FastHTML 404 error page
    """
    return PageLayout(
        Div(
            Div(
                H2("Tag Not Found", cls="form-title"),
                P("The requested tag could not be found."),
                ActionButton("Back to Tags", href="/tags", btn_type="primary"),
                cls="form-card",
            ),
            cls="container",
        ),
        title="Tag Not Found - Test Case Management",
    )
