"""
Tags list page for browsing and managing tags.
"""

from fasthtml.common import *
from tcm.pages.components import (
    PageLayout,
    TagBadge,
    ActionButton,
    CategoryGroup,
    SelectField,
    ErrorMessage,
    SuccessMessage,
)


def TagRow(tag: dict):
    """
    Render a single tag row in the list.

    Args:
        tag: Tag data dictionary

    Returns:
        FastHTML table row element
    """
    return Tr(
        Td(TagBadge(tag["value"], tag["category"], tag.get("is_predefined", False))),
        Td(tag["category"].replace("_", " ").title()),
        Td(tag.get("description", "") or "-"),
        Td(
            Span("Predefined", cls="status-badge status-predefined")
            if tag.get("is_predefined")
            else Span("Custom", cls="status-badge status-custom")
        ),
        Td(
            Div(
                ActionButton("Edit", href=f"/tags/{tag['id']}/edit", size="small"),
                ActionButton(
                    "Delete",
                    onclick=f"confirmDelete({tag['id']}, '{tag['value']}')",
                    btn_type="danger",
                    size="small",
                ),
                cls="action-buttons",
            ) if not tag.get("is_predefined") else Span("System Tag", cls="system-tag-indicator")
        ),
        cls="tag-row",
    )


def TagsTable(tags: list[dict]):
    """
    Render the tags table.

    Args:
        tags: List of tag data dictionaries

    Returns:
        FastHTML table element
    """
    if not tags:
        return Div(
            P("No tags found.", cls="empty-message"),
            cls="empty-state",
        )

    return Table(
        Thead(
            Tr(
                Th("Tag"),
                Th("Category"),
                Th("Description"),
                Th("Type"),
                Th("Actions"),
            )
        ),
        Tbody(*[TagRow(tag) for tag in tags]),
        cls="data-table",
    )


def CategoryTagsGroup(category: str, tags: list[dict]):
    """
    Render a group of tags for a category.

    Args:
        category: Category name
        tags: List of tags in this category

    Returns:
        FastHTML CategoryGroup element
    """
    return CategoryGroup(
        category=category,
        count=len(tags),
        children=TagsTable(tags),
    )


def TagsListPage(
    tags: list[dict],
    categories: list[str],
    current_category: str = "",
    success_message: str = "",
    error_message: str = "",
    grouped: bool = True,
):
    """
    Render the tags list page.

    Args:
        tags: List of tag data dictionaries
        categories: List of available categories for filtering
        current_category: Currently selected category filter
        success_message: Success message to display
        error_message: Error message to display
        grouped: Whether to group tags by category

    Returns:
        FastHTML page with tags list
    """
    # Prepare category options for filter dropdown
    category_options = [("", "All Categories")] + [
        (cat, cat.replace("_", " ").title()) for cat in categories
    ]

    # Handle empty state
    if not tags:
        content_list = [
            Div(
                P("No tags found.", cls="empty-message"),
                cls="empty-state",
            )
        ]
    # Group tags by category if needed
    elif grouped and not current_category:
        tags_by_category = {}
        for tag in tags:
            cat = tag["category"]
            if cat not in tags_by_category:
                tags_by_category[cat] = []
            tags_by_category[cat].append(tag)

        content_list = [
            CategoryTagsGroup(cat, cat_tags)
            for cat, cat_tags in sorted(tags_by_category.items())
        ]
    else:
        content_list = [TagsTable(tags)]

    return PageLayout(
        Div(
            Div(
                H2("Tags Management", cls="page-title"),
                Div(
                    ActionButton("Create New Tag", href="/tags/new", btn_type="primary"),
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
                            name="category",
                            label="Filter by Category",
                            options=category_options,
                            selected_value=current_category,
                            placeholder="All Categories",
                        ),
                        cls="filter-field",
                    ),
                    Button("Filter", type="submit", cls="btn btn-secondary btn-small"),
                    Button(
                        "Clear",
                        type="button",
                        onclick="window.location.href='/tags'",
                        cls="btn btn-secondary btn-small",
                    ),
                    method="get",
                    action="/tags",
                    cls="filter-form",
                ),
                cls="filter-section",
            ),
            # Tags content
            Div(
                *content_list,
                cls="tags-content",
            ),
            # Delete confirmation script
            Script("""
                function confirmDelete(tagId, tagValue) {
                    if (confirm('Are you sure you want to delete the tag "' + tagValue + '"?')) {
                        fetch('/api/tags/' + tagId, {
                            method: 'DELETE',
                        }).then(response => {
                            if (response.ok) {
                                window.location.href = '/tags?success=Tag deleted successfully';
                            } else {
                                response.json().then(data => {
                                    alert('Error: ' + (data.detail || 'Failed to delete tag'));
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
        title="Tags - Test Case Management",
    )
