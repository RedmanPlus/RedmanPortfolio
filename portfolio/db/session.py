from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import settings

engine = create_async_engine(
    settings.REAL_DATABASE_URL,
    future=True,
    execution_options={"isolation_level": "AUTOCOMMIT"},
)

async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_db() -> Generator:

    try:
        session: AsyncSession = async_session()
        yield session

    finally:
        await session.close()

def get_session() -> AsyncSession:

    return async_session()
