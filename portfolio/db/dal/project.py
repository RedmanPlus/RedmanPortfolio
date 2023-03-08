from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from portfolio.db.models.projects import Project

from portfolio.db.models.user import User
from portfolio.models import ProjectData


class ProjectDAL:

    def __init__(self, session: AsyncSession):

        self.session = session

    async def get_projects(self, user: User) -> Sequence[Project]:

        if user.is_anonymous:
            query = select(Project).where(Project.is_public == True)
        else:
            query = select(Project)\
                .where(
                    Project.is_public == True 
                    or Project.author == user.info
                )\
                .options(selectinload(Project.author))\
                .options(selectinload(Project.blocks))

        projects = await self.session.scalars(query)

        return projects.all()

    async def add_project(self, user: User, data: ProjectData) -> Project:

        info = user.info

        project = Project(
            project_name=data.project_name,
            is_public=False,
            author=info
        )

        self.session.add(project)
        await self.session.flush()

        return project

    async def get_users_projects(
        self, user: User, username: str
    ) -> Sequence[Project]:

        if user.username != username:
            query = select(Project).where(
                Project.author.user.username == username 
                and Project.is_public == True
            )\
            .options(selectinload(Project.author))\
            .options(selectinload(Project.blocks))
        else:
            query = select(Project).where(
                Project.author == user.info
            )\
            .options(selectinload(Project.author))\
            .options(selectinload(Project.blocks))

        projects = await self.session.scalars(query)

        return projects.all()
