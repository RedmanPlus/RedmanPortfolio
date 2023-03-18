from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.db.dal.workplace import WorkplaceDAL
from portfolio.db.models.user import User
from portfolio.models.workplace import NewWorkplace, WorkplaceInfo


async def add_user_workplace(
    user: User, data: NewWorkplace, db: AsyncSession
) -> WorkplaceInfo:
    async with db.begin():

        dal = WorkplaceDAL(db)

        result = await dal.add_user_workplace(user, data)

        if result is None:
            raise Exception(
                "You can add workplaces, cause you're not logged in "
                "or not created profile info"
            )

        return WorkplaceInfo.from_orm(result)
