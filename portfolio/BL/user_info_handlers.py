from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.db.models import User
from portfolio.models import FullUserData


async def get_user_info(user: User, db: AsyncSession) -> FullUserData:
    async with db.begin():

        pass
