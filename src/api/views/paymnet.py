from typing import List

from fastapi import APIRouter

from src.schemas.schemas import PaymentDTO, PaymentAddDTO
from src.services import IService

pmnt_router = APIRouter(prefix='/payments', tags=['Payment'])
pmnt_service = IService()


@pmnt_router.get('/', response_model=List[PaymentDTO])
def get_all_pmnts():
    return pmnt_service.get_all_pmnt()


@pmnt_router.post('/add')
def add_pmnt(pmnt: PaymentAddDTO):
    return pmnt_service.add_pmnt(pmnt)


@pmnt_router.delete('/delete')
def delete_pmnt(pk: int):
    pmnt_service.delete_pmnt(pk)
    return {'status': 'OK'}


@pmnt_router.patch('/{pk}')
def update_pmnt(pk: int, pmnt: PaymentAddDTO):
    data_ = pmnt.dict()
    pmnt_service.update_pmnt(pk, data_)
    return {'status': 'OK'}


@pmnt_router.get('/{pk}', response_model=List[PaymentDTO])
def get_pmnt_by_id(pk: int):
    return pmnt_service.get_pmnt(id=pk)
