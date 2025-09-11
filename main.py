from __future__ import annotations

from fastapi import FastAPI
from app.src.router.api import router

app = FastAPI(title="SPROUT AI AGENT", description="Growing talent intelligence from resumes to opportunities🌱")
app.include_router(router=router)