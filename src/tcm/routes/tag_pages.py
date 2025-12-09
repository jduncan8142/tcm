"""
Page routes for Tag management UI.

Provides HTML pages for browsing, creating, and editing tags.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_303_SEE_OTHER

from tcm.database import get_async_session
from tcm.models.tag import Tag
from tcm.pages.tags import TagsListPage, CreateTagPage, EditTagPage
from tcm.pages.tags.edit import NotFoundPage

router = APIRouter(prefix="/tags", tags=["tag-pages"])


async def get_all_categories(session: AsyncSession) -> list[str]:
    """Get all unique tag categories."""
    query = select(Tag.category).distinct().order_by(Tag.category)
    result = await session.execute(query)
    return list(result.scalars().all())


@router.get("", response_class=HTMLResponse)
async def tags_list_page(
    request: Request,
    category: str = Query("", description="Filter by category"),
    success: str = Query("", description="Success message"),
    error: str = Query("", description="Error message"),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Render the tags list page.

    Args:
        request: FastAPI request object
        category: Optional category filter
        success: Success message from redirect
        error: Error message from redirect
        session: Database session
    """
    from fasthtml.common import to_xml

    # Build query
    query = select(Tag)
    if category:
        query = query.where(Tag.category == category)
    query = query.order_by(Tag.category, Tag.value)

    result = await session.execute(query)
    tags = result.scalars().all()

    # Convert to dict format
    tags_data = [
        {
            "id": tag.id,
            "category": tag.category,
            "value": tag.value,
            "description": tag.description,
            "is_predefined": tag.is_predefined,
        }
        for tag in tags
    ]

    # Get all categories for filter dropdown
    categories = await get_all_categories(session)

    return HTMLResponse(
        content=to_xml(
            TagsListPage(
                tags=tags_data,
                categories=categories,
                current_category=category,
                success_message=success,
                error_message=error,
                grouped=not category,  # Only group when not filtering
            )
        )
    )


@router.get("/new", response_class=HTMLResponse)
async def create_tag_page(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Render the create tag page.

    Args:
        request: FastAPI request object
        session: Database session
    """
    from fasthtml.common import to_xml

    categories = await get_all_categories(session)

    return HTMLResponse(
        content=to_xml(
            CreateTagPage(categories=categories)
        )
    )


@router.post("/new", response_class=HTMLResponse)
async def create_tag_submit(
    request: Request,
    category: Annotated[str, Form()],
    value: Annotated[str, Form()],
    description: Annotated[str, Form()] = "",
    is_predefined: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Handle create tag form submission.

    Args:
        request: FastAPI request object
        category: Tag category
        value: Tag value
        description: Tag description (optional)
        is_predefined: Whether tag is predefined (checkbox value)
        session: Database session
    """
    from fasthtml.common import to_xml

    # Validate required fields
    if not category or not value:
        categories = await get_all_categories(session)
        return HTMLResponse(
            content=to_xml(
                CreateTagPage(
                    categories=categories,
                    error_message="Category and value are required.",
                    form_data={
                        "category": category,
                        "value": value,
                        "description": description,
                        "is_predefined": is_predefined == "on",
                    },
                )
            )
        )

    # Check for duplicate
    duplicate_query = select(Tag).where(
        Tag.category == category,
        Tag.value == value,
    )
    duplicate_result = await session.execute(duplicate_query)
    if duplicate_result.scalar_one_or_none():
        categories = await get_all_categories(session)
        return HTMLResponse(
            content=to_xml(
                CreateTagPage(
                    categories=categories,
                    error_message=f"A tag with category '{category}' and value '{value}' already exists.",
                    form_data={
                        "category": category,
                        "value": value,
                        "description": description,
                        "is_predefined": is_predefined == "on",
                    },
                )
            )
        )

    # Create the tag
    tag = Tag(
        category=category,
        value=value,
        description=description if description else None,
        is_predefined=is_predefined == "on",
    )
    session.add(tag)
    await session.commit()

    return RedirectResponse(
        url="/tags?success=Tag created successfully",
        status_code=HTTP_303_SEE_OTHER,
    )


@router.get("/{tag_id}/edit", response_class=HTMLResponse)
async def edit_tag_page(
    request: Request,
    tag_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Render the edit tag page.

    Args:
        request: FastAPI request object
        tag_id: Tag ID
        session: Database session
    """
    from fasthtml.common import to_xml

    # Get the tag
    query = select(Tag).where(Tag.id == tag_id)
    result = await session.execute(query)
    tag = result.scalar_one_or_none()

    if not tag:
        return HTMLResponse(
            content=to_xml(NotFoundPage()),
            status_code=404,
        )

    categories = await get_all_categories(session)

    tag_data = {
        "id": tag.id,
        "category": tag.category,
        "value": tag.value,
        "description": tag.description,
        "is_predefined": tag.is_predefined,
    }

    return HTMLResponse(
        content=to_xml(
            EditTagPage(tag=tag_data, categories=categories)
        )
    )


@router.post("/{tag_id}/edit", response_class=HTMLResponse)
async def edit_tag_submit(
    request: Request,
    tag_id: int,
    category: Annotated[str, Form()],
    value: Annotated[str, Form()],
    description: Annotated[str, Form()] = "",
    is_predefined: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Handle edit tag form submission.

    Args:
        request: FastAPI request object
        tag_id: Tag ID
        category: Tag category
        value: Tag value
        description: Tag description (optional)
        is_predefined: Whether tag is predefined (checkbox value)
        session: Database session
    """
    from fasthtml.common import to_xml

    # Get the tag
    query = select(Tag).where(Tag.id == tag_id)
    result = await session.execute(query)
    tag = result.scalar_one_or_none()

    if not tag:
        return HTMLResponse(
            content=to_xml(NotFoundPage()),
            status_code=404,
        )

    # Validate required fields
    if not category or not value:
        categories = await get_all_categories(session)
        tag_data = {
            "id": tag.id,
            "category": category,
            "value": value,
            "description": description,
            "is_predefined": is_predefined == "on",
        }
        return HTMLResponse(
            content=to_xml(
                EditTagPage(
                    tag=tag_data,
                    categories=categories,
                    error_message="Category and value are required.",
                )
            )
        )

    # Check for duplicate (excluding current tag)
    duplicate_query = select(Tag).where(
        Tag.category == category,
        Tag.value == value,
        Tag.id != tag_id,
    )
    duplicate_result = await session.execute(duplicate_query)
    if duplicate_result.scalar_one_or_none():
        categories = await get_all_categories(session)
        tag_data = {
            "id": tag.id,
            "category": category,
            "value": value,
            "description": description,
            "is_predefined": is_predefined == "on",
        }
        return HTMLResponse(
            content=to_xml(
                EditTagPage(
                    tag=tag_data,
                    categories=categories,
                    error_message=f"A tag with category '{category}' and value '{value}' already exists.",
                )
            )
        )

    # Update the tag
    tag.category = category
    tag.value = value
    tag.description = description if description else None
    tag.is_predefined = is_predefined == "on"

    await session.commit()

    return RedirectResponse(
        url="/tags?success=Tag updated successfully",
        status_code=HTTP_303_SEE_OTHER,
    )
