from fastapi_mail import FastMail, MessageSchema, MessageType

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from portfolio.BL.session_handlers import create_email_token
from portfolio.db.models import User, EmailToken
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
            tempalate_body={"token": token.key},
            subtype=MessageType.html
        )

        fm = FastMail(mail_conf)
        await fm.send_message(
            message,
            template_name="register_email.html"
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
