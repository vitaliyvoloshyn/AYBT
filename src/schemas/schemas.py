from datetime import date
from typing import List, Optional, Any

from pydantic import BaseModel, Field


class WorkDayAddDTO(BaseModel):
    date: date
    description: str
    day_of_week: Optional[str] = None


class WorkDayDTO(WorkDayAddDTO):
    id: int


class WDMonthViewDTO(BaseModel):
    days_count: int
    days: List[WorkDayDTO]
    month_name: str
    month_num: int
    year: int
    report_name: str


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
    value: int = Field(ge=1)
    billing_date: date
    rate_id: int


class PaymentDTO(PaymentAddDTO):
    id: int


class PaymentRelDTO(PaymentDTO):
    rate: 'RateRelDTO'


class PaymentReportDTO(BaseModel):
    total: int
    payments: List['PaymentRelDTO']

    def __sub__(self, other: 'WagePerMonth') -> 'WagePerMonth':
        res = other.model_copy()
        total: int = 0
        for index in range(len(res.wages), 0, -1):
            category_sum = 0
            for payment in self.payments:
                if res.wages[index - 1].rate.name == payment.rate.name:
                    category_sum += payment.value
            res.wages[index - 1].value = category_sum - res.wages[index - 1].value
            total += res.wages[index - 1].value
            # видалення wage, в яких value дорівнює 0
            # if not res.wages[index - 1].value:
            #     res.wages.pop(index - 1)
        res.total = total
        return res


class WagePerMonth(BaseModel):
    total: int
    wages: List['Wage']


class Wage(BaseModel):
    rate: 'RateRelDTO'
    billing_date: date
    value: int


class ReportDiffActualPlan(BaseModel):
    wage: 'Wage'
    diff: int


class TotalDiff(BaseModel):
    total_diff: int
    diff_wages: List['ReportDiffActualPlan']


class MonthsDTO(BaseModel):
    num: int
    name: str
    year: Optional[int] = None


class PaymentAnalysisDTO(BaseModel):
    month_num: int
    month_name: str
    year: int
    wage: 'WagePerMonth'
    payment: 'PaymentReportDTO'
    diff: 'WagePerMonth'


class AllPaymentAnalysisDTO(BaseModel):
    total: int
    paDTO: List['PaymentAnalysisDTO']

