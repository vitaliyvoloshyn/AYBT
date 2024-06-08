from typing import List, Type, Sequence

from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.orm import sessionmaker

from src.db.database import db_session
from src.models.models import WorkDay, Base
from src.repositories import AbstractRepository
from src.schemas.schemas import WorkDayDTO


class SQLAlchemyRepository(AbstractRepository):
    model: Type[Base] = None
    dto: BaseModel = None

    def __init__(self, session: sessionmaker = db_session):
        self.session = session

    def add_obj(self, dto: BaseModel) -> int:
        with self.session() as session:
            m = self.model(**dto.dict())
            session.add(m)
            session.commit()
            return m.__getattribute__('id')

    def get_obj(self, **filter_by) -> List[BaseModel]:
        with self.session() as session:
            query = select(self.model).filter_by(**filter_by)
            res = session.execute(query).scalars().all()
            return self._model_validate(res)

    def get_all(self, *args, **kwargs) -> Sequence[BaseModel]:
        with self.session() as session:
            query = select(self.model)
            res: Sequence = session.execute(query).scalars().all()
            return res
            # return self._model_validate(res)

    def update(self, pk:int, data):

        with self.session() as session:
            stmt = update(self.model).filter_by(id=pk).values(**data)
            session.execute(stmt)
            session.commit()

    def delete(self, pk: int):
        with self.session() as session:
            orm_model = session.execute(select(self.model).filter_by(id=pk)).scalar()
            session.delete(orm_model)
            session.commit()

    def _model_validate(self, orm: Sequence[Base]) -> List[BaseModel]:
        return [self.dto.model_validate(row, from_attributes=True) for row in orm]


class WorDayRepository(SQLAlchemyRepository):
    model = WorkDay
    dto = WorkDayDTO
