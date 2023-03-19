from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.db.dal.workplace import WorkplaceDAL
from portfolio.db.models.user import User
from portfolio.models.workplace import NewWorkplace, UpdateWorkplace, WorkplaceInfo


async def get_user_workplace(
    user: User, db: AsyncSession
) -> List[WorkplaceInfo]:
    async with db.begin():

        dal = WorkplaceDAL(db)

        result = await dal.get_user_workplace(user)

        return [WorkplaceInfo.from_orm(obj) for obj in result]


async def add_user_workplace(
    user: User, data: NewWorkplace, db: AsyncSession
) -> NewWorkplace:
    async with db.begin():

        dal = WorkplaceDAL(db)

        result = await dal.add_user_workplace(user, data)

        if result is None:
            raise Exception(
                "You can't add workplaces, probably since you're not logged "
                "in or not created profile info"
            )

        return data


async def get_workplace_by_username(
    username: str, db: AsyncSession
) -> List[WorkplaceInfo]:
    async with db.begin():

        dal = WorkplaceDAL(db)

        result = await dal.get_workplace_by_username(username)

        return [WorkplaceInfo.from_orm(obj) for obj in result]


async def get_workplace_by_name(
    workplace_name: str, db: AsyncSession
) -> WorkplaceInfo:
    async with db.begin():

        dal = WorkplaceDAL(db)

        result = await dal.get_workplace_by_name(workplace_name)

        return WorkplaceInfo.from_orm(result)


async def update_workplace_by_name(
    user: User,
    workplace_name: str,
    data: UpdateWorkplace,
    db: AsyncSession
) -> WorkplaceInfo:
    async with db.begin():

        dal = WorkplaceDAL(db)

        result = await dal.update_workplace_by_name(user, workplace_name, data)

        if result is None:
            raise Exception(
                f"Workplace by name {workplace_name} doesnt' exist"
            )

        return WorkplaceInfo.from_orm(result)


async def delete_workplace_by_name(
    user: User, workplace_name: str, db: AsyncSession
) -> WorkplaceInfo:
    async with db.begin():

        dal = WorkplaceDAL(db)

        result = await dal.delete_workplace_by_name(user, workplace_name)

        return WorkplaceInfo.from_orm(result)
