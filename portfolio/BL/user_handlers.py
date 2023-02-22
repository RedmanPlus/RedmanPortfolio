from portfolio.db.dal import UserDAL
from portfolio.models import InputUser, OutputUser


async def create_user(body: InputUser, session) -> OutputUser:
    
    async with session.begin():

        dal = UserDAL(session)
        user = await dal.create_user(**body.dict())

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
