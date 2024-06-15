
from fastapi import APIRouter

from src.services import IService

report_router = APIRouter(prefix='/reports', tags=['Reports'])
report_service = IService()

@report_router.get('/get_work_days')
def get_work_days(month: int, year: int):
    return report_service.get_work_days_per_month(month, year)

@report_router.get('/get_wage')
def get_wage_per_month(month: int, year: int):
    return report_service.get_wage_per_month(month, year)
