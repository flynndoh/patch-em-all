from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from adapters.sqlmodel_fastapiuser import SQLModelUserDatabaseAsync
from adapters.sqlmodel_fastapiuser.access_token import SQLModelAccessTokenDatabaseAsync
from env import environment
from models import User, AccessToken

engine = create_async_engine(environment.dsn, echo=True, connect_args={"check_same_thread": False})


def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')


event.listen(engine.sync_engine, 'connect', _fk_pragma_on_connect)


async def create_db_and_tables() -> AsyncEngine:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    return engine


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)) -> AsyncGenerator[SQLModelUserDatabaseAsync, None]:
    yield SQLModelUserDatabaseAsync(session, User)


async def get_access_token_db(session: AsyncSession = Depends(get_async_session)) -> AsyncGenerator[SQLModelAccessTokenDatabaseAsync, None]:
    yield SQLModelAccessTokenDatabaseAsync(session, AccessToken)
