"""
Page routes for Dashboard UI.

Provides the dashboard page with statistics and recent activity.
"""

from datetime import datetime, timedelta, UTC
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from tcm.database import get_async_session
from tcm.models.tag import Tag
from tcm.models.testcase import TestCase
from tcm.models.project import Project
from tcm.pages.dashboard import DashboardPage

router = APIRouter(tags=["dashboard-pages"])


def format_relative_time(dt: datetime) -> str:
    """
    Format datetime as relative time string.

    Args:
        dt: Datetime to format

    Returns:
        Human-readable relative time string
    """
    now = datetime.now(UTC)

    # Ensure dt is timezone-aware
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)

    delta = now - dt

    if delta < timedelta(minutes=1):
        return "just now"
    elif delta < timedelta(hours=1):
        minutes = int(delta.total_seconds() / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif delta < timedelta(days=1):
        hours = int(delta.total_seconds() / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif delta < timedelta(days=7):
        days = delta.days
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif delta < timedelta(days=30):
        weeks = delta.days // 7
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    else:
        months = delta.days // 30
        return f"{months} month{'s' if months != 1 else ''} ago"


async def get_statistics(session: AsyncSession) -> dict:
    """
    Get entity counts for statistics widgets.

    Args:
        session: Database session

    Returns:
        Dictionary with entity counts
    """
    # Count test cases
    testcases_query = select(func.count(TestCase.id))
    testcases_result = await session.execute(testcases_query)
    testcases_count = testcases_result.scalar_one()

    # Count projects
    projects_query = select(func.count(Project.id))
    projects_result = await session.execute(projects_query)
    projects_count = projects_result.scalar_one()

    # Count tags
    tags_query = select(func.count(Tag.id))
    tags_result = await session.execute(tags_query)
    tags_count = tags_result.scalar_one()

    return {
        "testcases": testcases_count,
        "projects": projects_count,
        "tags": tags_count,
    }


async def get_recent_activity(session: AsyncSession, limit: int = 10) -> list[dict]:
    """
    Get recent activity across all entity types.

    Args:
        session: Database session
        limit: Maximum number of items to return

    Returns:
        List of activity dicts sorted by timestamp (newest first)
    """
    activities = []

    # Get recent test cases
    testcases_query = (
        select(TestCase)
        .order_by(desc(TestCase.updated_at))
        .limit(limit)
    )
    testcases_result = await session.execute(testcases_query)
    testcases = testcases_result.scalars().all()

    for tc in testcases:
        # Determine if it was created or updated
        is_new = (tc.updated_at - tc.created_at).total_seconds() < 60
        action = "created" if is_new else "updated"

        activities.append({
            "entity_type": "testcase",
            "entity_id": tc.id,
            "title": tc.title,
            "action": action,
            "timestamp": format_relative_time(tc.updated_at),
            "raw_timestamp": tc.updated_at,
            "link": f"/testcases/{tc.id}",
            "status": tc.status.value,
            "tags": [
                {
                    "category": tag.category,
                    "value": tag.value,
                    "is_predefined": tag.is_predefined,
                }
                for tag in tc.tags
            ],
        })

    # Get recent projects
    projects_query = (
        select(Project)
        .order_by(desc(Project.updated_at))
        .limit(limit)
    )
    projects_result = await session.execute(projects_query)
    projects = projects_result.scalars().all()

    for proj in projects:
        is_new = (proj.updated_at - proj.created_at).total_seconds() < 60
        action = "created" if is_new else "updated"

        activities.append({
            "entity_type": "project",
            "entity_id": proj.id,
            "title": proj.name,
            "action": action,
            "timestamp": format_relative_time(proj.updated_at),
            "raw_timestamp": proj.updated_at,
            "link": f"/projects/{proj.id}",
            "status": proj.status.value,
            "tags": [],
        })

    # Get recent tags
    tags_query = (
        select(Tag)
        .order_by(desc(Tag.updated_at))
        .limit(limit)
    )
    tags_result = await session.execute(tags_query)
    tags = tags_result.scalars().all()

    for tag in tags:
        is_new = (tag.updated_at - tag.created_at).total_seconds() < 60
        action = "created" if is_new else "updated"

        activities.append({
            "entity_type": "tag",
            "entity_id": tag.id,
            "title": f"{tag.category}: {tag.value}",
            "action": action,
            "timestamp": format_relative_time(tag.updated_at),
            "raw_timestamp": tag.updated_at,
            "link": f"/tags/{tag.id}/edit",
            "status": "",
            "tags": [],
        })

    # Sort all activities by timestamp and limit
    activities.sort(key=lambda x: x["raw_timestamp"], reverse=True)

    # Remove raw_timestamp from output
    for activity in activities:
        del activity["raw_timestamp"]

    return activities[:limit]


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Render the dashboard page with statistics and recent activity.

    Args:
        request: FastAPI request object
        session: Database session
    """
    from fasthtml.common import to_xml

    # Get statistics
    stats = await get_statistics(session)

    # Get recent activity
    activities = await get_recent_activity(session, limit=10)

    return HTMLResponse(
        content=to_xml(
            DashboardPage(
                stats=stats,
                activities=activities,
            )
        )
    )
