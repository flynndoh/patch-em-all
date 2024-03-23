from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from auth.user_session_manager import current_super_user
from database import get_async_session
from models.db_models import Flight

flights_router = APIRouter(tags=["flights"], prefix="/flights")


@flights_router.get("")
async def get_flights(session: AsyncSession = Depends(get_async_session)):
    return (await session.exec(select(Flight))).all()


@flights_router.get("/{id}")
async def get_flight(id: int, session: AsyncSession = Depends(get_async_session)):
    flight = await session.get(Flight, id)
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight


@flights_router.post("", dependencies=[Depends(current_super_user)])
async def create_flight(flight_id: int, flight_name: str, launch_datetime: datetime = datetime.utcnow(), session: AsyncSession = Depends(get_async_session)):
    if (await session.exec(select(func.count(Flight.id)).where(Flight.id == flight_id))).one():
        raise HTTPException(status_code=400, detail="Flight with that id already exists")
    flight = Flight(id=flight_id, name=flight_name, timestamp=launch_datetime)
    session.add(flight)
    await session.commit()
    await session.refresh(flight)
    return flight


@flights_router.put("/{id}", dependencies=[Depends(current_super_user)])
async def update_flight(id: int, flight_name: str, launch_datetime: datetime = datetime.utcnow(), session: AsyncSession = Depends(get_async_session)):
    db_flight = await session.get(Flight, id)
    if not db_flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    new_flight = Flight(id=id, name=flight_name, timestamp=launch_datetime)
    flight_data = new_flight.dict(exclude_unset=True)
    for key, value in flight_data.items():
        setattr(db_flight, key, value)
    session.add(db_flight)
    await session.commit()
    await session.refresh(db_flight)
    return db_flight


@flights_router.delete("/{id}", dependencies=[Depends(current_super_user)])
async def delete_flight(id: int, session: AsyncSession = Depends(get_async_session)):
    flight = await session.get(Flight, id)
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    await session.delete(flight)
    await session.commit()
    return {"message": "Flight deleted successfully"}
