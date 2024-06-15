from src.services import IService


class RateService(IService):
    def get_wage_per_month(self, month: int, year: int):
        month_dates = self.get_work_days_per_month(month, year)
        rates = self.sql_repo.get_all(with_relation=True)
        return rates
