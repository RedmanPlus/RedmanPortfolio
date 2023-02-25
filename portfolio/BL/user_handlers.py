from portfolio.BL.auth_handlers import hash_password
from portfolio.db.dal import UserDAL
from portfolio.models import InputUser, OutputUser, NewOutputUser, UserData


async def create_user(body: InputUser, session) -> NewOutputUser:
    
    async with session.begin():

        dal = UserDAL(session)
        user = await dal.create_user(**body.dict())

        return NewOutputUser(
            email=user.email
        )


async def update_user(user_id: int, body: UserData, session) -> OutputUser:

    async with session.begin():

        dal = UserDAL(session)
        if body.password_1 != body.password_2:
            raise Exception()

        hashed_password = hash_password(body.password_1)

        user = await dal.update_user(
            user_id=user_id,
            username=body.username,
            password=hashed_password
        )

        return OutputUser(
            username=user.username,
            email=user.email
        )


async def get_user_by_id(user_id: int, session) -> OutputUser:

    async with session.begin():

        dal = UserDAL(session)

        user = await dal.get_user_by_id(user_id)

        if user is None:
            raise Exception()

        return OutputUser(
            username=user.username,
            email=user.email,
        )


async def get_user_by_email(user_email: str, session) -> OutputUser:

    async with session.begin():

        dal = UserDAL(session)

        user = dal.get_user_by_email(user_email)

        if user is None:
            raise Exception()

        return OutputUser(
            username=user.username,
            email=user.email,
        )
