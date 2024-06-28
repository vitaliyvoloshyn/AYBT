from datetime import date
from typing import List, Type, Sequence, Union

from pydantic import BaseModel
from sqlalchemy import select, update, and_
from sqlalchemy.orm import sessionmaker, Session

from src.db.database import db_session
from src.models.models import WorkDay, Base, Rate, RateType, RateValue, Payment
from src.repositories import AbstractRepository
from src.schemas.schemas import WorkDayDTO, RateDTO, RateTypeDTO, RateValueDTO, RateRelDTO, PaymentDTO, PaymentAddDTO, \
    PaymentRelDTO


class SQLAlchemyRepository(AbstractRepository):
    model: Type[Base] = None
    dto: BaseModel = None
    rel_dto: BaseModel = None

    def __init__(self, session: sessionmaker = db_session):
        self.session = session

    def add_obj(self, session: Session, dto: BaseModel) -> Base:
        model = self.model(**dto.dict())
        session.add(model)
        return model

    def get_obj(self, session: Session, with_relation: bool = False, **filter_by) -> List[BaseModel]:
        query = select(self.model).filter_by(**filter_by)
        res = session.execute(query).scalars().all()
        return self.model_validate(res, with_relation)

    def get_all(self, session: Session, with_relation: bool = False, **filter_by) -> Sequence[BaseModel]:
        query = select(self.model).filter_by(**filter_by)
        res: Sequence = session.execute(query).scalars().all()
        return self.model_validate(res, with_relation)

    def update(self, session: Session, pk: int, **data):
        stmt = update(self.model).filter_by(id=pk).values(**data)
        session.execute(stmt)

    def delete(self, session: Session, pk: int):
        orm_model = session.execute(select(self.model).filter_by(id=pk)).scalar()
        session.delete(orm_model)

    def model_validate(self, orm: Union[Base, Sequence[Base]], with_relation: bool = False) \
            -> Union[BaseModel, List[BaseModel]]:
        dto = self.dto
        if with_relation:
            dto = self.rel_dto
        if isinstance(orm, (list, Sequence)):
            return [dto.model_validate(row, from_attributes=True) for row in orm]
        return self.dto.model_validate(orm, from_attributes=True)


class WorDayRepository(SQLAlchemyRepository):
    model = WorkDay
    dto = WorkDayDTO

    def get_all_wd_per_month_(self, session: Session, begin: date, end: date) -> List[BaseModel]:
        query = select(self.model).filter(and_(self.model.date < end, self.model.date >= begin))
        res = session.execute(query).scalars().all()
        return self.model_validate(res)


class RateRepository(SQLAlchemyRepository):
    model = Rate
    dto = RateDTO
    rel_dto = RateRelDTO


class RateTypeRepository(SQLAlchemyRepository):
    model = RateType
    dto = RateTypeDTO


class RateValueRepository(SQLAlchemyRepository):
    model = RateValue
    dto = RateValueDTO


class PaymentRepository(SQLAlchemyRepository):
    model = Payment
    dto = PaymentDTO
    rel_dto = PaymentRelDTO
