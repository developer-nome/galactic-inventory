from pydantic import BaseModel, Field
from typing import Optional


class ItemTypeBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None


class ItemTypeCreate(ItemTypeBase):
    pass


class ItemType(ItemTypeBase):
    id: int

    class Config:
        from_attributes = True


class ItemBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    item_type_id: Optional[int] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True


class ItemWithType(BaseModel):
    """Item with type information"""
    id: int
    name: str
    description: Optional[str] = None
    item_type_id: Optional[int] = None
    item_type_name: Optional[str] = None

    class Config:
        from_attributes = True


class PlanetBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None


class PlanetCreate(PlanetBase):
    pass


class Planet(PlanetBase):
    id: int

    class Config:
        from_attributes = True


class StationBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None


class StationCreate(StationBase):
    pass


class Station(StationBase):
    id: int

    class Config:
        from_attributes = True


class SolarSystemBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None


class SolarSystemCreate(SolarSystemBase):
    pass


class SolarSystem(SolarSystemBase):
    id: int

    class Config:
        from_attributes = True


class StationInventoryBase(BaseModel):
    galactic_station_id: int
    galactic_item_id: int


class StationInventoryCreate(StationInventoryBase):
    pass


class StationInventory(StationInventoryBase):
    id: int

    class Config:
        from_attributes = True


class PlanetInventoryBase(BaseModel):
    galactic_planet_id: int


class PlanetInventoryCreate(PlanetInventoryBase):
    pass


class PlanetInventory(PlanetInventoryBase):
    id: int

    class Config:
        from_attributes = True


class InventoryItemDetail(BaseModel):
    """Detailed inventory entry with item information"""
    inventory_id: int
    item_id: int
    item_name: str
    item_description: Optional[str] = None
    item_type_name: Optional[str] = None
