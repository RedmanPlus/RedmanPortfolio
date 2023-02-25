from fastapi_mail import FastMail, MessageSchema, MessageType

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from portfolio.BL.session_handlers import (
    create_session_key,
    create_email_token,
)
from portfolio.db.models import User, Session, EmailToken
from portfolio.settings import mail_conf


class UserDAL:

    def __init__(self, session: AsyncSession) -> None:
        self.db = session
    
    async def create_user(self, email: str) -> User:
        user = User(
            email=email,
            is_anonymous=False,
        )

        token = EmailToken(
            user=user,
            bearer=user.user_id,
            key=create_email_token()
        )

        user.email_token = token

        self.db.add(user)
        self.db.add(token)
        await self.db.flush()

        message = MessageSchema(
            subject="Регистрация на сервисе",
            recipients=[user.email],
            body={"token": token.key},
            subtype=MessageType.html
        )

        fm = FastMail(mail_conf)
        await fm.send_message(
            message,
            template_name="templates/register_email.html"
        )

        return user

    async def update_user(
        self, user_id: int, username: str, password: str
    ) -> User:

        user = await self.get_user_by_id(user_id)

        user.username = username
        user.password = password

        self.db.add(user)
        await self.db.flush()

        return user

    async def get_user_by_id(self, user_id: int) -> User:

        query = select(User).where(User.user_id == user_id)

        results = await self.db.scalars(query)

        return results.first()

    async def get_user_by_email(self, user_email: str) -> User:

        query = select(User).where(User.email == user_email)

        results = await self.db.scalars(query)

        return results.first()


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
