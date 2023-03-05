from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from portfolio.db.models import User, Session, EmailToken
from portfolio.models import LoginUser


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


async def authenticate(
    user_data: LoginUser, db: AsyncSession
) -> User | None:
    async with db.begin():
        q = select(User).where(User.username == user_data.username)

        query = await db.scalars(q)
        user = query.first()

    if not verify_password(user_data.password, user.password):
        return None

    return user


async def _login(user: User, session: Session, db: AsyncSession):
    session.user = user
    session.uid = user.user_id

    db.add(session)


async def login(
    user: User, session: Session, db: AsyncSession
):
    if db.in_transaction():
        print("im in transaction")
        await _login(user, session, db)
    else:
        print("im not in transaction")
        async with db.begin():
            await _login(user, session, db)
            await db.commit()


async def handle_email_token(
    session: Session, token_key: str, db: AsyncSession
) -> User | None:
    async with db.begin():
        q = select(EmailToken) \
            .where(EmailToken.key == token_key) \
            .options(selectinload(EmailToken.user))
        query = await db.scalars(q)

        token = query.first()

        if not token:
            raise Exception()

        user = token.user

        await login(user, session, db)
        await db.delete(token)
        await db.flush()

    return user
