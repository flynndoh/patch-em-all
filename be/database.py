from sqlalchemy import Engine
from sqlmodel import create_engine, SQLModel, Session

engine = create_engine("sqlite:///patch-em-all.sqlite", echo=True, connect_args={"check_same_thread": False})


def create_db_and_tables() -> Engine:
    SQLModel.metadata.create_all(engine)
    return engine


def get_session():
    with Session(engine) as session:
        yield session
