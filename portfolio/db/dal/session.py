from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from portfolio.BL.session_handlers import create_session_key
from portfolio.db.models import User, Session


class SessionDAL:

    def __init__(self, session: AsyncSession) -> None:
        self.db = session

    async def get_user_from_session(
        self, session_key: str
    ) -> User:
        q = select(
            Session
        ).where(
            Session.session_key == session_key
        ).options(
            selectinload(Session.user)
        )
        session = await self.db.scalars(q)
        session = session.one()
        print(session)

        return session.user

    async def create_session_key(self) -> Session:
        user = User(is_anonymous=True)
        session = Session(
            user=user,
            session_key=create_session_key(),
            uid=user.user_id,
        )

        self.db.add_all([user, session])
        await self.db.flush()

        return session
