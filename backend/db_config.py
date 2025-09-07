from collections.abc import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from fastapi_users.db import SQLAlchemyUserDatabase

DATABASE_URL = "postgresql+asyncpg://postgres:password@db:5432/jobgenie_db"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()



