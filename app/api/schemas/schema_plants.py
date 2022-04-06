from typing import Optional

from pydantic import BaseModel


class PlantGet(BaseModel):
    pass


class PlantCreate(BaseModel):
    name: str
    description: str
    category: str
    vase: str
    water_sprinklers_id: Optional[int] = None


class PlantPut(BaseModel):
    id: int
    name: str
    description: str
    category: str
    vase: str
    water_sprinklers_id: Optional[int] = None


class PlantPatch(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    vase: Optional[str] = None
    water_sprinklers_id: Optional[int] = None


class PlantDelete(BaseModel):
    id: int
