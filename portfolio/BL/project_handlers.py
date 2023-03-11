from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.db.dal import ProjectDAL
from portfolio.db.models.user import User
from portfolio.models import BlockInfo, BlockM2M, LinkBlock, ProjectData, ProjectInfo, PublichProjectData, ShortUserData, UpdateProjectData


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


async def publish_project_by_id(
    user: User,
    username: str,
    project_id: int,
    data: PublichProjectData,
    db: AsyncSession
) -> ProjectInfo:
    async with db.begin():
        dal = ProjectDAL(db)

        project = await dal.publish_project_by_id(
            user, username, project_id, data
        )

        if project is None:
            raise Exception(
                "It seems you have no rights to modify this project"
            )

        return ProjectInfo.from_orm(project)


async def delete_project_by_id(
    user: User,
    username: str,
    project_id: int,
    db: AsyncSession
) -> ProjectInfo:
    async with db.begin():
        dal = ProjectDAL(db)

        project = await dal.delete_project_by_id(
            user, username, project_id 
        )

        if project is None:
            raise Exception(
                "It seems you have no rights to modify this project"
            )

        return ProjectInfo.from_orm(project)


async def get_project_blocks_by_id(
    user: User,
    username: str,
    project_id: int,
    db: AsyncSession
) -> List[BlockInfo]:
    async with db.begin():
        dal = ProjectDAL(db)

        blocks = await dal.get_project_blocks_by_id(
            user, username, project_id 
        )

        if blocks is None:
            raise Exception(
                "It seems you cannot access this project's blocks"
            )

        return [BlockInfo.from_orm(obj) for obj in blocks]


async def add_block_to_project(
    user: User,
    username: str,
    project_id: int,
    data: BlockInfo,
    db: AsyncSession
) -> BlockInfo:
    async with db.begin():
        dal = ProjectDAL(db)

        block = await dal.add_block_to_project(
            user, username, project_id, data
        )

        if block is None:
            raise Exception(
                "It seems you cannot access this project's blocks"
            )

        return BlockInfo.from_orm(block)


async def link_blocks_in_project(
    user: User,
    username: str,
    project_id: int,
    data: LinkBlock,
    db: AsyncSession
) -> BlockM2M:
    async with db.begin():
        dal = ProjectDAL(db)

        block_m2m = await dal.link_blocks_in_project(
            user, username, project_id, data
        )

        if block_m2m is None:
            raise Exception(
                "It seems you cannot access this project's blocks"
            )

        return BlockM2M.from_orm(block_m2m)


async def get_project_block_by_name(
    user: User,
    username: str,
    project_id: int,
    block_name: str,
    db: AsyncSession
) -> BlockInfo:
    async with db.begin():
        dal = ProjectDAL(db)

        block = await dal.get_project_block_by_name(
            user, username, project_id, block_name 
        )

        if block is None:
            raise Exception(
                "It seems this block doesn't exist"
            )

        return BlockInfo.from_orm(block)


async def update_project_block_by_name(
    user: User,
    username: str,
    project_id: int,
    block_name: str,
    data: BlockInfo,
    db: AsyncSession
) -> BlockInfo:
    async with db.begin():
        dal = ProjectDAL(db)

        block = await dal.update_project_block_by_name(
            user, username, project_id, block_name, data
        )

        if block is None:
            raise Exception(
                "It seems this block doesn't exist"
            )

        return BlockInfo.from_orm(block)


async def delete_project_block_by_name(
    user: User,
    username: str,
    project_id: int,
    block_name: str,
    db: AsyncSession
) -> BlockInfo:
    async with db.begin():
        dal = ProjectDAL(db)

        block = await dal.delete_project_block_by_name(
            user, username, project_id, block_name
        )

        if block is None:
            raise Exception(
                "It seems this block doesn't exist"
            )

        return BlockInfo.from_orm(block)
