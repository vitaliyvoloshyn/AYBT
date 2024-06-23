from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class WorkDayAddDTO(BaseModel):
    date: date
    description: str
    day_of_week: Optional[str] = None


class WorkDayDTO(WorkDayAddDTO):
    id: int


class RateAddDTO(BaseModel):
    name: str
    rate_type_id: int


class RateDTO(RateAddDTO):
    id: int


class RateRelDTO(RateDTO):
    rate_values: List['RateValueDTO']
    rate_type: 'RateTypeDTO'


class RateValueAddDTO(BaseModel):
    value: int
    start_date: date
    end_date: Optional[date] = None
    rate_id: int


class RateValueDTO(RateValueAddDTO):
    id: int


class RateValueRelDTO(RateValueDTO):
    rate: 'RateDTO'


class RateTypeAddDTO(BaseModel):
    name: str


class RateTypeDTO(RateTypeAddDTO):
    id: int


class RateTypeRelDTO(RateTypeDTO):
    rates: List['RateDTO']


class PaymentAddDTO(BaseModel):
    date: date
    value: int
    billing_date: date
    rate_id: int


class PaymentDTO(PaymentAddDTO):
    id: int


class PaymentRelDTO(PaymentDTO):
    rate: 'RateDTO'


class ReportDiffActualPlan(BaseModel):
    rate: 'RateDTO'
    diff: int
    billing_date: date


class Wage(BaseModel):
    rate: 'RateRelDTO'
    billing_date: date
    value: int


class WagePerMonth(BaseModel):
    total: int
    wages: List['Wage']
