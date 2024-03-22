from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlmodel import select, Session
from database import get_session
from models import Patch, Patch

patches_router = APIRouter(tags=["patches"], prefix="/patches")


@patches_router.get("")
def get_patches(session: Session = Depends(get_session)):
    return session.exec(select(Patch)).all()


@patches_router.get("/{patch_id}")
def get_patch(user_id: int, flight_id: int, session: Session = Depends(get_session)):
    patch = session.get(Patch, (user_id, flight_id))
    if not patch:
        raise HTTPException(status_code=404, detail="Patch not found")
    return patch


@patches_router.post("")
def create_patch(user_id: int, flight_id: int, patch_number: int | None = None, session: Session = Depends(get_session)):
    patch = Patch(user_id=user_id, flight_id=flight_id, patch_number=patch_number)
    # todo: prevent 500 error when adding duplicates
    # if session.exec(select(func.count((Patch.flight_id, Patch.user_id))).where(Patch.flight_id == flight_id).where(Patch.user_id == user_id)).one():
    #     raise HTTPException(status_code=400, detail="Patch already exists for this flight + user combo")
    session.add(patch)
    session.commit()
    session.refresh(patch)
    return patch


@patches_router.put("/{patch_id}")
def update_patch(user_id: int, flight_id: int, patch_number: int, session: Session = Depends(get_session)):
    db_patch = session.get(Patch, (user_id, flight_id))
    if not db_patch:
        raise HTTPException(status_code=404, detail="Patch not found")

    db_patch.patch_number = patch_number
    session.add(db_patch)
    session.commit()
    session.refresh(db_patch)
    return db_patch


@patches_router.delete("/{patch_id}")
def delete_patch(user_id: int, flight_id: int, session: Session = Depends(get_session)):
    patch = session.get(Patch, (user_id, flight_id))
    if not patch:
        raise HTTPException(status_code=404, detail="Patch not found")
    session.delete(patch)
    session.commit()
    return {"message": "Patch deleted successfully"}
