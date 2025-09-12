from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.src.router import router

app = FastAPI(title="SPROUT - Multi Agent CV Analysis", description="Growing talent intelligence from resumes to opportunities🌱")
app.include_router(router=router)


templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})