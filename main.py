from __future__ import annotations

from fastapi import FastAPI
from app.src.router import router

app = FastAPI(title="SPROUT - Multi Agent CV Analysis", description="Growing talent intelligence from resumes to opportunities🌱")
app.include_router(router=router)