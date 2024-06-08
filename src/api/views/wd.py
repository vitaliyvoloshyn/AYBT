from typing import List

from fastapi import APIRouter

from src.repositories.SQLRepository import WorDayRepository
from src.schemas.schemas import WorkDayDTO, WorkDayAddDTO
from src.services.WorkDayService import WorkDayService

wd_router = APIRouter(prefix='/workdays', tags=['WorkDay'])
wd_service = WorkDayService(WorDayRepository)


@wd_router.get('/', response_model=List[WorkDayDTO])
def get_all_days():
    return wd_service.get_all()


@wd_router.get('/{pk}', response_model=List[WorkDayDTO])
def get_all_days(pk: int):
    return wd_service.get_obj(id=pk)


@wd_router.post('/add')
def add_wd(wd: WorkDayAddDTO):
    return wd_service.add(wd)


@wd_router.delete('/delete')
def delete_wd(pk: int):
    wd_service.delete(pk)
    return {'status': 'OK'}


@wd_router.patch('/{pk}')
def update_wd(pk: int, wd: WorkDayAddDTO):
    data_ = wd.dict()
    wd_service.update(pk, data_)
    return {'status': 'OK'}
