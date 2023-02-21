from portfolio.db.dal import UserDAL
from portfolio.models import InputUser, OutputUser


async def create_user(body: InputUser, session) -> OutputUser:
    
    async with session.begin():

        dal = UserDAL()
        user = await dal.create_user(**body.dict())

        return OutputUser(
            username=user.username,
            email=user.email
        )
