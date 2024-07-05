from fastapi import APIRouter

from src.api.views.rate import rate_router
from src.api.views.reports import report_router
from src.api.views.ratetype import rate_type_router
from src.api.views.ratevalue import rate_value_router
from src.api.views.wd import wd_router
from src.api.views.payment import pmnt_router

router = APIRouter()

router.include_router(wd_router)
router.include_router(rate_router)
router.include_router(rate_type_router)
router.include_router(rate_value_router)
router.include_router(report_router)
router.include_router(pmnt_router)
