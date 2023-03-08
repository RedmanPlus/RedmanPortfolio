from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.db.dal import ProjectDAL
from portfolio.db.models.user import User
from portfolio.models import ProjectData, ProjectInfo, ShortUserData


async def get_projects(user: User, db: AsyncSession) -> List[ProjectInfo]:
    async with db.begin():
        dal = ProjectDAL(db)

        projects = await dal.get_projects(user)
        
        return [ProjectInfo.from_orm(obj) for obj in projects]


async def add_project(
    user: User, data: ProjectData, db: AsyncSession
) -> ProjectInfo:
    async with db.begin():
        dal = ProjectDAL(db)

        project = await dal.add_project(user, data)
        print(project.author)

        return ProjectInfo(
            project_name=project.project_name,
            author=ShortUserData.from_orm(project.author),
            is_public=project.is_public
        )

async def get_users_projects(
    user: User, username: str, db: AsyncSession
) -> List[ProjectInfo]:
    async with db.begin():
        dal = ProjectDAL(db)

        projects = await dal.get_users_projects(user, username)

        return [ProjectInfo.from_orm(obj) for obj in projects]
