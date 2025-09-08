from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.users.schemas import *
from apps.users.user_manager import fastapi_users
from .services import UserService
from .dependencies import RefreshTokenBearer

from db_config import get_db


router = APIRouter(prefix="/auth", tags=["authentication"])

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
)


@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    return await user_service.login(login_data)

@router.get("/refresh_token")
async def refresh_token(token_details: dict = Depends(RefreshTokenBearer()), db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    return await user_service.get_new_access_token(token_details)

