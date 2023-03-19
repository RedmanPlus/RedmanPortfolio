from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from portfolio.db.models.user import User
from portfolio.db.models.user_info import UserInfo
from portfolio.db.models.workplace import Workplace
from portfolio.models.workplace import NewWorkplace, UpdateWorkplace, WorkplaceInfo


class WorkplaceDAL:

    def __init__(self, session: AsyncSession):
        self.session = session

    def validate_work_end(self, data: NewWorkplace | UpdateWorkplace):
        
        if all([
            data.work_end_date is None,
            data.is_current_workplace is None,
            isinstance(data, NewWorkplace)
        ]):
            raise Exception(
                "You must eather set a work end date"
                " or pick a workplace as current"
            )

        if all([
            data.work_end_date is None,
            data.is_current_workplace == False
        ]):
            raise Exception(
                "Please provide end date if this is not a current workplace"
            )

        if data.work_end_date is not None and data.is_current_workplace:
            raise Exception(
                "You must eather set a work end date"
                " or pick a workplace as current"
            )

    async def get_user_workplace(self, user: User) -> Sequence[Workplace]:
        
        if user.is_anonymous:
            raise Exception("Anonymous users can have no workplaces listed")

        info = user.info

        if info is None:
            raise Exception("User did not specify his profile info yet")

        query = select(Workplace) \
                .where(Workplace.worker == info) \
                .options(selectinload(Workplace.skills)) \
                .options(selectinload(Workplace.projects))

        workplaces = await self.session.scalars(query)

        return workplaces.all()

    async def add_user_workplace(
        self, user: User, data: NewWorkplace
    ) -> Workplace | None:
        if user.is_anonymous:
            return None

        info = user.info

        if info is None:
            return None

        self.validate_work_end(data)

        workplace = Workplace(
            workplace_name=data.workplace_name,
            work_start_date=data.work_start_date,
            work_end_date=data.work_end_date,
            is_current_workplace=data.is_current_workplace,
            company_link=data.company_link,
            workplace_decsription=data.workplace_description,
            worker=info
        )

        self.session.add(workplace)
        await self.session.flush()

        return workplace

    async def get_workplace_by_username(
        self, username: str
    ) -> Sequence[Workplace]:
        user_query = select(User) \
                    .where(User.username == username) \
                    .options(joinedload(User.info))

        user = await self.session.scalar(user_query)

        if user is None:
            raise Exception(
                "User by this username does not exist"
            )

        info = user.info

        if info is None:
            raise Exception(
                f"User by username {username} hasn't set a info object jet"
            )

        query = select(Workplace) \
                .where(Workplace.worker == info) \
                .options(selectinload(Workplace.projects)) \
                .options(selectinload(Workplace.skills))

        workplaces = await self.session.scalars(query)

        return workplaces.all()

    async def get_workplace_by_name(self, workplace_name: str) -> Workplace:

        query = select(Workplace) \
                .where(Workplace.workplace_name == workplace_name) \
                .options(selectinload(Workplace.projects)) \
                .options(selectinload(Workplace.skills))

        workplace = await self.session.scalar(query)

        return workplace

    async def update_workplace_by_name(
        self, user: User, workplace_name: str, data: UpdateWorkplace
    ) -> Workplace | None:

        query = select(Workplace) \
                .where(Workplace.workplace_name == workplace_name) \
                .options(
                    selectinload(Workplace.worker)
                    .selectinload(UserInfo.user)
                ) \
                .options(selectinload(Workplace.projects)) \
                .options(selectinload(Workplace.skills))

        workplace = await self.session.scalar(query)

        if workplace is None:
            return None

        if workplace.worker.user.username != user.username:
            raise Exception(
                "You have no rights to modify this workplace"
            )

        changing_end_status = True

        if all([
            data.work_end_date is not None,
            data.is_current_workplace is not None
        ]):
            self.validate_work_end(data)
        elif all([
            data.work_end_date is None,
            not data.is_current_workplace
        ]):
            changing_end_status = False

        if data.work_end_date is not None:
            data.is_current_workplace = False

        if data.is_current_workplace:
            data.work_end_date = None

        workplace.workplace_name = data.workplace_name \
            if data.workplace_name is not None \
            else workplace.workplace_name
        workplace.work_start_date = data.work_start_date \
            if data.work_start_date is not None \
            else workplace.work_start_date
        if changing_end_status:
            workplace.work_end_date = data.work_end_date
            workplace.is_current_workplace = data.is_current_workplace
        workplace.company_link = data.company_link \
            if data.company_link is not None \
            else workplace.company_link
        workplace.workplace_decsription = data.workplace_description \
            if data.workplace_description is not None \
            else workplace.workplace_description

        self.session.add(workplace)
        await self.session.flush()

        return workplace

    async def delete_workplace_by_name(
        self, user: User, workplace_name: str
    ) -> Workplace:
        
        if user.is_anonymous:
            raise Exception("You are not logged in")

        query = select(Workplace) \
                .where(Workplace.workplace_name == workplace_name) \
                .options(
                    selectinload(Workplace.worker)
                    .selectinload(UserInfo.user)
                ) \
                .options(selectinload(Workplace.projects)) \
                .options(selectinload(Workplace.skills))

        workplace = await self.session.scalar(query)

        if workplace is None:
            raise Exception(
                f"Workplace by name {workplace_name} does not exist"
            )

        if workplace.worker != user.info:
            raise Exception("You have no rights to modify this object")

        await self.session.delete(workplace)
        await self.session.flush()

        return workplace
