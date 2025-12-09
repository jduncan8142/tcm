"""
Page routes for TestCase management UI.

Provides HTML pages for browsing, creating, editing, and viewing test cases.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.status import HTTP_303_SEE_OTHER

from tcm.database import get_async_session
from tcm.models.testcase import TestCase, TestCaseStatus, TestCasePriority
from tcm.models.tag import Tag
from tcm.pages.testcases import (
    TestCasesListPage,
    CreateTestCasePage,
    EditTestCasePage,
    ViewTestCasePage,
)
from tcm.pages.testcases.edit import NotFoundPage as EditNotFoundPage
from tcm.pages.testcases.view import NotFoundPage as ViewNotFoundPage

router = APIRouter(prefix="/testcases", tags=["testcase-pages"])


async def get_all_tags(session: AsyncSession) -> list[dict]:
    """Get all tags for tag selection."""
    query = select(Tag).order_by(Tag.category, Tag.value)
    result = await session.execute(query)
    tags = result.scalars().all()
    return [
        {
            "id": tag.id,
            "category": tag.category,
            "value": tag.value,
            "description": tag.description,
            "is_predefined": tag.is_predefined,
        }
        for tag in tags
    ]


@router.get("", response_class=HTMLResponse)
async def testcases_list_page(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: str = Query("", description="Search query"),
    status: str = Query("", description="Filter by status"),
    priority: str = Query("", description="Filter by priority"),
    tag_id: int = Query(0, description="Filter by tag ID"),
    success: str = Query("", description="Success message"),
    error: str = Query("", description="Error message"),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Render the test cases list page.

    Args:
        request: FastAPI request object
        page: Page number (1-indexed)
        page_size: Number of items per page
        search: Search query for title/description
        status: Status filter
        priority: Priority filter
        tag_id: Tag ID filter
        success: Success message from redirect
        error: Error message from redirect
        session: Database session
    """
    from fasthtml.common import to_xml

    # Build query with eager loading
    query = select(TestCase).options(selectinload(TestCase.tags))

    # Apply search filter
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            or_(
                TestCase.title.ilike(search_pattern),
                TestCase.description.ilike(search_pattern),
            )
        )

    # Apply status filter
    if status:
        try:
            status_enum = TestCaseStatus(status)
            query = query.where(TestCase.status == status_enum)
        except ValueError:
            pass  # Invalid status, ignore filter

    # Apply priority filter
    if priority:
        try:
            priority_enum = TestCasePriority(priority)
            query = query.where(TestCase.priority == priority_enum)
        except ValueError:
            pass  # Invalid priority, ignore filter

    # Apply tag filter
    if tag_id:
        query = query.join(TestCase.tags).where(Tag.id == tag_id)

    # Get total count
    count_query = select(func.count()).select_from(TestCase)
    if search:
        search_pattern = f"%{search}%"
        count_query = count_query.where(
            or_(
                TestCase.title.ilike(search_pattern),
                TestCase.description.ilike(search_pattern),
            )
        )
    if status:
        try:
            status_enum = TestCaseStatus(status)
            count_query = count_query.where(TestCase.status == status_enum)
        except ValueError:
            pass
    if priority:
        try:
            priority_enum = TestCasePriority(priority)
            count_query = count_query.where(TestCase.priority == priority_enum)
        except ValueError:
            pass
    if tag_id:
        count_query = count_query.join(TestCase.tags).where(Tag.id == tag_id)

    total_result = await session.execute(count_query)
    total = total_result.scalar_one()

    # Get paginated results
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size).order_by(TestCase.id.desc())
    result = await session.execute(query)
    testcases = result.scalars().unique().all()

    # Convert to dict format
    testcases_data = [
        {
            "id": tc.id,
            "title": tc.title,
            "description": tc.description,
            "status": tc.status.value,
            "priority": tc.priority.value,
            "tags": [
                {
                    "id": tag.id,
                    "category": tag.category,
                    "value": tag.value,
                    "is_predefined": tag.is_predefined,
                }
                for tag in tc.tags
            ],
        }
        for tc in testcases
    ]

    # Get all tags for filter dropdown
    available_tags = await get_all_tags(session)

    return HTMLResponse(
        content=to_xml(
            TestCasesListPage(
                testcases=testcases_data,
                total=total,
                page=page,
                page_size=page_size,
                search=search,
                status_filter=status,
                priority_filter=priority,
                tag_filter=str(tag_id) if tag_id else "",
                available_tags=available_tags,
                success_message=success,
                error_message=error,
            )
        )
    )


