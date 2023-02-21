from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.db.models import User, Session
from portfolio.db.session import get_db
from portfolio.models import LoginUser


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


async def authenticate(
    user_data: LoginUser, db: AsyncSession = Depends(get_db)
) -> User | None:
    q = select(User).where(User.username == user_data.username)

    query = await db.scalars(q)
    user = query.first()

    if not verify_password(user_data.password, user.password):
        return None

    return user


async def login(
    user: User, session: Session, db: AsyncSession = Depends(get_db)
):

    session.user = user
    session.uid = user.user_id

    db.add(session)
    await db.commit()
