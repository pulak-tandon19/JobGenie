from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.authentication import CookieTransport, BearerTransport, JWTStrategy, AuthenticationBackend


from .models import User
from db_config import async_session_maker
import uuid

SECRET = "SUPER_SECRET"  # replace with env variable

bearer_transport = BearerTransport(tokenUrl="/auth/jwt/login")
cookie_transport = CookieTransport(cookie_max_age=3600)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600, algorithm="HS256")

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport, 
    get_strategy=get_jwt_strategy,
)


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Request | None = None):
        print(f"User {user.id} has registered.")

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])