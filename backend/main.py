from fastapi import FastAPI, APIRouter,  Depends, HTTPException, status
from fastapi_users.password import PasswordHelper
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from apps.users.routers import router as users_router
from errors import register_all_errors

app = FastAPI()
register_all_errors(app)
router = APIRouter()

@app.get("/")
def index():
    return {"msg": "Hello, World!"}


app.include_router(users_router)