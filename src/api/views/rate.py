from typing import List

from fastapi import APIRouter

from src.schemas.schemas import RateDTO, RateAddDTO
from src.services import IService

rate_router = APIRouter(prefix='/rates', tags=['Rate'])
rate_service = IService()


@rate_router.get('/', response_model=List[RateDTO])
def get_all_rates():
    return rate_service.get_all_rate()


@rate_router.post('/add')
def add_rate(r: RateAddDTO):
    return rate_service.add_rate(r)


@rate_router.delete('/delete')
def delete_rate(pk: int):
    rate_service.delete_rate(pk)
    return {'status': 'OK'}


@rate_router.patch('/{pk}')
def update_rate(pk: int, r: RateAddDTO):
    data_ = r.dict()
    rate_service.update_rate(pk, data_)
    return {'status': 'OK'}


@rate_router.get('/{pk}', response_model=List[RateDTO])
def get_rate_by_id(pk: int):
    return rate_service.get_rate(id=pk)
