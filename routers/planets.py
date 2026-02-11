from fastapi import APIRouter, HTTPException, status
from typing import List
from models import Planet, PlanetCreate, PlanetInventory, PlanetInventoryCreate
from database import db

router = APIRouter(prefix="/planets", tags=["planets"])


@router.get("", response_model=List[Planet])
async def get_planets():
    """Get all planets"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, name, description FROM galactic_planets ORDER BY id")
        return [dict(row) for row in rows]


@router.get("/{planet_id}", response_model=Planet)
async def get_planet(planet_id: int):
    """Get a specific planet by ID"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id, name, description FROM galactic_planets WHERE id = $1",
            planet_id
        )
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planet not found")
        return dict(row)


@router.post("", response_model=Planet, status_code=status.HTTP_201_CREATED)
async def create_planet(planet: PlanetCreate):
    """Create a new planet"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO galactic_planets (name, description)
            VALUES ($1, $2)
            RETURNING id, name, description
            """,
            planet.name,
            planet.description
        )
        return dict(row)


@router.put("/{planet_id}", response_model=Planet)
async def update_planet(planet_id: int, planet: PlanetCreate):
    """Update an existing planet"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            UPDATE galactic_planets
            SET name = $1, description = $2
            WHERE id = $3
            RETURNING id, name, description
            """,
            planet.name,
            planet.description,
            planet_id
        )
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planet not found")
        return dict(row)


@router.delete("/{planet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_planet(planet_id: int):
    """Delete a planet"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM galactic_planets WHERE id = $1",
            planet_id
        )
        if result == "DELETE 0":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planet not found")


@router.get("/{planet_id}/inventory", response_model=List[PlanetInventory])
async def get_planet_inventory(planet_id: int):
    """
    Get all inventory entries for a specific planet.
    Note: The galactic_planets_inventory table appears to be missing a galactic_item_id column.
    This endpoint returns basic inventory records.
    """
    pool = db.get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT id, galactic_planet_id
            FROM galactic_planets_inventory
            WHERE galactic_planet_id = $1
            ORDER BY id
            """,
            planet_id
        )
        return [dict(row) for row in rows]


@router.post("/{planet_id}/inventory", response_model=PlanetInventory, status_code=status.HTTP_201_CREATED)
async def add_to_planet_inventory(planet_id: int):
    """
    Add an inventory entry for a planet.
    Note: The galactic_planets_inventory table appears to be missing a galactic_item_id column.
    This endpoint creates a basic inventory record.
    """
    pool = db.get_pool()
    async with pool.acquire() as conn:
        planet_exists = await conn.fetchval(
            "SELECT EXISTS(SELECT 1 FROM galactic_planets WHERE id = $1)",
            planet_id
        )
        if not planet_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planet not found")

        row = await conn.fetchrow(
            """
            INSERT INTO galactic_planets_inventory (galactic_planet_id)
            VALUES ($1)
            RETURNING id, galactic_planet_id
            """,
            planet_id
        )
        return dict(row)


@router.delete("/{planet_id}/inventory/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_planet_inventory(planet_id: int, inventory_id: int):
    """Remove an inventory entry from a planet"""
    pool = db.get_pool()
    async with pool.acquire() as conn:
        result = await conn.execute(
            """
            DELETE FROM galactic_planets_inventory
            WHERE id = $1 AND galactic_planet_id = $2
            """,
            inventory_id,
            planet_id
        )
        if result == "DELETE 0":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inventory entry not found for this planet"
            )
