from fastapi import APIRouter, HTTPException, status
from typing import List
from models import ItemType, ItemTypeCreate
from database import db

router = APIRouter(prefix="/item-types", tags=["item-types"])


@router.get("", response_model=List[ItemType])
async def get_item_types():
    """Get all item types"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, name, description FROM galactic_item_types ORDER BY name")
        return [dict(row) for row in rows]


@router.get("/{item_type_id}", response_model=ItemType)
async def get_item_type(item_type_id: int):
    """Get a specific item type by ID"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id, name, description FROM galactic_item_types WHERE id = $1",
            item_type_id
        )
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item type not found")
        return dict(row)


@router.post("", response_model=ItemType, status_code=status.HTTP_201_CREATED)
async def create_item_type(item_type: ItemTypeCreate):
    """Create a new item type"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO galactic_item_types (name, description)
            VALUES ($1, $2)
            RETURNING id, name, description
            """,
            item_type.name,
            item_type.description
        )
        return dict(row)


@router.put("/{item_type_id}", response_model=ItemType)
async def update_item_type(item_type_id: int, item_type: ItemTypeCreate):
    """Update an existing item type"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            UPDATE galactic_item_types
            SET name = $1, description = $2
            WHERE id = $3
            RETURNING id, name, description
            """,
            item_type.name,
            item_type.description,
            item_type_id
        )
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item type not found")
        return dict(row)


@router.delete("/{item_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_type(item_type_id: int):
    """Delete an item type"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM galactic_item_types WHERE id = $1",
            item_type_id
        )
        if result == "DELETE 0":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item type not found")
