from sqlalchemy import select
from passlib.context import CryptContext
from datetime import datetime, timedelta
from .models import User
import jwt
import uuid

from config import Config

password_context = CryptContext(schemes=["argon2"], deprecated="auto")

class JWTAuth:

    async def verify_password(self, plain_password: str, hashed_password: str):
        return password_context.verify(plain_password, hashed_password)

    async def create_token(self, user_data: dict, refresh: bool = False):
        payload = {}
        payload['user'] = user_data
        if not refresh:
            payload['exp'] = datetime.utcnow() + timedelta(minutes=Config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        else:
            payload['exp'] = datetime.utcnow() + timedelta(days=Config.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        payload['jti'] = str(uuid.uuid4())
        payload['refresh'] = refresh

        print("payload", payload)

        token = jwt.encode(payload, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

        return token

    async def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired"}
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}

