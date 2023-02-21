from fastapi import Depends
from fastapi.requests import Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.db.models import User, Session
from portfolio.db.session import get_db


def user(request: Request) -> User:
    return request.state.user


async def session(
    request: Request, db: AsyncSession = Depends(get_db)
) -> Session | None:

    session_key = request.cookies.get("User-Session")

    q = select(Session).where(Session.session_key == session_key)

    result = await db.scalars(q)
    return result.first()
