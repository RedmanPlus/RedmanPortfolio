from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.db.models.projects import BlockBlockM2M, Project


class BlockRelationsDAL:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_project_relations(
        self, project: Project
    ) -> Sequence[BlockBlockM2M]:
        query = select(BlockBlockM2M) \
            .where(
                BlockBlockM2M.left.project_id == project.project_id 
                or BlockBlockM2M.right.project_id == project.project_id
            )

        relations = await self.session.scalars(query)
        print(relations)
        return relations.all()
