from fastapi import APIRouter, HTTPException, status
from typing import List
from models import Station, StationCreate, StationInventory, StationInventoryCreate, InventoryItemDetail
from database import db

router = APIRouter(prefix="/stations", tags=["stations"])


@router.get("", response_model=List[Station])
async def get_stations():
    """Get all stations"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, name, description FROM galactic_stations ORDER BY id")
        return [dict(row) for row in rows]


@router.get("/{station_id}", response_model=Station)
async def get_station(station_id: int):
    """Get a specific station by ID"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id, name, description FROM galactic_stations WHERE id = $1",
            station_id
        )
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station not found")
        return dict(row)


@router.post("", response_model=Station, status_code=status.HTTP_201_CREATED)
async def create_station(station: StationCreate):
    """Create a new station"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO galactic_stations (name, description)
            VALUES ($1, $2)
            RETURNING id, name, description
            """,
            station.name,
            station.description
        )
        return dict(row)


@router.put("/{station_id}", response_model=Station)
async def update_station(station_id: int, station: StationCreate):
    """Update an existing station"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            UPDATE galactic_stations
            SET name = $1, description = $2
            WHERE id = $3
            RETURNING id, name, description
            """,
            station.name,
            station.description,
            station_id
        )
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station not found")
        return dict(row)


@router.delete("/{station_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_station(station_id: int):
    """Delete a station"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM galactic_stations WHERE id = $1",
            station_id
        )
        if result == "DELETE 0":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station not found")


@router.get("/{station_id}/inventory", response_model=List[InventoryItemDetail])
async def get_station_inventory(station_id: int):
    """Get all inventory items for a specific station"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT
                si.id as inventory_id,
                i.id as item_id,
                i.name as item_name,
                i.description as item_description,
                it.name as item_type_name
            FROM galactic_stations_inventory si
            JOIN galactic_items i ON si.galactic_item_id = i.id
            LEFT JOIN galactic_item_types it ON i.item_type_id = it.id
            WHERE si.galactic_station_id = $1
            ORDER BY si.id
            """,
            station_id
        )
        return [dict(row) for row in rows]


@router.post("/{station_id}/inventory", response_model=StationInventory, status_code=status.HTTP_201_CREATED)
async def add_item_to_station_inventory(station_id: int, item_id: int):
    """Add an item to a station's inventory"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        station_exists = await conn.fetchval(
            "SELECT EXISTS(SELECT 1 FROM galactic_stations WHERE id = $1)",
            station_id
        )
        if not station_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station not found")

        item_exists = await conn.fetchval(
            "SELECT EXISTS(SELECT 1 FROM galactic_items WHERE id = $1)",
            item_id
        )
        if not item_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

        row = await conn.fetchrow(
            """
            INSERT INTO galactic_stations_inventory (galactic_station_id, galactic_item_id)
            VALUES ($1, $2)
            RETURNING id, galactic_station_id, galactic_item_id
            """,
            station_id,
            item_id
        )
        return dict(row)


@router.delete("/{station_id}/inventory/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item_from_station_inventory(station_id: int, inventory_id: int):
    """Remove an item from a station's inventory"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        result = await conn.execute(
            """
            DELETE FROM galactic_stations_inventory
            WHERE id = $1 AND galactic_station_id = $2
            """,
            inventory_id,
            station_id
        )
        if result == "DELETE 0":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inventory entry not found for this station"
            )
