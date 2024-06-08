from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.models import Base

engine = create_engine("sqlite:///aybt.db", echo=True)
db_session = sessionmaker(engine)


def create_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    drop_db()
    create_db()
