from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from portfolio.db.models.projects import BlockBlockM2M, Project


class BlockRelationsDAL:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_project_relations(
        self, project: Project
    ) -> Sequence[BlockBlockM2M]:
        query = select(BlockBlockM2M) \
            .where(
                BlockBlockM2M.left_id.in_(
                    [block.block_id for block in project.blocks]
                ) 
                | BlockBlockM2M.right_id.in_(
                    [block.block_id for block in project.blocks]
                )
            ) \
            .options(selectinload(BlockBlockM2M.left)) \
            .options(selectinload(BlockBlockM2M.right))

        relations = await self.session.scalars(query)
        print(relations)
        return relations.all()
