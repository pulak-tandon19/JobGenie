from fastapi import FastAPI, APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from apps.users.schemas import *
from apps.users.user_manager import fastapi_users
from .services import UserService, get_current_user
from .dependencies import RefreshTokenBearer
from .models import User

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

@router.post("/upload-profile-picture")
async def upload_profile_picture(file: UploadFile = File(...), user: User = Depends(get_current_user)):
    user_service = UserService()
    url = await user_service.save_profile_picture(file)
    return {"url": url}

@router.get("/users/me", response_model=UserRead)
async def get_my_profile(user: User = Depends(get_current_user),
):
    user_service = UserService()
    return await user_service.get_user(user)


@router.patch("/users/me", response_model=UserRead)
async def update_me(
    payload: UserUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_service = UserService(db)
    return await user_service.update_user(user, payload)


