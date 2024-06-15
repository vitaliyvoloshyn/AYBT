from typing import List

from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError

from src.schemas.schemas import RateTypeDTO, RateTypeAddDTO
from src.services import IService

rate_type_router = APIRouter(prefix='/rate_types', tags=['RateType'])
rate_type_service = IService()


@rate_type_router.get('/', response_model=List[RateTypeDTO])
def get_all_rate_types():
    return rate_type_service.get_all_rt()


@rate_type_router.get('/{pk}', response_model=List[RateTypeDTO])
def get_rate_type_by_id(pk: int):
    return rate_type_service.get_rt(id=pk)


@rate_type_router.post('/add')
def add_rate_type(rt: RateTypeAddDTO):
    try:
        res = rate_type_service.add_rt(rt)
        return res
    except IntegrityError as e:
        return e


@rate_type_router.delete('/delete')
def delete_rate_type(pk: int):
    rate_type_service.delete_rt(pk)
    return {'status': 'OK'}


@rate_type_router.patch('/{pk}')
def update_rate_type(pk: int, rt: RateTypeAddDTO):
    data_ = rt.dict()
    rate_type_service.update_rt(pk, data_)
    return {'status': 'OK'}
