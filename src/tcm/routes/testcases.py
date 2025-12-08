"""
API routes for TestCase management.

Provides CRUD operations for test cases with tag associations.
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from tcm.database import get_async_session
from tcm.models.testcase import TestCase, TestCaseStatus, TestCasePriority
from tcm.models.tag import Tag
from tcm.schemas.testcase import (
    TestCaseCreate,
    TestCaseUpdate,
    TestCaseResponse,
    TestCaseListResponse,
)

router = APIRouter(prefix="/testcases", tags=["testcases"])


@router.get("", response_model=TestCaseListResponse)
async def list_testcases(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    status: TestCaseStatus | None = Query(None, description="Filter by status"),
    priority: TestCasePriority | None = Query(None, description="Filter by priority"),
    tag_id: int | None = Query(None, description="Filter by tag ID"),
    session: AsyncSession = Depends(get_async_session),
):
    """
    List all test cases with pagination and optional filtering.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        status: Optional status filter
        priority: Optional priority filter
        tag_id: Optional tag ID filter
        session: Database session
    """
    # Build query with eager loading
    query = select(TestCase).options(selectinload(TestCase.tags))

    # Apply filters
    if status:
        query = query.where(TestCase.status == status)
    if priority:
        query = query.where(TestCase.priority == priority)
    if tag_id:
        query = query.join(TestCase.tags).where(Tag.id == tag_id)

    # Get total count
    count_query = select(func.count()).select_from(TestCase)
    if status:
        count_query = count_query.where(TestCase.status == status)
    if priority:
        count_query = count_query.where(TestCase.priority == priority)
    if tag_id:
        count_query = count_query.join(TestCase.tags).where(Tag.id == tag_id)

    total_result = await session.execute(count_query)
    total = total_result.scalar_one()

    # Get paginated results
    query = query.offset(skip).limit(limit).order_by(TestCase.id.desc())
    result = await session.execute(query)
    testcases = result.scalars().unique().all()

    return TestCaseListResponse(
        testcases=[TestCaseResponse.model_validate(tc) for tc in testcases],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get("/{testcase_id}", response_model=TestCaseResponse)
async def get_testcase(
    testcase_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Get a specific test case by ID.

    Args:
        testcase_id: Test case ID
        session: Database session
    """
    query = (
        select(TestCase)
        .options(selectinload(TestCase.tags))
        .where(TestCase.id == testcase_id)
    )
    result = await session.execute(query)
    testcase = result.scalar_one_or_none()

    if not testcase:
        raise HTTPException(
            status_code=404, detail=f"Test case with id {testcase_id} not found"
        )

    return TestCaseResponse.model_validate(testcase)


