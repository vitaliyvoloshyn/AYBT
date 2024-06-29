from datetime import date, timedelta
from pprint import pprint
from typing import List, Union, Sequence

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker

from src.db.database import db_session
from src.repositories.SQLRepository import SQLAlchemyRepository, WorDayRepository, RateRepository, RateValueRepository, \
    RateTypeRepository, PaymentRepository
from src.schemas.schemas import RateDTO, ReportDiffActualPlan, WagePerMonth, RateRelDTO, Wage, PaymentReportDTO, \
    TotalDiff, WDMonthViewDTO, WorkDayAddDTO, WorkDayDTO, MonthsDTO


class IService:
    wd_repository: WorDayRepository = WorDayRepository()
    rate_repository: SQLAlchemyRepository = RateRepository()
    rv_repository: SQLAlchemyRepository = RateValueRepository()
    rt_repository: SQLAlchemyRepository = RateTypeRepository()
    payment_repository: SQLAlchemyRepository = PaymentRepository()
    months = {
        1: "Січень",
        2: "Лютий",
        3: "Березень",
        4: "Квітень",
        5: "Травень",
        6: "Червень",
        7: "Липень",
        8: "Серпень",
        9: "Вересень",
        10: "Жовтень",
        11: "Листопад",
        12: "Грудень",
    }

    def __init__(self, session: sessionmaker = db_session):
        self.session = session

    # ______________________________CRUD WD____________________________________________________________________

    def add_wd(self, dto: BaseModel) -> Union[BaseModel, List[BaseModel]]:
        with self.session() as session:
            dto.__setattr__('day_of_week', self._get_weekday(dto.date))
            model = self.wd_repository.add_obj(session, dto)
            session.commit()
            return self.wd_repository.model_validate(model)

    def get_all_wd(self, **filter_by):
        with self.session() as session:
            return self.wd_repository.get_all(session, **filter_by)

    def get_wd(self, **filter_by) -> List[BaseModel]:
        with self.session() as session:
            return self.wd_repository.get_obj(session, **filter_by)

    def delete_wd(self, pk: int):
        with self.session() as session:
            self.wd_repository.delete(session, pk)
            session.commit()

    def update_wd(self, pk: int, data: dict):
        with self.session() as session:
            self.wd_repository.update(session, pk, **data)
            session.commit()
            return self.wd_repository.get_obj(session, id=pk)

    # _______________________________CRUD RateType___________________________________________________________

    def add_rt(self, dto: BaseModel) -> Union[BaseModel, List[BaseModel]]:
        with self.session() as session:
            model = self.rt_repository.add_obj(session, dto)
            session.commit()
            return self.rt_repository.model_validate(model)

    def get_all_rt(self):
        with self.session() as session:
            return self.rt_repository.get_all(session)

    def get_rt(self, **filter_by) -> List[BaseModel]:
        with self.session() as session:
            return self.rt_repository.get_obj(session, **filter_by)

    def delete_rt(self, pk: int):
        with self.session() as session:
            self.rt_repository.delete(session, pk)
            session.commit()

    def update_rt(self, pk: int, data: dict):
        with self.session() as session:
            self.rt_repository.update(session, pk, **data)
            session.commit()
            return self.rt_repository.get_obj(session, id=pk)

    # _______________________________CRUD RateValue___________________________________________________________

    def add_rv(self, dto: BaseModel) -> Union[BaseModel, List[BaseModel]]:
        with self.session() as session:
            dto.__setattr__('end_date', None)  # змінюємо кінцеву дату на None
            dto.__setattr__('start_date', date(dto.start_date.year, dto.start_date.month, 1))
            model = self.rv_repository.add_obj(session, dto)
            session.commit()
            return self.rv_repository.model_validate(model)

    def get_all_rv(self):
        with self.session() as session:
            return self.rv_repository.get_all(session)

    def get_rv(self, **filter_by) -> List[BaseModel]:
        with self.session() as session:
            return self.rv_repository.get_obj(session, **filter_by)

    def delete_rv(self, pk: int):
        with self.session() as session:
            try:
                rv = self.rv_repository.get_obj(session, id=pk)[0]
            except IndexError:
                raise TypeError('Ставки з таким ID в базі не знайдено')

            rv_list = self.rv_repository.get_all(session, rate_id=rv.rate_id)
            for index, rv_ in enumerate(rv_list):
                if rv_ == rv:
                    if index > 0:
                        self.rv_repository.update(session,
                                                  rv_list[index - 1].id,
                                                  end_date=rv_list[index].end_date)
            self.rv_repository.delete(session, pk)
            session.commit()

    def update_rv(self, pk: int, data: dict):
        with self.session() as session:
            self.rv_repository.update(session, pk, **data)
            session.commit()
            return self.rv_repository.get_obj(session, id=pk)

    def change_rv(self, pk: int, dto: BaseModel):
        """Зміна ставки"""
        dto.__setattr__('start_date', date(dto.start_date.year, dto.start_date.month, 1))
        with self.session() as session:
            cur_rv = self.rv_repository.get_all(session, rate_id=dto.rate_id)
            if not cur_rv:
                raise TypeError('Ставки з таким ID в базі не знайдено')
            print(cur_rv[-1].start_date)
            print(dto.start_date)
            if cur_rv[-1].start_date >= dto.start_date:
                raise TypeError('Зміна ставки можлива тільки з наступного місяця')
            # add rate
            new_rv = self.rv_repository.add_obj(session, dto)
            # change rate
            self.rv_repository.update(session, cur_rv[-1].id, end_date=new_rv.start_date - timedelta(days=1))
            session.commit()
            return self.rv_repository.model_validate(new_rv)

    # _______________________________CRUD Rate___________________________________________________________

    def add_rate(self, dto: BaseModel) -> Union[BaseModel, List[BaseModel]]:
        with self.session() as session:
            model = self.rate_repository.add_obj(session, dto)
            session.commit()
            return self.rate_repository.model_validate(model)

    def get_all_rate(self, with_relation: bool = False):
        with self.session() as session:
            return self.rate_repository.get_all(session, with_relation)

    def get_rate(self, **filter_by) -> List[BaseModel]:
        with self.session() as session:
            return self.rate_repository.get_obj(session, **filter_by)

    def delete_rate(self, pk: int):
        with self.session() as session:
            rv_list = self.rv_repository.get_obj(session, rate_id=pk)
            for rv in rv_list:
                self.rv_repository.delete(session, rv.id)
            self.rate_repository.delete(session, pk)
            session.commit()

    def update_rate(self, pk: int, data: dict):
        with self.session() as session:
            self.rate_repository.update(session, pk, **data)
            session.commit()
            return self.rate_repository.get_obj(session, id=pk)

    # ______________________________CRUD Payment____________________________________________________________________

    def add_pmnt(self, dto: BaseModel) -> Union[BaseModel, List[BaseModel]]:
        with self.session() as session:
            dto.__setattr__('billing_date', date(dto.billing_date.year, dto.billing_date.month, 1))
            model = self.payment_repository.add_obj(session, dto)
            session.commit()
            return self.payment_repository.model_validate(model)

    def get_all_pmnt(self, **filter_by):
        with self.session() as session:
            return self.payment_repository.get_all(session, with_relation=True, **filter_by)

    def get_pmnt(self, **filter_by) -> List[BaseModel]:
        with self.session() as session:
            return self.payment_repository.get_obj(session, **filter_by)

    def delete_pmnt(self, pk: int):
        with self.session() as session:
            self.payment_repository.delete(session, pk)
            session.commit()

    def update_pmnt(self, pk: int, data: dict):
        with self.session() as session:
            self.payment_repository.update(session, pk, **data)
            session.commit()
            return self.payment_repository.get_obj(session, id=pk)

    # ________________________________UTILS____________________________________________________________

    def get_fact_wd_per_month(self, month: int, year: int) -> WDMonthViewDTO:
        """Повертає список фактично відпрацьованих днів за вказаний місяць"""
        begin = date(year, month, 1)
        end = date(year, month, 1) + relativedelta(months=1)
        with self.session() as session:
            days = self.wd_repository.get_all_wd_per_month_(session, begin, end)
        return WDMonthViewDTO(
            days_count=len(days),
            days=days,
            month_name=self._get_month_name(month),
            month_num=month,
            year=year)

    def get_plan_wd_per_month(self, month: int, year: int) -> WDMonthViewDTO:
        """Повертає список планових робочих днів за вказаний місяць"""
        days = []
        start_date = date(year, month, 1)
        end_date = self._get_end_date_of_month(month, year)
        while start_date <= end_date:
            if start_date.isoweekday() != 7:
                days.append(WorkDayDTO(
                    id=0,
                    date=start_date,
                    description='-',
                    day_of_week=self._get_weekday(start_date)
                ))
            start_date += timedelta(days=1)
        return WDMonthViewDTO(
            days_count=len(days),
            days=days,
            month_name=self._get_month_name(month),
            month_num=month,
            year=year)

    def get_wage_per_month(self, month: int, year: int, fact_wage: bool = True):
        """Повертає суму заробітньої плати за разрахунковий місяць за фактично відпрацьовані дні"""
        res = []
        wage = []
        sum_ = 0
        dates: WDMonthViewDTO = self.get_fact_wd_per_month(month, year)
        if not fact_wage:
            dates: WDMonthViewDTO = self.get_plan_wd_per_month(month, year)
        rates = self.get_all_rate(with_relation=True)
        daily_rate_wage = self._get_wage(self.define_daily_rate(rates, month, year), month, year, dates.days_count)
        month_rate_wage = self._get_wage(self.define_month_rate(rates, month, year), month, year, dates.days_count)
        single_prim_wage = self._get_wage(self.define_single_prim(rates, month, year), month, year, dates.days_count)
        single_fine_wage = self._get_wage(self.define_single_fine(rates, month, year), month, year, dates.days_count)
        wages = daily_rate_wage + month_rate_wage + single_fine_wage + single_prim_wage

        total = sum([i.value for i in wages])
        return WagePerMonth(total=total, wages=wages)

    def _get_wage(self, rates: List[RateRelDTO], month: int, year: int, days: int) -> List[Wage]:
        """Повертає заробітню плату за вибраний місяць"""
        out = []
        value = 0
        for rate in rates:
            value = rate.rate_values[0].value
            if rate.rate_type_id == 1:
                value *= days
            out.append(Wage(rate=rate, billing_date=date(year, month, 1), value=value))
        return out

    def get_fact_payments_per_month(self, month: int, year: int, billing: bool) -> PaymentReportDTO:
        """Повертає всі розрахункові виплати за вказаний місяць по кожній категорії"""
        payments_ = []
        total = 0
        payments = self.get_all_pmnt()
        start_date = date(year, month, 1)
        end_date = self._get_end_date_of_month(month, year)
        for payment in payments:
            check_date = payment.date
            if billing:
                check_date = payment.billing_date
            if start_date <= check_date <= end_date:
                payments_.append(payment)
                total += payment.value
        return PaymentReportDTO(total=total, payments=payments_)

    def summary_report_actual_planned(self, month: int, year: int) -> TotalDiff:
        """Порівнює фактичні і планові виплати"""
        res = []
        total_diff = 0
        diff = 0
        payments = self.get_fact_payments_per_month(month, year, billing=True)  # те, що вже отримав
        wages = self.get_wage_per_month(month, year)  # те, що я маю отримати

        for wage in wages.wages:
            payment_value = 0
            for payment in payments.payments:
                if payment.rate.name == wage.rate.name:
                    payment_value += payment.value
            diff = payment_value - wage.value
            total_diff += diff
            res.append(ReportDiffActualPlan(wage=wage, diff=diff))
        return TotalDiff(total_diff=total_diff, diff_wages=res)

    def define_daily_rate(self, rates: Sequence[BaseModel], month: int, year: int) -> List[RateRelDTO]:
        """Визначає розмір денної ставки для розрахункового місяця"""
        rate_ = []

        for rate in rates:
            out = None
            if rate.rate_type.id == 1:
                dto = rate.model_dump()
                dto['rate_values'] = []
                out = RateRelDTO(**dto)
                for value in rate.rate_values:
                    if value.end_date:
                        if value.start_date <= date(year, month, 1) <= value.end_date:
                            out.rate_values.append(value)
                    else:
                        if value.start_date <= date(year, month, 1):
                            out.rate_values.append(value)
                rate_.append(out)

        return rate_

    def define_single_fine(self, rates: Sequence[BaseModel], month: int, year: int) -> List[RateRelDTO]:
        """Визначає розмір разового вирахування для розрахункового місяця"""
        rate_ = []

        for rate in rates:
            out = None
            if rate.rate_type.id == 4:
                dto = rate.model_dump()
                dto['rate_values'] = []
                out = RateRelDTO(**dto)
                for value in rate.rate_values:
                    if value.start_date.month == month and value.start_date.year == year:
                        out.rate_values.append(value)
                rate_.append(out)

        return rate_

    def define_single_prim(self, rates: Sequence[BaseModel], month: int, year: int) -> List[RateRelDTO]:
        """Визначає розмір разового нарахування для розрахункового місяця"""
        rate_ = []

        for rate in rates:
            out = None
            if rate.rate_type.id == 3:
                dto = rate.model_dump()
                dto['rate_values'] = []
                out = RateRelDTO(**dto)
                for value in rate.rate_values:
                    if value.start_date.month == month and value.start_date.year == year:
                        out.rate_values.append(value)
                rate_.append(out)

        return rate_

    def define_month_rate(self, rates: Sequence[BaseModel], month: int, year: int) -> List[RateRelDTO]:
        """Визначає розмір місячної ставки"""
        rate_ = []

        for rate in rates:
            out = None
            if rate.rate_type.id == 2:
                dto = rate.model_dump()
                dto['rate_values'] = []
                out = RateRelDTO(**dto)
                for value in rate.rate_values:
                    if value.end_date:
                        if value.start_date <= date(year, month, 1) <= value.end_date:
                            out.rate_values.append(value)
                    else:
                        if value.start_date <= date(year, month, 1):
                            out.rate_values.append(value)
                rate_.append(out)
        return rate_

    @staticmethod
    def _get_period(month: int, year: int) -> bool:
        """Повертає True, якщо рахрахунковий період минулий, False - якщо поточний або майбутній"""
        if year < date.today().year or (year == date.today().year and month < date.today().month):
            return True
        return False

    @staticmethod
    def _get_weekday(date_: date) -> str:
        """Повертає назву дня тижня"""
        week = {
            1: 'Пн',
            2: 'Вт',
            3: 'Ср',
            4: 'Чт',
            5: 'Пт',
            6: 'Сб',
            7: 'Нд',
        }
        return week.get(date_.isoweekday())

    @staticmethod
    def _get_end_date_of_month(month: int, year: int) -> date:
        """Визначає останній день вказаного місяця"""
        cur_date = date(year, month, 28)
        while cur_date.month == month:
            cur_date += timedelta(days=1)
        return cur_date - timedelta(days=1)

    def _get_month_name(self, month_num: int) -> str:
        """Повертає назву місяця"""
        return self.months.get(month_num)

    def get_months(self) -> list[MonthsDTO]:
        """Повертає список місяців """
        lst = []
        for key, value in self.months.items():
            lst.append(MonthsDTO(num=key, name=value))
        return lst

    def month_for_view_wd(self, month: int, year: int) -> list[MonthsDTO]:
        """Повертає список місяців для view_wd +/- 5 місяців вперед/назад"""
        lst = []
        start = date(year, month, 1)
        for i in range(5, 0, -1):
            lst.append(MonthsDTO(
                name=self.months.get((start - relativedelta(months=i)).month),
                num=(start - relativedelta(months=i)).month,
                year=(start - relativedelta(months=i)).year
            )
            )
        for i in range(7):
            lst.append(MonthsDTO(
                name=self.months.get((start + relativedelta(months=i)).month),
                num=(start + relativedelta(months=i)).month,
                year=(start + relativedelta(months=i)).year
            )
            )

        return lst


if __name__ == '__main__':
    a = IService().month_for_view_wd(1)
    print(a)
