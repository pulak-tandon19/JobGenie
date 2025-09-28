from typing import Any, List

from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User

from .utils import JWTAuth
from errors import (
    InvalidToken,
    RefreshTokenRequired,
    AccessTokenRequired,
    # InsufficientPermission,
    # AccountNotVerified,
)



class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        self.jwt_auth = JWTAuth()

        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials

        token_data = await self.jwt_auth.decode_token(token)

        if not await self.token_valid(token):
            raise InvalidToken()

        self.verify_token_data(token_data)

        return token_data

    async def token_valid(self, token: str) -> bool:
        token_data = await self.jwt_auth.decode_token(token)

        return token_data is not None

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data.get("refresh"):
            raise AccessTokenRequired()


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data.get("refresh"):
            raise RefreshTokenRequired()



