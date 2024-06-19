
from fastapi import APIRouter

from src.services import IService

report_router = APIRouter(prefix='/reports', tags=['Reports'])
report_service = IService()


@report_router.get('/get_plan_work_days')
def get_plan_work_days(month: int, year: int):
    return report_service.get_plan_wd_per_month(month, year)


@report_router.get('/get_fact_work_days')
def get_fact_work_days(month: int, year: int):
    return report_service.get_fact_wd_per_month(month, year)


@report_router.get('/get_wage')
def get_wage_per_month(month: int, year: int, fact_wage: bool = True):
    return report_service.get_wage_per_month(month, year, fact_wage)
