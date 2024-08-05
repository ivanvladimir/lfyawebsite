import time
from datetime import timedelta
import humanize
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse

from app import crud
from app.api.deps import CurrentUser
from app.core import security
from app.core import uptime
from app.core.config import settings
from app.models import Token

router = APIRouter()

__API_VERSION__ = "0.1.5"
__API_NAME__ = "API para Lenguajes Formales y Autómatas"


@router.get("/")
async def main_api():
    """Prints info"""
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time
    delta = timedelta(seconds=time.time() - uptime.get_uptime())
    return {
        "name": __API_NAME__,
        "version": __API_VERSION__,
        "uptime": f"{humanize.precisedelta(delta)}",
        "elapsed_time_seconds": f"{elapsed_time():2.3f} segs",
    }
