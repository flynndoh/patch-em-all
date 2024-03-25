from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from session.user_session_manager import current_super_user
from database import get_async_session
from models.db_models import Patch, Flight

patches_router = APIRouter(tags=["patches"], prefix="/patches")


@patches_router.get("")
async def get_patches(session: AsyncSession = Depends(get_async_session)):
    return (await session.exec(select(Patch))).all()


@patches_router.get("/{id}")
async def get_patch(id: str, session: AsyncSession = Depends(get_async_session)):
    patch = await session.get(Patch, id)
    if not patch:
        raise HTTPException(status_code=404, detail="Patch not found")
    return patch


@patches_router.post("", dependencies=[Depends(current_super_user)])
async def create_patch(patch: Patch, session: AsyncSession = Depends(get_async_session)):
    if not (await session.exec(select(func.count(Flight.id)).where(Flight.id == patch.flight_id))).one():
        raise HTTPException(status_code=400, detail="Flight does not exist with that id")
    session.add(patch)
    await session.commit()
    await session.refresh(patch)
    return patch


@patches_router.put("/{id}", dependencies=[Depends(current_super_user)])
async def update_patch(id: str, flight_id: int | None = None, thumbnail: str | None = None, image: str | None = None,
                       session: AsyncSession = Depends(get_async_session)):
    db_patch = await session.get(Patch, id)
    if not db_patch:
        raise HTTPException(status_code=404, detail="Patch not found")

    if flight_id is not None:
        if not (await session.exec(select(func.count(Flight.id)).where(Flight.id == flight_id))).one():
            raise HTTPException(status_code=400, detail="No flight exists with that id")
        db_patch.flight_id = flight_id
    if thumbnail is not None:
        db_patch.thumbnail = thumbnail
    if image is not None:
        db_patch.image = image
    session.add(db_patch)
    await session.commit()
    await session.refresh(db_patch)
    return db_patch


@patches_router.delete("/{id}", dependencies=[Depends(current_super_user)])
async def delete_patch(id: str, session: AsyncSession = Depends(get_async_session)):
    patch = await session.get(Patch, id)
    if not patch:
        raise HTTPException(status_code=404, detail="Patch not found")
    await session.delete(patch)
    await session.commit()
    return {"message": "Patch deleted successfully"}
