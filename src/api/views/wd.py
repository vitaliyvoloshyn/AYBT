from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from src.repositories.SQLRepository import WorDayRepository
from src.schemas.schemas import WorkDayDTO, WorkDayAddDTO
from src.services import IService
from src.services.WorkDayService import WorkDayService

wd_router = APIRouter(prefix='/workdays', tags=['WorkDay'])
wd_service = IService()


@wd_router.get('/', response_model=List[WorkDayDTO])
def get_all_days():
    return wd_service.get_all_wd()


@wd_router.get('/{pk}', response_model=List[WorkDayDTO])
def get_day_by_id(pk: int):
    try:
        return wd_service.get_wd(id=pk)
    except Exception as e:
        return HTTPException(status_code=500, detail=e)


@wd_router.post('/add')
def add_wd(wd: WorkDayAddDTO):
    try:
        res = wd_service.add_wd(wd)
    except IntegrityError as e:
        return HTTPException(status_code=400, detail=e)
    return res


@wd_router.delete('/{pk}')
def delete_wd(pk: int):
    try:
        wd_service.delete_wd(pk)
    except IntegrityError as e:
        return e
    except UnmappedInstanceError as e:
        return HTTPException(status_code=400, detail="Такого запису не існує")
    return {'status': 'OK'}


@wd_router.put('/{pk}')
def update_wd(pk: int, wd: WorkDayAddDTO):
    try:
        return wd_service.update_wd(pk, wd.dict())
    except UnmappedInstanceError as e:
        return HTTPException(status_code=400, detail=e)
