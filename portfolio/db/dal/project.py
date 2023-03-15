from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from portfolio.db.models.projects import BlockBlockM2M, Project, ProjectBlock
from portfolio.db.models.skill import Skill, SkillBlockM2M
from portfolio.db.models.user import User
from portfolio.db.models.user_info import UserInfo
from portfolio.models import (
    BlockInfo,
    LinkBlock,
    ProjectData,
    PublichProjectData,
    UpdateProjectData
)


class ProjectDAL:

    def __init__(self, session: AsyncSession):

        self.session = session

    async def _get_project_by_id(self, project_id: int) -> Project:
        
        query = select(Project)\
            .where(Project.project_id == project_id)\
            .options(selectinload(Project.author))\
            .options(
                selectinload(Project.blocks)\
                .selectinload(ProjectBlock.blocks)
            )

        return await self.session.scalar(query)

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
        
        project = await self._get_project_by_id(project_id)

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

        project = await self._get_project_by_id(project_id)

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
        
        return await self._get_project_by_id(project_id)

    async def publish_project_by_id(
        self,
        user: User,
        username: str,
        project_id: int,
        data: PublichProjectData
    ) -> Project | None:

        project = await self._get_project_by_id(project_id)

        if project is None:
            return None

        if user.username != username:
            return None

        project.is_public = data.is_public

        self.session.add(project)

        await self.session.flush()

        return project

    async def delete_project_by_id(
        self,
        user: User,
        username: str,
        project_id: int,
    ) -> Project | None:

        project = await self._get_project_by_id(project_id)

        if project is None:
            return None

        if user.username != username:
            return None


        await self.session.delete(project)
        await self.session.flush()

        return project

    async def get_project_blocks_by_id(
        self,
        user: User,
        username: str,
        project_id: int,
    ) -> Sequence[ProjectBlock] | None:

        project = await self._get_project_by_id(project_id)
        
        if project is None:
            return None

        if user.username != username and not project.is_public:
            return None

        return project.blocks
    
    async def add_block_to_project(
        self,
        user: User,
        username: str,
        project_id: int,
        data: BlockInfo
    ) -> ProjectBlock | None:

        project = await self._get_project_by_id(project_id)
        
        if project is None:
            return None

        if user.username != username and not project.is_public:
            return None

        block = ProjectBlock(block_name=data.block_name, project=project)

        block.block_author = data.block_author \
            if data.block_author is not None else None
        block.block_description = data.block_description \
            if data.block_description is not None else None
        
        if data.skills is not None:
            for obj in data.skills:
                query = select(Skill) \
                    .where(Skill.skill_name == obj.skill_name)

                skill = await self.session.scalar(query)

                if skill is None:
                    raise Exception(
                        f"Skill by name {obj.skill_name} doesn't exist"
                    )

                m2m = SkillBlockM2M(skill=skill, block=block)
                self.session.add(m2m)

        self.session.add(block)
        await self.session.flush()

        project = await self._get_project_by_id(project_id)

        for block in project.blocks:
            if block.block_name == data.block_name:
                return block

    async def link_blocks_in_project(
        self,
        user: User,
        username: str,
        project_id: int,
        data: LinkBlock
    ) -> BlockBlockM2M | None:

        project = await self._get_project_by_id(project_id)

        if project is None:
            return None

        if user.username != username and not project.is_public:
            return None

        linked_blocks = []
        for block in project.blocks:
            if block.block_name == data.block_1_name \
                    or block.block_name == data.block_2_name:
                linked_blocks.append(block)

        if len(linked_blocks) != 2:
            return None

        m2m = BlockBlockM2M(
            left_block=linked_blocks[0],
            right_block=linked_blocks[1]
        )

        self.session.add(m2m)
        await self.session.flush()

        return m2m

    async def get_project_block_by_name(
        self,
        user: User,
        username: str,
        project_id: int,
        block_name: str
    ) -> Sequence[ProjectBlock] | None:

        project = await self._get_project_by_id(project_id)
        
        if project is None:
            return None

        if user.username != username and not project.is_public:
            return None

        for block in project.blocks:
            if block.block_name == block_name:
                return block

    async def update_project_block_by_name(
        self,
        user: User,
        username: str,
        project_id: int,
        block_name: str,
        data: BlockInfo
    ) -> ProjectBlock | None:

        project = await self._get_project_by_id(project_id)
        
        if project is None:
            return None

        if user.username != username and not project.is_public:
            return None

        for block in project.blocks:
            if block.block_name == block_name:
                block.block_name = data.block_name \
                    if data.block_name is not None \
                    else block.block_name
                block.block_description = data.block_description \
                    if data.block_description is not None \
                    else block.block_description
                block.skills = data.skills \
                    if data.skills is not None \
                    else block.skills
                if data.block_author is not None:
                    author_query = select(UserInfo) \
                    .where(
                        UserInfo.first_name == data.block_author.first_name
                        and UserInfo.last_name == data.block_author.last_name
                    )
                    author = await self.session.scalar(author_query)
                    if author is None:
                        return None
                    block.block_author = author

                self.session.add(block)
                await self.session.flush()

                return block

    async def delete_project_block_by_name(
        self,
        user: User,
        username: str,
        project_id: int,
        block_name: str
    ) -> Sequence[ProjectBlock] | None:

        project = await self._get_project_by_id(project_id)
        
        if project is None:
            return None

        if user.username != username and not project.is_public:
            return None

        for block in project.blocks:
            if block.block_name == block_name:
                await self.session.delete(block)
                await self.session.flush()

                return block
