"""
API routes for Project management.

Provides CRUD operations for projects with test case associations.
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from tcm.database import get_async_session
from tcm.models.project import Project, ProjectStatus
from tcm.models.testcase import TestCase
from tcm.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectListResponse,
)
from tcm.schemas.testcase import TestCaseResponse

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=ProjectListResponse)
async def list_projects(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    status: ProjectStatus | None = Query(None, description="Filter by status"),
    session: AsyncSession = Depends(get_async_session),
):
    """
    List all projects with pagination and optional filtering.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        status: Optional status filter
        session: Database session
    """
    # Build query
    query = select(Project)

    # Apply filters
    if status:
        query = query.where(Project.status == status)

    # Get total count
    count_query = select(func.count()).select_from(Project)
    if status:
        count_query = count_query.where(Project.status == status)

    total_result = await session.execute(count_query)
    total = total_result.scalar_one()

    # Get paginated results
    query = query.offset(skip).limit(limit).order_by(Project.id.desc())
    result = await session.execute(query)
    projects = result.scalars().all()

    return ProjectListResponse(
        projects=[ProjectResponse.model_validate(proj) for proj in projects],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Get a specific project by ID.

    Args:
        project_id: Project ID
        session: Database session
    """
    query = select(Project).where(Project.id == project_id)
    result = await session.execute(query)
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=404, detail=f"Project with id {project_id} not found"
        )

    return ProjectResponse.model_validate(project)


@router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(
    project_data: ProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Create a new project.

    Args:
        project_data: Project data to create
        session: Database session
    """
    # Check if project with same name already exists
    name_query = select(Project).where(Project.name == project_data.name)
    name_result = await session.execute(name_query)
    existing_project = name_result.scalar_one_or_none()

    if existing_project:
        raise HTTPException(
            status_code=400,
            detail=f"Project with name '{project_data.name}' already exists",
        )

    # Extract testcase_ids before creating the model
    testcase_ids = project_data.testcase_ids
    project_dict = project_data.model_dump(exclude={"testcase_ids"})

    # Create project
    project = Project(**project_dict)

    # Associate test cases if provided
    if testcase_ids:
        tc_query = select(TestCase).where(TestCase.id.in_(testcase_ids))
        tc_result = await session.execute(tc_query)
        testcases = tc_result.scalars().all()

        if len(testcases) != len(testcase_ids):
            found_ids = {tc.id for tc in testcases}
            missing_ids = set(testcase_ids) - found_ids
            raise HTTPException(
                status_code=400,
                detail=f"Test cases with IDs {missing_ids} not found",
            )

        project.testcases = list(testcases)

    session.add(project)
    await session.commit()
    await session.refresh(project)

    return ProjectResponse.model_validate(project)


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Update an existing project.

    Args:
        project_id: Project ID
        project_data: Project data to update
        session: Database session
    """
    # Get existing project
    query = (
        select(Project)
        .options(selectinload(Project.testcases))
        .where(Project.id == project_id)
    )
    result = await session.execute(query)
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=404, detail=f"Project with id {project_id} not found"
        )

    # Extract and handle testcase_ids separately
    update_data = project_data.model_dump(exclude_unset=True)
    testcase_ids = update_data.pop("testcase_ids", None)

    # Check for name uniqueness if name is being updated
    if "name" in update_data:
        name_query = select(Project).where(
            Project.name == update_data["name"],
            Project.id != project_id,
        )
        name_result = await session.execute(name_query)
        if name_result.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail=f"Project with name '{update_data['name']}' already exists",
            )

    # Update basic fields
    for field, value in update_data.items():
        setattr(project, field, value)

    # Update test cases if provided
    if testcase_ids is not None:
        tc_query = select(TestCase).where(TestCase.id.in_(testcase_ids))
        tc_result = await session.execute(tc_query)
        testcases = tc_result.scalars().all()

        if len(testcases) != len(testcase_ids):
            found_ids = {tc.id for tc in testcases}
            missing_ids = set(testcase_ids) - found_ids
            raise HTTPException(
                status_code=400,
                detail=f"Test cases with IDs {missing_ids} not found",
            )

        project.testcases = list(testcases)

    await session.commit()
    await session.refresh(project)

    return ProjectResponse.model_validate(project)


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Delete a project.

    Args:
        project_id: Project ID
        session: Database session
    """
    # Get existing project
    query = select(Project).where(Project.id == project_id)
    result = await session.execute(query)
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=404, detail=f"Project with id {project_id} not found"
        )

    await session.delete(project)
    await session.commit()


@router.get("/{project_id}/testcases", response_model=list[TestCaseResponse])
async def get_project_testcases(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Get all test cases associated with a project.

    Args:
        project_id: Project ID
        session: Database session
    """
    # Get project with test cases
    query = (
        select(Project)
        .options(selectinload(Project.testcases).selectinload(TestCase.tags))
        .where(Project.id == project_id)
    )
    result = await session.execute(query)
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=404, detail=f"Project with id {project_id} not found"
        )

    return [TestCaseResponse.model_validate(tc) for tc in project.testcases]


@router.post("/{project_id}/testcases/{testcase_id}", response_model=ProjectResponse)
async def add_testcase_to_project(
    project_id: int,
    testcase_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Add a test case to a project.

    Args:
        project_id: Project ID
        testcase_id: Test case ID to add
        session: Database session
    """
    # Get project
    proj_query = (
        select(Project)
        .options(selectinload(Project.testcases))
        .where(Project.id == project_id)
    )
    proj_result = await session.execute(proj_query)
    project = proj_result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=404, detail=f"Project with id {project_id} not found"
        )

    # Get test case
    tc_query = select(TestCase).where(TestCase.id == testcase_id)
    tc_result = await session.execute(tc_query)
    testcase = tc_result.scalar_one_or_none()

    if not testcase:
        raise HTTPException(
            status_code=404, detail=f"Test case with id {testcase_id} not found"
        )

    # Check if test case is already associated
    if testcase in project.testcases:
        raise HTTPException(
            status_code=400,
            detail=f"Test case {testcase_id} is already associated with project {project_id}",
        )

    # Add test case
    project.testcases.append(testcase)
    await session.commit()
    await session.refresh(project)

    return ProjectResponse.model_validate(project)


@router.delete("/{project_id}/testcases/{testcase_id}", response_model=ProjectResponse)
async def remove_testcase_from_project(
    project_id: int,
    testcase_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Remove a test case from a project.

    Args:
        project_id: Project ID
        testcase_id: Test case ID to remove
        session: Database session
    """
    # Get project
    proj_query = (
        select(Project)
        .options(selectinload(Project.testcases))
        .where(Project.id == project_id)
    )
    proj_result = await session.execute(proj_query)
    project = proj_result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=404, detail=f"Project with id {project_id} not found"
        )

    # Find and remove test case
    tc_to_remove = None
    for tc in project.testcases:
        if tc.id == testcase_id:
            tc_to_remove = tc
            break

    if not tc_to_remove:
        raise HTTPException(
            status_code=404,
            detail=f"Test case {testcase_id} is not associated with project {project_id}",
        )

    project.testcases.remove(tc_to_remove)
    await session.commit()
    await session.refresh(project)

    return ProjectResponse.model_validate(project)
