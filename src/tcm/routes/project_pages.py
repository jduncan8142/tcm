"""
Page routes for Project management UI.

Provides HTML pages for browsing, creating, editing, and viewing projects.
"""

from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.status import HTTP_303_SEE_OTHER

from tcm.database import get_async_session
from tcm.models.project import Project, ProjectStatus
from tcm.models.testcase import TestCase
from tcm.pages.projects import ProjectsListPage, CreateProjectPage, EditProjectPage, ViewProjectPage
from tcm.pages.projects.edit import NotFoundPage

router = APIRouter(prefix="/projects", tags=["project-pages"])


@router.get("", response_class=HTMLResponse)
async def projects_list_page(
    request: Request,
    status: str = Query("", description="Filter by status"),
    success: str = Query("", description="Success message"),
    error: str = Query("", description="Error message"),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Render the projects list page.

    Args:
        request: FastAPI request object
        status: Optional status filter
        success: Success message from redirect
        error: Error message from redirect
        session: Database session
    """
    from fasthtml.common import to_xml

    # Build query
    query = select(Project).options(selectinload(Project.testcases))
    if status:
        query = query.where(Project.status == status)
    query = query.order_by(Project.id.desc())

    result = await session.execute(query)
    projects = result.scalars().all()

    # Convert to dict format
    projects_data = [
        {
            "id": proj.id,
            "name": proj.name,
            "description": proj.description,
            "status": proj.status.value if hasattr(proj.status, 'value') else proj.status,
            "start_date": proj.start_date.isoformat() if proj.start_date else None,
            "end_date": proj.end_date.isoformat() if proj.end_date else None,
            "testcase_ids": [tc.id for tc in proj.testcases],
        }
        for proj in projects
    ]

    # Get all statuses for filter dropdown
    statuses = [s.value for s in ProjectStatus]

    return HTMLResponse(
        content=to_xml(
            ProjectsListPage(
                projects=projects_data,
                statuses=statuses,
                current_status=status,
                success_message=success,
                error_message=error,
            )
        )
    )


@router.get("/new", response_class=HTMLResponse)
async def create_project_page(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Render the create project page.

    Args:
        request: FastAPI request object
        session: Database session
    """
    from fasthtml.common import to_xml

    return HTMLResponse(
        content=to_xml(CreateProjectPage())
    )


@router.post("/new", response_class=HTMLResponse)
async def create_project_submit(
    request: Request,
    name: Annotated[str, Form()],
    description: Annotated[str, Form()] = "",
    status: Annotated[str, Form()] = "planning",
    start_date: Annotated[str, Form()] = "",
    end_date: Annotated[str, Form()] = "",
    session: AsyncSession = Depends(get_async_session),
):
    """
    Handle create project form submission.

    Args:
        request: FastAPI request object
        name: Project name
        description: Project description (optional)
        status: Project status
        start_date: Project start date (optional)
        end_date: Project end date (optional)
        session: Database session
    """
    from fasthtml.common import to_xml

    # Validate required fields
    if not name:
        return HTMLResponse(
            content=to_xml(
                CreateProjectPage(
                    error_message="Project name is required.",
                    form_data={
                        "name": name,
                        "description": description,
                        "status": status,
                        "start_date": start_date,
                        "end_date": end_date,
                    },
                )
            )
        )

    # Check for duplicate name
    duplicate_query = select(Project).where(Project.name == name)
    duplicate_result = await session.execute(duplicate_query)
    if duplicate_result.scalar_one_or_none():
        return HTMLResponse(
            content=to_xml(
                CreateProjectPage(
                    error_message=f"A project with name '{name}' already exists.",
                    form_data={
                        "name": name,
                        "description": description,
                        "status": status,
                        "start_date": start_date,
                        "end_date": end_date,
                    },
                )
            )
        )

    # Parse dates
    start_date_parsed = None
    end_date_parsed = None
    try:
        if start_date:
            start_date_parsed = datetime.fromisoformat(start_date)
        if end_date:
            end_date_parsed = datetime.fromisoformat(end_date)

        # Validate date range
        if start_date_parsed and end_date_parsed and end_date_parsed < start_date_parsed:
            return HTMLResponse(
                content=to_xml(
                    CreateProjectPage(
                        error_message="End date must be after start date.",
                        form_data={
                            "name": name,
                            "description": description,
                            "status": status,
                            "start_date": start_date,
                            "end_date": end_date,
                        },
                    )
                )
            )
    except ValueError:
        return HTMLResponse(
            content=to_xml(
                CreateProjectPage(
                    error_message="Invalid date format.",
                    form_data={
                        "name": name,
                        "description": description,
                        "status": status,
                        "start_date": start_date,
                        "end_date": end_date,
                    },
                )
            )
        )

    # Create the project
    project = Project(
        name=name,
        description=description if description else None,
        status=ProjectStatus(status),
        start_date=start_date_parsed,
        end_date=end_date_parsed,
    )
    session.add(project)
    await session.commit()
    await session.refresh(project)

    return RedirectResponse(
        url=f"/projects/{project.id}?success=Project created successfully",
        status_code=HTTP_303_SEE_OTHER,
    )


@router.get("/{project_id}", response_class=HTMLResponse)
async def view_project_page(
    request: Request,
    project_id: int,
    success: str = Query("", description="Success message"),
    error: str = Query("", description="Error message"),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Render the project details view page.

    Args:
        request: FastAPI request object
        project_id: Project ID
        success: Success message from redirect
        error: Error message from redirect
        session: Database session
    """
    from fasthtml.common import to_xml

    # Get the project with test cases
    query = (
        select(Project)
        .options(selectinload(Project.testcases).selectinload(TestCase.tags))
        .where(Project.id == project_id)
    )
    result = await session.execute(query)
    project = result.scalar_one_or_none()

    if not project:
        return HTMLResponse(
            content=to_xml(NotFoundPage()),
            status_code=404,
        )

    # Get all available test cases
    all_testcases_query = select(TestCase)
    all_testcases_result = await session.execute(all_testcases_query)
    all_testcases = all_testcases_result.scalars().all()

    project_data = {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "status": project.status.value if hasattr(project.status, 'value') else project.status,
        "start_date": project.start_date.isoformat() if project.start_date else None,
        "end_date": project.end_date.isoformat() if project.end_date else None,
    }

    testcases_data = [
        {
            "id": tc.id,
            "title": tc.title,
            "status": tc.status.value if hasattr(tc.status, 'value') else tc.status,
            "priority": tc.priority.value if hasattr(tc.priority, 'value') else tc.priority,
        }
        for tc in project.testcases
    ]

    available_testcases_data = [
        {
            "id": tc.id,
            "title": tc.title,
        }
        for tc in all_testcases
    ]

    return HTMLResponse(
        content=to_xml(
            ViewProjectPage(
                project=project_data,
                testcases=testcases_data,
                available_testcases=available_testcases_data,
                success_message=success,
                error_message=error,
            )
        )
    )


@router.get("/{project_id}/edit", response_class=HTMLResponse)
async def edit_project_page(
    request: Request,
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Render the edit project page.

    Args:
        request: FastAPI request object
        project_id: Project ID
        session: Database session
    """
    from fasthtml.common import to_xml

    # Get the project
    query = select(Project).where(Project.id == project_id)
    result = await session.execute(query)
    project = result.scalar_one_or_none()

    if not project:
        return HTMLResponse(
            content=to_xml(NotFoundPage()),
            status_code=404,
        )

    project_data = {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "status": project.status.value if hasattr(project.status, 'value') else project.status,
        "start_date": project.start_date.isoformat() if project.start_date else None,
        "end_date": project.end_date.isoformat() if project.end_date else None,
    }

    return HTMLResponse(
        content=to_xml(
            EditProjectPage(project=project_data)
        )
    )


@router.post("/{project_id}/edit", response_class=HTMLResponse)
async def edit_project_submit(
    request: Request,
    project_id: int,
    name: Annotated[str, Form()],
    description: Annotated[str, Form()] = "",
    status: Annotated[str, Form()] = "planning",
    start_date: Annotated[str, Form()] = "",
    end_date: Annotated[str, Form()] = "",
    session: AsyncSession = Depends(get_async_session),
):
    """
    Handle edit project form submission.

    Args:
        request: FastAPI request object
        project_id: Project ID
        name: Project name
        description: Project description (optional)
        status: Project status
        start_date: Project start date (optional)
        end_date: Project end date (optional)
        session: Database session
    """
    from fasthtml.common import to_xml

    # Get the project
    query = select(Project).where(Project.id == project_id)
    result = await session.execute(query)
    project = result.scalar_one_or_none()

    if not project:
        return HTMLResponse(
            content=to_xml(NotFoundPage()),
            status_code=404,
        )

    # Validate required fields
    if not name:
        project_data = {
            "id": project.id,
            "name": name,
            "description": description,
            "status": status,
            "start_date": start_date,
            "end_date": end_date,
        }
        return HTMLResponse(
            content=to_xml(
                EditProjectPage(
                    project=project_data,
                    error_message="Project name is required.",
                )
            )
        )

    # Check for duplicate name (excluding current project)
    duplicate_query = select(Project).where(
        Project.name == name,
        Project.id != project_id,
    )
    duplicate_result = await session.execute(duplicate_query)
    if duplicate_result.scalar_one_or_none():
        project_data = {
            "id": project.id,
            "name": name,
            "description": description,
            "status": status,
            "start_date": start_date,
            "end_date": end_date,
        }
        return HTMLResponse(
            content=to_xml(
                EditProjectPage(
                    project=project_data,
                    error_message=f"A project with name '{name}' already exists.",
                )
            )
        )

    # Parse dates
    start_date_parsed = None
    end_date_parsed = None
    try:
        if start_date:
            start_date_parsed = datetime.fromisoformat(start_date)
        if end_date:
            end_date_parsed = datetime.fromisoformat(end_date)

        # Validate date range
        if start_date_parsed and end_date_parsed and end_date_parsed < start_date_parsed:
            project_data = {
                "id": project.id,
                "name": name,
                "description": description,
                "status": status,
                "start_date": start_date,
                "end_date": end_date,
            }
            return HTMLResponse(
                content=to_xml(
                    EditProjectPage(
                        project=project_data,
                        error_message="End date must be after start date.",
                    )
                )
            )
    except ValueError:
        project_data = {
            "id": project.id,
            "name": name,
            "description": description,
            "status": status,
            "start_date": start_date,
            "end_date": end_date,
        }
        return HTMLResponse(
            content=to_xml(
                EditProjectPage(
                    project=project_data,
                    error_message="Invalid date format.",
                )
            )
        )

    # Update the project
    project.name = name
    project.description = description if description else None
    project.status = ProjectStatus(status)
    project.start_date = start_date_parsed
    project.end_date = end_date_parsed

    await session.commit()

    return RedirectResponse(
        url=f"/projects/{project_id}?success=Project updated successfully",
        status_code=HTTP_303_SEE_OTHER,
    )
