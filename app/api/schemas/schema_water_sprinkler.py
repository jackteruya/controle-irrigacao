from typing import Optional

from pydantic import BaseModel


class WaterSprinklerGet(BaseModel):
    pass


class WaterSprinklerCreate(BaseModel):
    name: str
    description: str
    is_active: bool
    settings: list


class WaterSprinklerAddSettings(BaseModel):
    id: int
    settings: list


class WaterSprinklerPut(BaseModel):
    id: int
    name: str
    is_active: bool
    description: str
    settings: list


class WaterSprinklerPatch(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    settings: Optional[list] = None


class WaterSprinklerDelete(BaseModel):
    id: int
