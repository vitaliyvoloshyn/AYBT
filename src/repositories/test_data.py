import datetime

from src.repositories.SQLRepository import WorDayRepository
from src.schemas.schemas import WorkDayAddDTO
from src.services.WorkDayService import WorkDayService

wd_add_dto = WorkDayAddDTO(date=datetime.date.today(),
                           day_of_week='Mo',
                           description='JOB')
wd_add_dto1 = WorkDayAddDTO(date=datetime.date.today(),
                            day_of_week='Tu',
                            description='JOB')

wds = WorkDayService(WorDayRepository)


def insert_data():
    print(wds.sql_repo.add_obj(wd_add_dto))
    print(wds.add(wd_add_dto1))


def get_all_wd():
    return wds.get_all()


def get_obj():
    return wds.get_obj(day_of_week='Tu')

def delete_id2():
    wds.delete(2)
