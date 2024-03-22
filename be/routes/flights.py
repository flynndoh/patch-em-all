from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from database import get_session
from models import Flight

flights_router = APIRouter(tags=["flights"], prefix="/flights")


@flights_router.get("")
def get_flights(session: Session = Depends(get_session)):
    return session.exec(select(Flight)).all()


@flights_router.get("/{flight_id}")
def get_flight(flight_id: int, session: Session = Depends(get_session)):
    flight = session.get(Flight, flight_id)
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight


@flights_router.post("")
def create_flight(flight_id: int, flight_name: str, launch_datetime: datetime = datetime.utcnow(), session: Session = Depends(get_session)):
    flight = Flight(id=flight_id, name=flight_name, timestamp=launch_datetime)
    session.add(flight)
    session.commit()
    session.refresh(flight)
    return flight


@flights_router.put("/{flight_id}")
def update_flight(flight_id: int, flight_name: str, launch_datetime: datetime = datetime.utcnow(), session: Session = Depends(get_session)):
    db_flight = session.get(Flight, flight_id)
    if not db_flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    new_flight = Flight(id=flight_id, name=flight_name, timestamp=launch_datetime)
    flight_data = new_flight.dict(exclude_unset=True)
    for key, value in flight_data.items():
        setattr(db_flight, key, value)
    session.add(db_flight)
    session.commit()
    session.refresh(db_flight)
    return db_flight


@flights_router.delete("/{flight_id}")
def delete_flight(flight_id: int, session: Session = Depends(get_session)):
    flight = session.get(Flight, flight_id)
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    session.delete(flight)
    session.commit()
    return {"message": "Flight deleted successfully"}
