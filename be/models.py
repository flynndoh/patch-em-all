from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class Flight(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    timestamp: datetime
    patch: "Patch" = Relationship(back_populates="flight")


class Patch(SQLModel, table=True):
    user: "User" = Relationship(back_populates="patches")
    user_id: int = Field(primary_key=True, foreign_key="user.id")
    flight: Flight = Relationship(back_populates="patch")
    flight_id: int = Field(primary_key=True, foreign_key="flight.id")
    patch_number: Optional[int]


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    created: datetime = Field(default_factory=datetime.utcnow)
    patches: list[Patch] = Relationship(back_populates="user")


