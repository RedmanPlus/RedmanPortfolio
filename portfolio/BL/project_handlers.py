from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.db.dal import ProjectDAL
from portfolio.db.models.user import User
from portfolio.models import ProjectData, ProjectInfo, ShortUserData, UpdateProjectData


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


async def get_user_project_by_id(
    user: User, username: str, project_id: int, db: AsyncSession
) -> ProjectInfo:
    async with db.begin():
        dal = ProjectDAL(db)

        project = await dal.get_user_project_by_id(user, username, project_id)

        return ProjectInfo.from_orm(project)

async def update_user_project_by_id(
    user: User,
    username: str,
    project_id: int,
    data: UpdateProjectData,
    db: AsyncSession
) -> ProjectInfo:
    async with db.begin():
        dal = ProjectDAL(db)

        project = await dal.update_user_project_by_id(
            user, username, project_id, data
        )

        if project is None:
            raise Exception(
                "It seems you have no rights to modify this object"
            )

        return ProjectInfo.from_orm(project)
