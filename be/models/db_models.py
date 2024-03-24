import uuid
from datetime import datetime
from typing import Optional

from pydantic import UUID4
from sqlmodel import SQLModel, Field, Relationship

from adapters.sqlmodel_fastapiuser import SQLModelBaseUserDB
from adapters.sqlmodel_fastapiuser.access_token import SQLModelBaseAccessToken


class Flight(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    timestamp: datetime
    patch: "Patch" = Relationship(back_populates="flight", sa_relationship_kwargs={"lazy": "selectin"})


class UserPatch(SQLModel, table=True):
    user_id: UUID4 = Field(foreign_key="user.id", primary_key=True)
    patch_id: UUID4 = Field(foreign_key="patch.id", primary_key=True)
    patch_number: Optional[int] = Field(default=None)

    patch: "Patch" = Relationship(back_populates="user_patches", sa_relationship_kwargs={"lazy": "selectin"})
    user: "User" = Relationship(back_populates="patches", sa_relationship_kwargs={"lazy": "selectin"})


class Patch(SQLModel, table=True):
    id: UUID4 = Field(primary_key=True, default_factory=uuid.uuid4)
    flight: Flight = Relationship(back_populates="patch", sa_relationship_kwargs={"lazy": "selectin"})
    flight_id: Optional[int] = Field(foreign_key="flight.id")
    thumbnail: Optional[str] = Field(default=None)
    image: Optional[str] = Field(default=None)

    user_patches: list[UserPatch] = Relationship(back_populates="patch", sa_relationship_kwargs={"lazy": "selectin", "cascade": "delete"})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "flight_id": "0",
                    "image": "https://link/to/image.com",
                    "thumbnail": "https://link/to/thumbnail.com",
                }
            ]
        }
    }


class User(SQLModelBaseUserDB, table=True):
    id: UUID4 = Field(primary_key=True, default_factory=uuid.uuid4)
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    created: datetime = Field(default_factory=datetime.utcnow)

    patches: list[UserPatch] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin", "cascade": "delete"})


class AccessToken(SQLModelBaseAccessToken, table=True):
    pass

