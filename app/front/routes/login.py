import time
from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from app import crud
from app.api.deps import CurrentUser
from app.core import security
from app.core.config import settings
#from app.core.security import get_password_hash
from app.models import Token, UserEnum

templates = Jinja2Templates(directory="app/front/templates")

router = APIRouter()

@router.get("/")
async def index(request: Request) -> RedirectResponse:
    """
    Logs in user if has the correct url
    """
    return templates.TemplateResponse(
        request=request, name="index.html", context={}
    )

@router.get("/login/{secret_url}")
async def login_url(request: Request, secret_url) -> HTMLResponse:
    """
    Logs in user if has the correct url
    """
    user= await crud.authenticate(secret_url)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if user:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token=security.create_access_token(
            subject=user.id, expires_delta=access_token_expires
        )
        if user.role is UserEnum.teacher:
            response=RedirectResponse(url=request.url_for('teacher_home'))
        else:
            raise HTTPException(status_code=400, detail="Incorrect url")
        response.set_cookie(key="session", value=access_token)
        return response
    else:
        return 404, "URL invalid"

@router.get("/logout")
async def logout(request: Request) -> HTMLResponse:
    """
    Logout user
    """
    response=RedirectResponse(url=request.url_for('index'))
    response.delete_cookie("session")
    return response




