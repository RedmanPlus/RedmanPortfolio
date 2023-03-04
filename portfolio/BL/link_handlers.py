from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.db.dal import LinkDAL
from portfolio.db.models import User
from portfolio.models import LinkInfo


async def create_new_link(user: User, info: LinkInfo, db: AsyncSession) -> LinkInfo:
    async with db.begin():
        dal = LinkDAL(db)

        link = await dal.create_new_link(user, info)

        return LinkInfo(
            resource=link.resource,
            url=link.url
        )
