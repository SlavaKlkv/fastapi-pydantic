from typing import Optional

from pydantic import BaseModel


class EntityBase(BaseModel):
    name: str
    value: int


class EntityCreate(EntityBase):
    pass


class EntityUpdate(BaseModel):
    name: Optional[str] = None
    value: Optional[int] = None


class Entity(EntityBase):
    id: int
