from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.db.models.link import Link
from portfolio.db.models.user import User
from portfolio.models import LinkInfo


class LinkDAL:

    def __init__(self, session: AsyncSession):

        self.session = session

    async def create_new_link(self, user: User, info: LinkInfo) -> Link:

        user_info = user.info
        link = Link(
            resource=info.resource,
            url=info.url,
            user_id=user_info.info_id
        )
        user_info.links.add(link)

        self.session.add(link)
        self.session.add(user_info)
        await self.session.flush()

        return link
