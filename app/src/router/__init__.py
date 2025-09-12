from fastapi import APIRouter
from app.src.router.agent.api import router as agent
from app.src.router.orchestration.api import router as orchestration


router = APIRouter(prefix="/api")
router.include_router(agent)
router.include_router(orchestration)