import time
from datetime import timedelta
from typing import Annotated, Any
import markdown

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import APIKeyCookie

from app.front.deps import get_current_user, TokenDep

import os
