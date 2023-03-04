from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.db.models import User
from portfolio.db.dal.user_info import UserInfoDAL
from portfolio.models import FullUserData


async def get_user_info(user: User, db: AsyncSession) -> FullUserData:
    async with db.begin():
        dal = UserInfoDAL(db)
        return await dal.get_user_info(user)
