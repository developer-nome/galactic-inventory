from fastapi import APIRouter, HTTPException, status
from typing import List
from models import Item, ItemCreate, ItemWithType
from database import db

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=List[ItemWithType])
async def get_items():
    """Get all items with their type information"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT
                i.id,
                i.name,
                i.description,
                i.item_type_id,
                it.name as item_type_name
            FROM galactic_items i
            LEFT JOIN galactic_item_types it ON i.item_type_id = it.id
            ORDER BY i.id
            """
        )
        return [dict(row) for row in rows]


@router.get("/{item_id}", response_model=ItemWithType)
async def get_item(item_id: int):
    """Get a specific item by ID with type information"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT
                i.id,
                i.name,
                i.description,
                i.item_type_id,
                it.name as item_type_name
            FROM galactic_items i
            LEFT JOIN galactic_item_types it ON i.item_type_id = it.id
            WHERE i.id = $1
            """,
            item_id
        )
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return dict(row)


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    """Create a new item"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO galactic_items (name, description, item_type_id)
            VALUES ($1, $2, $3)
            RETURNING id, name, description, item_type_id
            """,
            item.name,
            item.description,
            item.item_type_id
        )
        return dict(row)


@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemCreate):
    """Update an existing item"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            UPDATE galactic_items
            SET name = $1, description = $2, item_type_id = $3
            WHERE id = $4
            RETURNING id, name, description, item_type_id
            """,
            item.name,
            item.description,
            item.item_type_id,
            item_id
        )
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return dict(row)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """Delete an item"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM galactic_items WHERE id = $1",
            item_id
        )
        if result == "DELETE 0":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
