"""
Layout components for consistent page structure.
"""

from fasthtml.common import *


def PageLayout(
    *content,
    title: str = "Test Case Management",
    show_header: bool = True,
    show_footer: bool = True,
):
    """
    Consistent page layout wrapper for all pages.

    Args:
        *content: Content to display in the main area
        title: Page title for the browser tab
        show_header: Whether to display the header
        show_footer: Whether to display the footer

    Returns:
        FastHTML page structure with header, main content, and footer
    """
    return Html(
        Head(
            Title(title),
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Link(rel="stylesheet", href="/static/css/styles.css"),
        ),
        Body(
            Div(
                (
                    Header(
                        H1("Test Case Management"),
                        cls="page-header",
                    )
                    if show_header
                    else None
                ),
                Main(*content, cls="page-main"),
                (
                    Footer(
                        P(f"© 2025 Test Case Management. All rights reserved."),
                        cls="page-footer",
                    )
                    if show_footer
                    else None
                ),
                cls="page-container",
            )
        ),
    )
