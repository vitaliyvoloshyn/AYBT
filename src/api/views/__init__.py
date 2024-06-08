from fastapi import APIRouter
from src.api.views.wd import wd_router

router = APIRouter()

router.include_router(wd_router)