@router.post("", response_model=TestCaseResponse, status_code=201)
async def create_testcase(
    testcase_data: TestCaseCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Create a new test case.

    Args:
        testcase_data: Test case data to create
        session: Database session
    """
    # Extract tag_ids before creating the model
    tag_ids = testcase_data.tag_ids
    testcase_dict = testcase_data.model_dump(exclude={"tag_ids"})

    # Create test case
    testcase = TestCase(**testcase_dict)

    # Associate tags if provided
    if tag_ids:
        tag_query = select(Tag).where(Tag.id.in_(tag_ids))
        tag_result = await session.execute(tag_query)
        tags = tag_result.scalars().all()

        if len(tags) != len(tag_ids):
            found_ids = {tag.id for tag in tags}
            missing_ids = set(tag_ids) - found_ids
            raise HTTPException(
                status_code=400,
                detail=f"Tags with IDs {missing_ids} not found",
            )

        testcase.tags = list(tags)

    session.add(testcase)
    await session.commit()
    await session.refresh(testcase)

    # Reload with tags
    query = (
        select(TestCase)
        .options(selectinload(TestCase.tags))
        .where(TestCase.id == testcase.id)
    )
    result = await session.execute(query)
    testcase = result.scalar_one()

    return TestCaseResponse.model_validate(testcase)


@router.patch("/{testcase_id}", response_model=TestCaseResponse)
async def update_testcase(
    testcase_id: int,
    testcase_data: TestCaseUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Update an existing test case.

    Args:
        testcase_id: Test case ID
        testcase_data: Test case data to update
        session: Database session
    """
    # Get existing test case
    query = (
        select(TestCase)
        .options(selectinload(TestCase.tags))
        .where(TestCase.id == testcase_id)
    )
    result = await session.execute(query)
    testcase = result.scalar_one_or_none()

    if not testcase:
        raise HTTPException(
            status_code=404, detail=f"Test case with id {testcase_id} not found"
        )

    # Extract and handle tag_ids separately
    update_data = testcase_data.model_dump(exclude_unset=True)
    tag_ids = update_data.pop("tag_ids", None)

    # Update basic fields
    for field, value in update_data.items():
        setattr(testcase, field, value)

    # Update tags if provided
    if tag_ids is not None:
        tag_query = select(Tag).where(Tag.id.in_(tag_ids))
        tag_result = await session.execute(tag_query)
        tags = tag_result.scalars().all()

        if len(tags) != len(tag_ids):
            found_ids = {tag.id for tag in tags}
            missing_ids = set(tag_ids) - found_ids
            raise HTTPException(
                status_code=400,
                detail=f"Tags with IDs {missing_ids} not found",
            )

        testcase.tags = list(tags)

    await session.commit()
    await session.refresh(testcase)

    return TestCaseResponse.model_validate(testcase)


@router.delete("/{testcase_id}", status_code=204)
async def delete_testcase(
    testcase_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Delete a test case.

    Args:
        testcase_id: Test case ID
        session: Database session
    """
    # Get existing test case
    query = select(TestCase).where(TestCase.id == testcase_id)
    result = await session.execute(query)
    testcase = result.scalar_one_or_none()

    if not testcase:
        raise HTTPException(
            status_code=404, detail=f"Test case with id {testcase_id} not found"
        )

    await session.delete(testcase)
    await session.commit()


@router.post("/{testcase_id}/tags/{tag_id}", response_model=TestCaseResponse)
async def add_tag_to_testcase(
    testcase_id: int,
    tag_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Add a tag to a test case.

    Args:
        testcase_id: Test case ID
        tag_id: Tag ID to add
        session: Database session
    """
    # Get test case
    tc_query = (
        select(TestCase)
        .options(selectinload(TestCase.tags))
        .where(TestCase.id == testcase_id)
    )
    tc_result = await session.execute(tc_query)
    testcase = tc_result.scalar_one_or_none()

    if not testcase:
        raise HTTPException(
            status_code=404, detail=f"Test case with id {testcase_id} not found"
        )

    # Get tag
    tag_query = select(Tag).where(Tag.id == tag_id)
    tag_result = await session.execute(tag_query)
    tag = tag_result.scalar_one_or_none()

    if not tag:
        raise HTTPException(status_code=404, detail=f"Tag with id {tag_id} not found")

    # Check if tag is already associated
    if tag in testcase.tags:
        raise HTTPException(
            status_code=400,
            detail=f"Tag {tag_id} is already associated with test case {testcase_id}",
        )

    # Add tag
    testcase.tags.append(tag)
    await session.commit()
    await session.refresh(testcase)

    return TestCaseResponse.model_validate(testcase)


@router.delete("/{testcase_id}/tags/{tag_id}", response_model=TestCaseResponse)
async def remove_tag_from_testcase(
    testcase_id: int,
    tag_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Remove a tag from a test case.

    Args:
        testcase_id: Test case ID
        tag_id: Tag ID to remove
        session: Database session
    """
    # Get test case
    tc_query = (
        select(TestCase)
        .options(selectinload(TestCase.tags))
        .where(TestCase.id == testcase_id)
    )
    tc_result = await session.execute(tc_query)
    testcase = tc_result.scalar_one_or_none()

    if not testcase:
        raise HTTPException(
            status_code=404, detail=f"Test case with id {testcase_id} not found"
        )

    # Find and remove tag
    tag_to_remove = None
    for tag in testcase.tags:
        if tag.id == tag_id:
            tag_to_remove = tag
            break

    if not tag_to_remove:
        raise HTTPException(
            status_code=404,
            detail=f"Tag {tag_id} is not associated with test case {testcase_id}",
        )

    testcase.tags.remove(tag_to_remove)
    await session.commit()
    await session.refresh(testcase)

    return TestCaseResponse.model_validate(testcase)
