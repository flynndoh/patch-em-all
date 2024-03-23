import uuid
from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import UUID4
from sqlmodel import SQLModel, Field, Relationship

from adapters.sqlmodel_fastapiuser import SQLModelBaseUserDB
from adapters.sqlmodel_fastapiuser.access_token import SQLModelBaseAccessToken


class Flight(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    timestamp: datetime
    patch: "Patch" = Relationship(back_populates="flight")


class Patch(SQLModel, table=True):
    id:  UUID4 = Field(primary_key=True, default_factory=uuid.uuid4)
    user: "User" = Relationship(back_populates="patches")
    user_id: UUID4 = Field(foreign_key="user.id")
    flight: Flight = Relationship(back_populates="patch")
    flight_id: Optional[int] = Field(foreign_key="flight.id")
    patch_number: Optional[int] = Field(default=None)


class User(SQLModelBaseUserDB, table=True):
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    created: datetime = Field(default_factory=datetime.utcnow)
    patches: list[Patch] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "delete"})


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


class AccessToken(SQLModelBaseAccessToken, table=True):
    pass
