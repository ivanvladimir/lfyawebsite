from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import APIKeyCookie

from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from app.core import security
from app.core.config import settings
from app.models import TokenPayload, User
from app.core.db import user_collection
from app.crud import get_user
from bson import ObjectId

cookie_scheme = APIKeyCookie(name="session")

TokenDep = Annotated[str, Depends(cookie_scheme)]

async def get_current_user(token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = await get_user(token_data.subject)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]
