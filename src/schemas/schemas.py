import datetime
from typing import List, Optional

from pydantic import BaseModel


class WorkDayAddDTO(BaseModel):
    date: datetime.date
    description: str
    day_of_week: str


class WorkDayDTO(WorkDayAddDTO):
    id: int


class RateAddDTO(BaseModel):
    name: str
    type: int


class RateDTO(RateAddDTO):
    id: int


class RateRelDTO(RateDTO):
    ratevalues: List['RateValueDTO']


class RateValueAddDTO(BaseModel):
    value: int
    start_date: datetime.date
    end_date: Optional[datetime.date] = None
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
