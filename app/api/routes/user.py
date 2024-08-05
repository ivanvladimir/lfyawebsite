
from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse

from app import crud
from app.api.deps import CurrentUser
from app.core import security
from app.core.config import settings
#from app.core.security import get_password_hash
from app.models import Token

router = APIRouter()
