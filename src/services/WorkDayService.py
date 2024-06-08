from typing import Type, List

from src.repositories.SQLRepository import SQLAlchemyRepository
from pydantic import BaseModel


class WorkDayService:
    def __init__(self, sql_repo: Type[SQLAlchemyRepository]):
        self.sql_repo = sql_repo()

    def add(self, dto: BaseModel) -> int:
        return self.sql_repo.add_obj(dto)

    def get_all(self):
        return self.sql_repo.get_all()

    def get_obj(self, **filter_by) -> List[BaseModel]:
        return self.sql_repo.get_obj(**filter_by)

    def delete(self, pk: int):
        self.sql_repo.delete(pk)
