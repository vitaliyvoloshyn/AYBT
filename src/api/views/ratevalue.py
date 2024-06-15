from typing import List

from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError

from src.schemas.schemas import RateValueDTO, RateValueAddDTO
from src.services import IService

rate_value_router = APIRouter(prefix='/rate_values', tags=['RateValue'])
rate_value_service = IService()


@rate_value_router.get('/', response_model=List[RateValueDTO])
def get_all_rate_vales():
    return rate_value_service.get_all_rv()


@rate_value_router.get('/{pk}', response_model=List[RateValueDTO])
def get_rate_value_by_id(pk: int):
    return rate_value_service.get_rv(id=pk)


@rate_value_router.post('/add')
def add_rate_value(rv: RateValueAddDTO):
    try:
        res = rate_value_service.add_rv(rv)
        return res
    except IntegrityError as e:
        return e


@rate_value_router.delete('/delete')
def delete_rate_value(pk: int):
    rate_value_service.delete_rv(pk)
    return {'status': 'OK'}


@rate_value_router.patch('/{pk}')
def update_rate_value(pk: int, rv: RateValueAddDTO):
    data_ = rv.dict()
    rate_value_service.update_rv(pk, data_)
    return {'status': 'OK'}

@rate_value_router.post('/{pk}')
def change_rv(pk: int, rv: RateValueAddDTO):
    try:
        res = rate_value_service.change_rv(pk, rv)
    except TypeError as e:
        print(e)
        return {'error': str(e)}
    return res
