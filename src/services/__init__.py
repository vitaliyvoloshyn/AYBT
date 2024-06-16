from datetime import date, timedelta
from typing import List, Union, Sequence

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from src.db.database import db_session
from src.repositories.SQLRepository import SQLAlchemyRepository, WorDayRepository, RateRepository, RateValueRepository, \
    RateTypeRepository


class IService:
    wd_repository: SQLAlchemyRepository = WorDayRepository()
    rate_repository: SQLAlchemyRepository = RateRepository()
    rv_repository: SQLAlchemyRepository = RateValueRepository()
    rt_repository: SQLAlchemyRepository = RateTypeRepository()

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

    def get_all_wd_per_month(self, begin: date, end: date):
        with self.session() as session:
            return self.wd_repository.get_all_wd_per_month_(session, begin, end)

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

    # ________________________________UTILS____________________________________________________________

    def get_work_days_per_month(self, month: int, year: int) -> dict:
        """Якщо розрахунковий місяць більше/дорівнює поточному, повертається список дат без сьомого дня тижня (неділі)
         вказаного місяця, якщо менше поточного - список фактично відпрацьованих днів"""
        dates = {'days_count': 0, 'days': []}
        days = []
        last_period: bool
        start_date = date(year, month, 1)
        end_date = self._get_end_date_of_month(month, year)
        if not self._get_period(month, year):
            while start_date.month == month:
                if start_date.isoweekday() != 7:
                    days.append((start_date, self._get_weekday(start_date)))
                start_date += timedelta(days=1)
        else:
            days = self.get_all_wd_per_month(start_date, end_date)
        dates['days'] = days
        dates['days_count'] = len(days)
        return dates

    def get_wage_per_month(self, month: int, year: int):
        """Повертає повну суму заробітньої плати за рахрахунковий місяць"""
        res = []
        sum_ = 0
        dates: dict = self.get_work_days_per_month(month, year)
        rates = self.get_all_rate(with_relation=True)
        daily_rate = self.define_daily_rate(rates, month, year)
        month_rate = self.define_month_rate(rates, month, year)
        single_prim = self.define_single_prim(rates, month, year)
        single_fine = self.define_single_fine(rates, month, year)
        for rate_ in daily_rate:
            res.append({'name': rate_['name'], 'value': rate_['value'] * dates.get('days_count')})
        res.extend(month_rate)
        res.extend(single_prim)
        sum_ = sum(i['value'] for i in res)
        res.extend(single_fine)
        sum_fine = sum(i['value'] for i in single_fine)
        end_sum = sum_ - sum_fine
        return {'total': end_sum,
                'rates': res}

    def define_daily_rate(self, rates: Sequence[BaseModel], month: int, year: int) -> list:
        """Визначає розмір денної ставки для розрахункового місяця"""
        res = []

        for rate in rates:
            if rate.rate_type.id == 1:
                for value in rate.rate_values:
                    if value.end_date:
                        if value.start_date <= date(year, month, 1) <= value.end_date:
                            res.append({'name': str(rate.name), 'value': value.value})
                    else:
                        if value.start_date <= date(year, month, 1):
                            res.append({'name': str(rate.name), 'value': value.value})

        return res

    def define_single_fine(self, rates: Sequence[BaseModel], month: int, year: int) -> list:
        """Визначає розмір разового вирахування для розрахункового місяця"""
        res = []

        for rate in rates:
            if rate.rate_type.id == 4:
                for value in rate.rate_values:
                    if value.start_date.month == month and value.start_date.year == year:
                        res.append({'name': str(rate.name), 'value': value.value})
        return res

    def define_single_prim(self, rates: Sequence[BaseModel], month: int, year: int) -> list:
        """Визначає розмір разового нарахування для розрахункового місяця"""
        res = []

        for rate in rates:
            if rate.rate_type.id == 3:
                for value in rate.rate_values:
                    if value.start_date.month == month and value.start_date.year == year:
                        res.append({'name': str(rate.name), 'value': value.value})
        return res

    def define_month_rate(self, rates: Sequence[BaseModel], month: int, year: int) -> list:
        """Визначає розмір місячної ставки"""
        res = []
        for rate in rates:
            if rate.rate_type.id == 2:
                for value in rate.rate_values:
                    if value.end_date:
                        if value.start_date <= date(year, month, 1) <= value.end_date:
                            res.append({'name': str(rate.name), 'value': value.value})
                    else:
                        if value.start_date <= date(year, month, 1):
                            res.append({'name': str(rate.name), 'value': value.value})

        return res

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
