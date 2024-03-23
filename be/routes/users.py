from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from auth.user_session_manager import fastapi_users, current_active_user
from database import get_async_session, get_user_db
from adapters.sqlmodel_fastapiuser import SQLModelUserDatabaseAsync
from models.db_models import User, Patch
from models.biz_models import UserRead, UserUpdate

users_router = APIRouter(tags=["users"], prefix="/users")

users_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)


@users_router.get("")
async def get_users(session: AsyncSession = Depends(get_async_session)):
    return [UserRead(**u.dict()) for u in (await session.exec(select(User))).all()]


@users_router.get("/me/patches")
async def get_user_patches(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)):
    return (await session.exec(select(Patch).where(Patch.user_id == user.id))).all()


@users_router.get("/{id}/patches")
async def get_user_patches(id: str, session: AsyncSession = Depends(get_async_session), user_db: SQLModelUserDatabaseAsync = Depends(get_user_db)):
    user = await user_db.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return (await session.exec(select(Patch).where(Patch.user_id == user.id))).all()

