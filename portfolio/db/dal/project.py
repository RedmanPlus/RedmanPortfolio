from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from portfolio.db.models.projects import Project, ProjectBlock

from portfolio.db.models.user import User
from portfolio.models import ProjectData, UpdateProjectData


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

    async def get_user_project_by_id(
        self, user: User, username: str, project_id: int
    ) -> Project | None:

        query = select(Project)\
            .where(Project.project_id == project_id)\
            .options(selectinload(Project.author))\
            .options(selectinload(Project.blocks))

        project = await self.session.scalar(query)

        if project is None:
            return None
        
        if username != user.username and not project.is_public:
            return None

        return project

    async def update_user_project_by_id(
        self,
        user: User,
        username: str,
        project_id: int,
        data: UpdateProjectData
    ) -> Project | None:

        query = select(Project)\
            .where(Project.project_id == project_id)\
            .options(selectinload(Project.author))\
            .options(selectinload(Project.blocks))

        project = await self.session.scalar(query)

        if project is None:
            return None

        if username != user.username and not project.is_public:
            return None
        
        if data.blocks is not None:
            for block in data.blocks:
                block = ProjectBlock(
                    block_name=block.block_name,
                    project=project,
                )
                self.session.add(block)

        project.project_name = data.project_name \
            if data.project_name is not None \
            else project.project_name
        project.short_description = data.short_description \
            if data.short_description is not None \
            else project.short_description
        project.full_description = data.full_description \
            if data.full_description is not None \
            else project.full_description
        project.project_logo = data.project_logo \
            if data.project_logo is not None \
            else project.project_logo

        self.session.add(project)
        await self.session.flush()
        
        query = select(Project)\
            .where(Project.project_id == project_id)\
            .options(selectinload(Project.author))\
            .options(selectinload(Project.blocks))

        project = await self.session.scalar(query)

        return project
