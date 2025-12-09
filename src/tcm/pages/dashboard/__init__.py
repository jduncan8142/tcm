"""
Dashboard page for displaying statistics and recent activity.
"""

from fasthtml.common import *
from tcm.pages.components import (
    PageLayout,
    ActionButton,
    TagBadge,
)


def StatisticsWidget(title: str, count: int, icon: str = "", color: str = "blue"):
    """
    Render a statistics widget showing a count and title.

    Args:
        title: Title of the statistic
        count: Numeric count to display
        icon: Optional icon character or emoji
        color: Color scheme (blue, green, orange, purple)

    Returns:
        FastHTML div element with statistic display
    """
    return Div(
        Div(
            Span(icon, cls=f"stat-icon stat-icon-{color}") if icon else None,
            Div(
                Div(str(count), cls="stat-count"),
                Div(title, cls="stat-title"),
                cls="stat-content",
            ),
            cls="stat-inner",
        ),
        cls=f"stat-widget stat-widget-{color}",
    )


def ActivityFeedItem(
    entity_type: str,
    entity_id: int,
    title: str,
    action: str,
    timestamp: str,
    link: str,
    status: str = "",
    tags: list[dict] = None,
):
    """
    Render a single activity feed item.

    Args:
        entity_type: Type of entity (testcase, project, tag)
        entity_id: Entity ID
        title: Title of the entity
        action: Action performed (created, updated)
        timestamp: Human-readable timestamp
        link: URL to the entity
        status: Optional status badge text
        tags: Optional list of tag dicts with category, value

    Returns:
        FastHTML div element for activity item
    """
    entity_icon_map = {
        "testcase": "\U0001F4CB",  # 📋
        "project": "\U0001F4C1",  # 📁
        "tag": "\U0001F3F7",  # 🏷
    }

    return Div(
        Div(
            Span(
                entity_icon_map.get(entity_type, "\U0001F4C4"),
                cls=f"activity-icon activity-icon-{entity_type}",
            ),
            Div(
                Div(
                    A(title, href=link, cls="activity-title"),
                    Span(f" {action}", cls="activity-action"),
                    cls="activity-header",
                ),
                Div(
                    Span(timestamp, cls="activity-time"),
                    (
                        Span(status.replace("_", " ").title(), cls=f"status-badge status-{status}")
                        if status
                        else None
                    ),
                    (
                        Div(
                            *[
                                TagBadge(
                                    tag["value"],
                                    tag["category"],
                                    tag.get("is_predefined", False),
                                )
                                for tag in (tags or [])[:3]
                            ],
                            cls="activity-tags",
                        )
                        if tags
                        else None
                    ),
                    cls="activity-meta",
                ),
                cls="activity-content",
            ),
            cls="activity-item-inner",
        ),
        cls="activity-item",
    )


def ActivityFeed(activities: list[dict]):
    """
    Render the activity feed with recent items.

    Args:
        activities: List of activity dicts

    Returns:
        FastHTML div element with activity feed
    """
    if not activities:
        return Div(
            P("No recent activity.", cls="empty-message"),
            cls="empty-state",
        )

    return Div(
        *[
            ActivityFeedItem(
                entity_type=activity["entity_type"],
                entity_id=activity["entity_id"],
                title=activity["title"],
                action=activity["action"],
                timestamp=activity["timestamp"],
                link=activity["link"],
                status=activity.get("status", ""),
                tags=activity.get("tags", []),
            )
            for activity in activities
        ],
        cls="activity-feed",
    )


def QuickActions():
    """
    Render quick action links for common operations.

    Returns:
        FastHTML div element with quick action buttons
    """
    return Div(
        H3("Quick Actions", cls="card-title"),
        Div(
            ActionButton(
                "Create Test Case",
                href="/testcases/new",
                btn_type="primary",
                size="medium",
            ),
            ActionButton(
                "Create Project",
                href="/projects/new",
                btn_type="secondary",
                size="medium",
            ),
            ActionButton(
                "Create Tag",
                href="/tags/new",
                btn_type="secondary",
                size="medium",
            ),
            ActionButton(
                "Search",
                href="/search",
                btn_type="secondary",
                size="medium",
            ),
            cls="quick-actions-grid",
        ),
        cls="quick-actions-card card",
    )


def DashboardPage(
    stats: dict,
    activities: list[dict],
):
    """
    Render the dashboard page with statistics and activity feed.

    Args:
        stats: Dictionary with counts (testcases, projects, tags)
        activities: List of recent activity items

    Returns:
        FastHTML page with dashboard
    """
    return PageLayout(
        Div(
            # Header
            Div(
                H2("Dashboard", cls="page-title"),
                cls="page-header-content",
            ),
            # Statistics row
            Div(
                StatisticsWidget(
                    title="Test Cases",
                    count=stats.get("testcases", 0),
                    icon="\U0001F4CB",  # 📋
                    color="blue",
                ),
                StatisticsWidget(
                    title="Projects",
                    count=stats.get("projects", 0),
                    icon="\U0001F4C1",  # 📁
                    color="green",
                ),
                StatisticsWidget(
                    title="Tags",
                    count=stats.get("tags", 0),
                    icon="\U0001F3F7",  # 🏷
                    color="orange",
                ),
                cls="stats-grid",
            ),
            # Main content grid
            Div(
                # Recent activity section
                Div(
                    Div(
                        H3("Recent Activity", cls="card-title"),
                        ActivityFeed(activities),
                        cls="card",
                    ),
                    cls="dashboard-main",
                ),
                # Sidebar with quick actions
                Div(
                    QuickActions(),
                    cls="dashboard-sidebar",
                ),
                cls="dashboard-content",
            ),
            cls="container container-wide",
        ),
        title="Dashboard - Test Case Management",
    )
