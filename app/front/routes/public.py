import time
from datetime import timedelta
from typing import Annotated, Any
import os
import markdown

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import APIKeyCookie

from app.front.deps import get_current_user, TokenDep

import os

templates = Jinja2Templates(directory="app/front/templates")

router = APIRouter()

@router.get("/page/{view}")
async def page(view: str, request:Request) -> HTMLResponse:
    """
    Main view for pages
    """
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time

    content_path="app/content/"

    if os.path.exists(os.path.join(content_path,f"{view}.md")):
        content = open(os.path.join(content_path,f"{view}.md")).read()
        md = markdown.Markdown(extensions=['meta','tables'])
        content= md.convert(content)
        response=templates.TemplateResponse(
            request=request, 
            name="public/page.html", 
            context={
                "content":content,
                "metadata":md.Meta,
                "elapsed_time_seconds":f"{elapsed_time():2.3f}"})        
        return response
    else:
        raise HTTPException(status_code=404, detail="Page not found")
