from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.db.models.user import User
from portfolio.db.models.workplace import Workplace
from portfolio.models.workplace import NewWorkplace


class WorkplaceDAL:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user_workplace(
        self, user: User, data: NewWorkplace
    ) -> Workplace | None:
        if user.is_anonymous:
            return None

        info = user.info

        if info is None:
            return None

        if data.work_end_date is None and not data.is_current_workplace:
            raise Exception(
                "You must eather set a work end date"
                " or pick a workplace as current"
            )

        if data.work_end_date is not None and data.is_current_workplace:
            raise Exception(
                "You must eather set a work end date"
                " or pick a workplace as current"
            )

        workplace = Workplace(
            workplace_name=data.workplace_name,
            work_start_date=data.work_start_date,
            work_end_date=data.work_end_date,
            is_current_workplace=data.is_current_workplace,
            company_link=data.company_link,
            workplace_decsription=data.workplace_description,
        )

        self.session.add(workplace)
        await self.session.flush()

        return workplace
