from fastapi import APIRouter

from auth.user_session_manager import auth_backend, fastapi_users
from models import UserCreate, UserRead

auth_router = APIRouter(tags=["auth"], prefix="/auth")

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
)

auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

auth_router.include_router(
    fastapi_users.get_reset_password_router(),
)