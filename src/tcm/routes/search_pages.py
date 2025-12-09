"""
Page routes for Search UI.

Provides global search across test cases, projects, and tags.
"""

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from tcm.database import get_async_session
from tcm.models.tag import Tag
from tcm.models.testcase import TestCase
from tcm.models.project import Project
from tcm.pages.search import SearchPage

router = APIRouter(tags=["search-pages"])


async def search_testcases(
    session: AsyncSession,
    query: str,
    status_filter: str = "",
) -> list[dict]:
    """
    Search test cases by title or description.

    Args:
        session: Database session
        query: Search query string
        status_filter: Optional status filter

    Returns:
        List of matching test case dicts
    """
    # Build query
    search_query = select(TestCase).where(
        or_(
            TestCase.title.ilike(f"%{query}%"),
            TestCase.description.ilike(f"%{query}%"),
            TestCase.steps.ilike(f"%{query}%"),
        )
    )

    # Apply status filter
    if status_filter:
        from tcm.models.testcase import TestCaseStatus
        try:
            status_enum = TestCaseStatus(status_filter)
            search_query = search_query.where(TestCase.status == status_enum)
        except ValueError:
            pass  # Invalid status, ignore filter

    search_query = search_query.order_by(TestCase.updated_at.desc()).limit(50)

    result = await session.execute(search_query)
    testcases = result.scalars().all()

    return [
        {
            "entity_type": "testcase",
            "entity_id": tc.id,
            "title": tc.title,
            "description": tc.description or "",
            "link": f"/testcases/{tc.id}",
            "status": tc.status.value,
            "priority": tc.priority.value,
            "tags": [
                {
                    "category": tag.category,
                    "value": tag.value,
                    "is_predefined": tag.is_predefined,
                }
                for tag in tc.tags
            ],
        }
        for tc in testcases
    ]


async def search_projects(
    session: AsyncSession,
    query: str,
    status_filter: str = "",
) -> list[dict]:
    """
    Search projects by name or description.

    Args:
        session: Database session
        query: Search query string
        status_filter: Optional status filter

    Returns:
        List of matching project dicts
    """
    # Build query
    search_query = select(Project).where(
        or_(
            Project.name.ilike(f"%{query}%"),
            Project.description.ilike(f"%{query}%"),
        )
    )

    # Apply status filter
    if status_filter:
        from tcm.models.project import ProjectStatus
        try:
            status_enum = ProjectStatus(status_filter)
            search_query = search_query.where(Project.status == status_enum)
        except ValueError:
            pass  # Invalid status, ignore filter

    search_query = search_query.order_by(Project.updated_at.desc()).limit(50)

    result = await session.execute(search_query)
    projects = result.scalars().all()

    return [
        {
            "entity_type": "project",
            "entity_id": proj.id,
            "title": proj.name,
            "description": proj.description or "",
            "link": f"/projects/{proj.id}",
            "status": proj.status.value,
            "testcase_count": len(proj.testcases),
            "start_date": proj.start_date.strftime("%Y-%m-%d") if proj.start_date else None,
            "end_date": proj.end_date.strftime("%Y-%m-%d") if proj.end_date else None,
        }
        for proj in projects
    ]


async def search_tags(
    session: AsyncSession,
    query: str,
    category_filter: str = "",
) -> list[dict]:
    """
    Search tags by category or value.

    Args:
        session: Database session
        query: Search query string
        category_filter: Optional category filter

    Returns:
        List of matching tag dicts
    """
    # Build query
    search_query = select(Tag).where(
        or_(
            Tag.category.ilike(f"%{query}%"),
            Tag.value.ilike(f"%{query}%"),
            Tag.description.ilike(f"%{query}%"),
        )
    )

    # Apply category filter
    if category_filter:
        search_query = search_query.where(Tag.category == category_filter)

    search_query = search_query.order_by(Tag.category, Tag.value).limit(50)

    result = await session.execute(search_query)
    tags = result.scalars().all()

    return [
        {
            "entity_type": "tag",
            "entity_id": tag.id,
            "title": f"{tag.category}: {tag.value}",
            "category": tag.category,
            "value": tag.value,
            "description": tag.description or "",
            "link": f"/tags/{tag.id}/edit",
            "is_predefined": tag.is_predefined,
            "testcase_count": len(tag.testcases),
        }
        for tag in tags
    ]


@router.get("/search", response_class=HTMLResponse)
async def search_page(
    request: Request,
    q: str = Query("", description="Search query"),
    entity_type: str = Query("", description="Entity type filter"),
    status: str = Query("", description="Status filter"),
    category: str = Query("", description="Category filter for tags"),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Render the search page with results.

    Args:
        request: FastAPI request object
        q: Search query
        entity_type: Entity type filter (testcase, project, tag)
        status: Status filter
        category: Category filter for tags
        session: Database session
    """
    from fasthtml.common import to_xml

    # If no query, show empty search page
    if not q:
        return HTMLResponse(
            content=to_xml(
                SearchPage(
                    query="",
                    entity_type=entity_type,
                    status_filter=status,
                    category_filter=category,
                    results={},
                    total_count=0,
                )
            )
        )

    # Perform searches based on entity type filter
    results = {}

    if not entity_type or entity_type == "testcase":
        results["testcase"] = await search_testcases(session, q, status)

    if not entity_type or entity_type == "project":
        results["project"] = await search_projects(session, q, status)

    if not entity_type or entity_type == "tag":
        results["tag"] = await search_tags(session, q, category)

    # Calculate total count
    total_count = sum(len(items) for items in results.values())

    return HTMLResponse(
        content=to_xml(
            SearchPage(
                query=q,
                entity_type=entity_type,
                status_filter=status,
                category_filter=category,
                results=results,
                total_count=total_count,
            )
        )
    )
