"""
API routes for Tag management.

Provides CRUD operations for tags.
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from tcm.database import get_async_session
from tcm.models.tag import Tag
from tcm.schemas.tag import TagCreate, TagUpdate, TagResponse, TagListResponse

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=TagListResponse)
async def list_tags(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    category: str | None = Query(None, description="Filter by category"),
    session: AsyncSession = Depends(get_async_session),
):
    """
    List all tags with pagination and optional filtering.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        category: Optional category filter
        session: Database session
    """
    # Build query
    query = select(Tag)
    if category:
        query = query.where(Tag.category == category)

    # Get total count
    count_query = select(func.count()).select_from(Tag)
    if category:
        count_query = count_query.where(Tag.category == category)

    total_result = await session.execute(count_query)
    total = total_result.scalar_one()

    # Get paginated results
    query = query.offset(skip).limit(limit).order_by(Tag.category, Tag.value)
    result = await session.execute(query)
    tags = result.scalars().all()

    return TagListResponse(
        tags=[TagResponse.model_validate(tag) for tag in tags],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get("/categories", response_model=list[str])
async def list_categories(
    session: AsyncSession = Depends(get_async_session),
):
    """
    List all unique tag categories.

    Args:
        session: Database session
    """
    query = select(Tag.category).distinct().order_by(Tag.category)
    result = await session.execute(query)
    categories = result.scalars().all()
    return list(categories)


@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(
    tag_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Get a specific tag by ID.

    Args:
        tag_id: Tag ID
        session: Database session
    """
    query = select(Tag).where(Tag.id == tag_id)
    result = await session.execute(query)
    tag = result.scalar_one_or_none()

    if not tag:
        raise HTTPException(status_code=404, detail=f"Tag with id {tag_id} not found")

    return TagResponse.model_validate(tag)


@router.post("", response_model=TagResponse, status_code=201)
async def create_tag(
    tag_data: TagCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Create a new tag.

    Args:
        tag_data: Tag data to create
        session: Database session
    """
    # Check if tag with same category and value already exists
    query = select(Tag).where(
        Tag.category == tag_data.category,
        Tag.value == tag_data.value,
    )
    result = await session.execute(query)
    existing_tag = result.scalar_one_or_none()

    if existing_tag:
        raise HTTPException(
            status_code=400,
            detail=f"Tag with category '{tag_data.category}' and value '{tag_data.value}' already exists",
        )

    # Create new tag
    tag = Tag(**tag_data.model_dump())
    session.add(tag)
    await session.commit()
    await session.refresh(tag)

    return TagResponse.model_validate(tag)


@router.patch("/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: int,
    tag_data: TagUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Update an existing tag.

    Args:
        tag_id: Tag ID
        tag_data: Tag data to update
        session: Database session
    """
    # Get existing tag
    query = select(Tag).where(Tag.id == tag_id)
    result = await session.execute(query)
    tag = result.scalar_one_or_none()

    if not tag:
        raise HTTPException(status_code=404, detail=f"Tag with id {tag_id} not found")

    # Update fields
    update_data = tag_data.model_dump(exclude_unset=True)

    # Check for duplicate if category or value is being updated
    if "category" in update_data or "value" in update_data:
        new_category = update_data.get("category", tag.category)
        new_value = update_data.get("value", tag.value)

        # Check if another tag with same category and value exists
        duplicate_query = select(Tag).where(
            Tag.category == new_category,
            Tag.value == new_value,
            Tag.id != tag_id,
        )
        duplicate_result = await session.execute(duplicate_query)
        if duplicate_result.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail=f"Tag with category '{new_category}' and value '{new_value}' already exists",
            )

    for field, value in update_data.items():
        setattr(tag, field, value)

    await session.commit()
    await session.refresh(tag)

    return TagResponse.model_validate(tag)


@router.delete("/{tag_id}", status_code=204)
async def delete_tag(
    tag_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Delete a tag.

    Args:
        tag_id: Tag ID
        session: Database session
    """
    # Get existing tag
    query = select(Tag).where(Tag.id == tag_id)
    result = await session.execute(query)
    tag = result.scalar_one_or_none()

    if not tag:
        raise HTTPException(status_code=404, detail=f"Tag with id {tag_id} not found")

    await session.delete(tag)
    await session.commit()
