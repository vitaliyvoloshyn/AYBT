from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime


class Base(DeclarativeBase):
    pass


class WorkDay(Base):
    __tablename__ = 'workdays'
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(unique=True)
    day_of_week: Mapped[str]
    description: Mapped[str]


class RateType(Base):
    __tablename__ = 'rate_types'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    rates: Mapped[List['Rate']] = relationship(back_populates='rate_type')


class Rate(Base):
    __tablename__ = 'rates'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    rate_type_id: Mapped[int] = mapped_column(ForeignKey('rate_types.id'))
    rate_type: Mapped['RateType'] = relationship(back_populates='rates')
    rate_values: Mapped[List['RateValue']] = relationship(back_populates='rate')


class RateValue(Base):
    __tablename__ = 'rate_values'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int]
    start_date: Mapped[datetime]
    end_date: Mapped[datetime] = mapped_column(nullable=True)
    rate_id: Mapped[int] = mapped_column(ForeignKey('rates.id'))
    rate: Mapped['Rate'] = relationship(back_populates='rate_values')
