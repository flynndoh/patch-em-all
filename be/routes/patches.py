from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from auth.user_session_manager import current_active_user
from database import get_async_session
from models.db_models import Patch, User, Flight

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


@patches_router.post("")
async def create_patch(flight_id: int, patch_number: int | None = None,
                       session: AsyncSession = Depends(get_async_session), 
                       user: User = Depends(current_active_user)):
    if not (await session.exec(select(func.count(Flight.id)).where(Flight.id == flight_id))).one():
        raise HTTPException(status_code=400, detail="Flight does not exist with that id")

    patch = Patch(user_id=user.id, flight_id=flight_id, patch_number=patch_number)
    session.add(patch)
    await session.commit()
    await session.refresh(patch)
    return patch


@patches_router.put("/{id}")
async def update_patch(id: str, user_id: str | None = None, flight_id: int | None = None, patch_number: int | None = None,
                       session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)):
    db_patch = await session.get(Patch, id)
    if not db_patch:
        raise HTTPException(status_code=404, detail="Patch not found")
    if not user.is_superuser and db_patch.user_id != user.user_id:
        raise HTTPException(status_code=403, detail="You may only modify your own patches")

    if user_id is not None:
        if not (await session.exec(select(func.count(User.id)).where(User.id == user_id))).one():
            raise HTTPException(status_code=400, detail="User does not exist with that id")
        db_patch.user_id = user_id
    if flight_id is not None:
        if not (await session.exec(select(func.count(Flight.id)).where(Flight.id == flight_id))).one():
            raise HTTPException(status_code=400, detail="Flight does not exist with that id")
        db_patch.flight_id = flight_id
    if patch_number is not None:
        db_patch.patch_number = patch_number
    session.add(db_patch)
    await session.commit()
    await session.refresh(db_patch)
    return db_patch


@patches_router.delete("/{id}")
async def delete_patch(id: str, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)):
    patch = await session.get(Patch, id)
    if not patch:
        raise HTTPException(status_code=404, detail="Patch not found")
    if not user.is_superuser and patch.user_id != user.id:
        raise HTTPException(status_code=403, detail="You may only delete your own patches")

    await session.delete(patch)
    await session.commit()
    return {"message": "Patch deleted successfully"}
