from typing import Annotated, List

from fastapi import APIRouter, Form

from src.repositories.SQLRepository import WorDayRepository
from src.schemas.schemas import WorkDayDTO, WorkDayAddDTO
from src.services.WorkDayService import WorkDayService

wd_router = APIRouter(prefix='/workdays', tags=['WorkDay'])
wd_service = WorkDayService(WorDayRepository)


@wd_router.get('/', response_model=List[WorkDayDTO])
def get_all_days():
    return wd_service.get_all()


@wd_router.post('/add')
def add_wd(wd: WorkDayAddDTO):
    return wd_service.add(wd)