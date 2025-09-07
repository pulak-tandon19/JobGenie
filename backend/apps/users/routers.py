from fastapi import FastAPI, APIRouter
from apps.users.schemas import UserRead, UserCreate
from apps.users.user_manager import fastapi_users

router = APIRouter()

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)