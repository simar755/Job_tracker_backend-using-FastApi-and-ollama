from fastapi import APIRouter
from controllers.resume_controller import router as resume_router

router = APIRouter()

router.include_router(resume_router)
