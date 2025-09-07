from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import Column, Integer, String

from db_config import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    first_name = Column(String)
    last_name = Column(String)
    profile_picture = Column(String)
    