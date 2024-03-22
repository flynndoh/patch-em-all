from fastapi import APIRouter

from routes.flights import flights_router
from routes.patches import patches_router
from routes.users import users_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(flights_router)
api_v1_router.include_router(users_router)
api_v1_router.include_router(patches_router)
