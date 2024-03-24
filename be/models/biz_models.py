import uuid
from datetime import datetime

from fastapi_users import schemas
from pydantic import BaseModel

from models.db_models import Flight


class UserRead(schemas.BaseUser[uuid.UUID]):
    first_name: str
    last_name: str
    created: datetime


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str
    last_name: str


class Pokemon(BaseModel):
    id: int
    name: str
    sprite: str
    image: str


class PatchRead(BaseModel):
    id: uuid.UUID
    patch_number: int
    flight: Flight
    image: str
    thumbnail: str


class PatchesRead(BaseModel):
    patches: list[PatchRead]

