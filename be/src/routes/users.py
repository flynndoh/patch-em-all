from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession

from session.user_session_manager import fastapi_users, current_active_user
from database import get_async_session, get_user_db
from adapters.sqlmodel_fastapiuser import SQLModelUserDatabaseAsync
from models.db_models import User, UserPatch, Patch
from models.biz_models import UserRead, UserUpdate, PatchesRead, PatchRead

users_router = APIRouter(tags=["users"], prefix="/users")

users_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)


@users_router.get("")
async def get_users(session: AsyncSession = Depends(get_async_session)):
    return [UserRead(**u.dict()) for u in (await session.exec(select(User))).all()]


@users_router.get("/me/patches")
async def get_patches(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)):
    patches = (
        await session.exec(
            select(UserPatch)
            .where(UserPatch.user_id == user.id)
            .order_by(desc(UserPatch.patch_number))
        )
    ).all()
    response = PatchesRead(patches=[])
    for patch in patches:
        response.patches.append(PatchRead(id=patch.patch_id, patch_number=patch.patch_number, flight=patch.patch.flight,
                                          image=patch.patch.image, thumbnail=patch.patch.thumbnail))
    return response


@users_router.get("/{id}/patches")
async def get_user_patches(id: str, session: AsyncSession = Depends(get_async_session), user_db: SQLModelUserDatabaseAsync = Depends(get_user_db)):
    user = await user_db.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await get_patches(session=session, user=user)


@users_router.post("/me/patches")
async def add_patch(flight_id: int, patch_number: int | None = None, session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_active_user)):

    patch = (await session.exec(select(Patch).where(Patch.flight_id == flight_id))).one_or_none()
    if not patch:
        raise HTTPException(status_code=400, detail="No patches exist for a flight with that id")

    user_patch = UserPatch(user_id=user.id, patch_id=patch.id, patch_number=patch_number, flight=flight_id)
    session.add(user_patch)
    await session.commit()
    await session.refresh(user_patch)
    return user_patch


@users_router.put("/me/patches/{id}")
async def update_patch(id: str, patch_number: int, session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_active_user)):
    db_patch = await session.get(UserPatch, (user.id, id))
    if not db_patch:
        raise HTTPException(status_code=404, detail="Patch not found")
    if not user.is_superuser and db_patch.user_id != user.user_id:
        raise HTTPException(status_code=403, detail="You may only modify your own patches")

    db_patch.patch_number = patch_number
    session.add(db_patch)
    await session.commit()
    await session.refresh(db_patch)
    return db_patch


@users_router.delete("/me/patches/{id}")
async def delete_patch(id: str, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)):
    patch = await session.get(UserPatch, (user.id, id))
    if not patch:
        raise HTTPException(status_code=404, detail="Patch not found")
    if not user.is_superuser and patch.user_id != user.id:
        raise HTTPException(status_code=403, detail="You may only delete your own patches")
    await session.delete(patch)
    await session.commit()
    return {"message": "Patch deleted successfully"}