@router.get("/new", response_class=HTMLResponse)
async def create_testcase_page(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Render the create test case page.

    Args:
        request: FastAPI request object
        session: Database session
    """
    from fasthtml.common import to_xml

    available_tags = await get_all_tags(session)

    return HTMLResponse(
        content=to_xml(
            CreateTestCasePage(available_tags=available_tags)
        )
    )


@router.post("/new", response_class=HTMLResponse)
async def create_testcase_submit(
    request: Request,
    title: Annotated[str, Form()],
    steps: Annotated[str, Form()],
    expected_results: Annotated[str, Form()],
    status: Annotated[str, Form()],
    priority: Annotated[str, Form()],
    description: Annotated[str, Form()] = "",
    preconditions: Annotated[str, Form()] = "",
    tag_ids: Annotated[list[str], Form()] = [],
    session: AsyncSession = Depends(get_async_session),
):
    """
    Handle create test case form submission.

    Args:
        request: FastAPI request object
        title: Test case title
        description: Test case description
        preconditions: Test case preconditions
        steps: Test case steps
        expected_results: Test case expected results
        status: Test case status
        priority: Test case priority
        tag_ids: List of tag IDs to associate
        session: Database session
    """
    from fasthtml.common import to_xml

    # Validate required fields
    if not title or not steps or not expected_results:
        available_tags = await get_all_tags(session)
        return HTMLResponse(
            content=to_xml(
                CreateTestCasePage(
                    available_tags=available_tags,
                    error_message="Title, steps, and expected results are required.",
                    form_data={
                        "title": title,
                        "description": description,
                        "preconditions": preconditions,
                        "steps": steps,
                        "expected_results": expected_results,
                        "status": status,
                        "priority": priority,
                        "tag_ids": [int(tid) for tid in tag_ids if tid],
                    },
                )
            )
        )

    # Validate status and priority
    try:
        status_enum = TestCaseStatus(status)
        priority_enum = TestCasePriority(priority)
    except ValueError as e:
        available_tags = await get_all_tags(session)
        return HTMLResponse(
            content=to_xml(
                CreateTestCasePage(
                    available_tags=available_tags,
                    error_message=f"Invalid status or priority: {e}",
                    form_data={
                        "title": title,
                        "description": description,
                        "preconditions": preconditions,
                        "steps": steps,
                        "expected_results": expected_results,
                        "status": status,
                        "priority": priority,
                        "tag_ids": [int(tid) for tid in tag_ids if tid],
                    },
                )
            )
        )

    # Create the test case
    testcase = TestCase(
        title=title,
        description=description if description else None,
        preconditions=preconditions if preconditions else None,
        steps=steps,
        expected_results=expected_results,
        status=status_enum,
        priority=priority_enum,
    )

    # Associate tags if provided
    if tag_ids:
        tag_id_ints = [int(tid) for tid in tag_ids if tid]
        if tag_id_ints:
            tag_query = select(Tag).where(Tag.id.in_(tag_id_ints))
            tag_result = await session.execute(tag_query)
            tags = tag_result.scalars().all()
            testcase.tags = list(tags)

    session.add(testcase)
    await session.commit()
    await session.refresh(testcase)

    return RedirectResponse(
        url=f"/testcases/{testcase.id}?success=Test case created successfully",
        status_code=HTTP_303_SEE_OTHER,
    )


@router.get("/{testcase_id}", response_class=HTMLResponse)
async def view_testcase_page(
    request: Request,
    testcase_id: int,
    success: str = Query("", description="Success message"),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Render the view test case details page.

    Args:
        request: FastAPI request object
        testcase_id: Test case ID
        success: Success message from redirect
        session: Database session
    """
    from fasthtml.common import to_xml

    # Get the test case with relationships
    query = (
        select(TestCase)
        .options(
            selectinload(TestCase.tags),
            selectinload(TestCase.projects),
        )
        .where(TestCase.id == testcase_id)
    )
    result = await session.execute(query)
    testcase = result.scalar_one_or_none()

    if not testcase:
        return HTMLResponse(
            content=to_xml(ViewNotFoundPage()),
            status_code=404,
        )

    # Convert to dict format
    testcase_data = {
        "id": testcase.id,
        "title": testcase.title,
        "description": testcase.description,
        "preconditions": testcase.preconditions,
        "steps": testcase.steps,
        "expected_results": testcase.expected_results,
        "actual_results": testcase.actual_results,
        "status": testcase.status.value,
        "priority": testcase.priority.value,
        "created_at": str(testcase.created_at),
        "updated_at": str(testcase.updated_at),
        "created_by": testcase.created_by,
        "updated_by": testcase.updated_by,
        "tags": [
            {
                "id": tag.id,
                "category": tag.category,
                "value": tag.value,
                "is_predefined": tag.is_predefined,
            }
            for tag in testcase.tags
        ],
        "projects": [
            {
                "id": project.id,
                "name": project.name,
            }
            for project in testcase.projects
        ],
    }

    return HTMLResponse(
        content=to_xml(
            ViewTestCasePage(testcase=testcase_data, success_message=success)
        )
    )


@router.get("/{testcase_id}/edit", response_class=HTMLResponse)
async def edit_testcase_page(
    request: Request,
    testcase_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Render the edit test case page.

    Args:
        request: FastAPI request object
        testcase_id: Test case ID
        session: Database session
    """
    from fasthtml.common import to_xml

    # Get the test case with tags
    query = (
        select(TestCase)
        .options(selectinload(TestCase.tags))
        .where(TestCase.id == testcase_id)
    )
    result = await session.execute(query)
    testcase = result.scalar_one_or_none()

    if not testcase:
        return HTMLResponse(
            content=to_xml(EditNotFoundPage()),
            status_code=404,
        )

    available_tags = await get_all_tags(session)

    # Convert to dict format
    testcase_data = {
        "id": testcase.id,
        "title": testcase.title,
        "description": testcase.description,
        "preconditions": testcase.preconditions,
        "steps": testcase.steps,
        "expected_results": testcase.expected_results,
        "status": testcase.status.value,
        "priority": testcase.priority.value,
        "tags": [
            {
                "id": tag.id,
                "category": tag.category,
                "value": tag.value,
                "is_predefined": tag.is_predefined,
            }
            for tag in testcase.tags
        ],
    }

    return HTMLResponse(
        content=to_xml(
            EditTestCasePage(
                testcase=testcase_data,
                available_tags=available_tags,
            )
        )
    )


@router.post("/{testcase_id}/edit", response_class=HTMLResponse)
async def edit_testcase_submit(
    request: Request,
    testcase_id: int,
    title: Annotated[str, Form()],
    steps: Annotated[str, Form()],
    expected_results: Annotated[str, Form()],
    status: Annotated[str, Form()],
    priority: Annotated[str, Form()],
    description: Annotated[str, Form()] = "",
    preconditions: Annotated[str, Form()] = "",
    tag_ids: Annotated[list[str], Form()] = [],
    session: AsyncSession = Depends(get_async_session),
):
    """
    Handle edit test case form submission.

    Args:
        request: FastAPI request object
        testcase_id: Test case ID
        title: Test case title
        description: Test case description
        preconditions: Test case preconditions
        steps: Test case steps
        expected_results: Test case expected results
        status: Test case status
        priority: Test case priority
        tag_ids: List of tag IDs to associate
        session: Database session
    """
    from fasthtml.common import to_xml

    # Get the test case
    query = (
        select(TestCase)
        .options(selectinload(TestCase.tags))
        .where(TestCase.id == testcase_id)
    )
    result = await session.execute(query)
    testcase = result.scalar_one_or_none()

    if not testcase:
        return HTMLResponse(
            content=to_xml(EditNotFoundPage()),
            status_code=404,
        )

    # Validate required fields
    if not title or not steps or not expected_results:
        available_tags = await get_all_tags(session)
        testcase_data = {
            "id": testcase.id,
            "title": title,
            "description": description,
            "preconditions": preconditions,
            "steps": steps,
            "expected_results": expected_results,
            "status": status,
            "priority": priority,
            "tags": [{"id": int(tid)} for tid in tag_ids if tid],
        }
        return HTMLResponse(
            content=to_xml(
                EditTestCasePage(
                    testcase=testcase_data,
                    available_tags=available_tags,
                    error_message="Title, steps, and expected results are required.",
                )
            )
        )

    # Validate status and priority
    try:
        status_enum = TestCaseStatus(status)
        priority_enum = TestCasePriority(priority)
    except ValueError as e:
        available_tags = await get_all_tags(session)
        testcase_data = {
            "id": testcase.id,
            "title": title,
            "description": description,
            "preconditions": preconditions,
            "steps": steps,
            "expected_results": expected_results,
            "status": status,
            "priority": priority,
            "tags": [{"id": int(tid)} for tid in tag_ids if tid],
        }
        return HTMLResponse(
            content=to_xml(
                EditTestCasePage(
                    testcase=testcase_data,
                    available_tags=available_tags,
                    error_message=f"Invalid status or priority: {e}",
                )
            )
        )

    # Update the test case
    testcase.title = title
    testcase.description = description if description else None
    testcase.preconditions = preconditions if preconditions else None
    testcase.steps = steps
    testcase.expected_results = expected_results
    testcase.status = status_enum
    testcase.priority = priority_enum

    # Update tags
    if tag_ids:
        tag_id_ints = [int(tid) for tid in tag_ids if tid]
        if tag_id_ints:
            tag_query = select(Tag).where(Tag.id.in_(tag_id_ints))
            tag_result = await session.execute(tag_query)
            tags = tag_result.scalars().all()
            testcase.tags = list(tags)
        else:
            testcase.tags = []
    else:
        testcase.tags = []

    await session.commit()

    return RedirectResponse(
        url=f"/testcases/{testcase_id}?success=Test case updated successfully",
        status_code=HTTP_303_SEE_OTHER,
    )
