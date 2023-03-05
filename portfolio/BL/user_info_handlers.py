from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.db.models import User
from portfolio.db.dal.user_info import UserInfoDAL
from portfolio.models import FullUserData, InfoData


async def get_user_info(user: User, db: AsyncSession) -> FullUserData:
    async with db.begin():
        dal = UserInfoDAL(db)
        return await dal.get_user_info(user)


async def add_user_data(
    user: User, data: InfoData, db: AsyncSession
) -> FullUserData:
    async with db.begin():

        dal = UserInfoDAL(db)

        user_info = await dal.create_user_info(user, data)

        return FullUserData(
            first_name=user_info.first_name,
            last_name=user_info.last_name,
            description=user_info.description,
            links=user_info._links,
            skills=user_info.skills
        )
