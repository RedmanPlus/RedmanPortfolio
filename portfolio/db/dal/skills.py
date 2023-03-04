from typing import Sequence
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.db.models.skill import Skill
from portfolio.models import SkillData


class SkillDAL:

    def __init__(self, session: AsyncSession):

        self.session = session

    async def get_skills(self) -> Sequence[Skill]:

        query = select(Skill)

        skills = await self.session.scalars(query)

        return skills.fetchall()

    async def create_skill(self, data: SkillData) -> Skill:

        skill = Skill(
            skill_name=data.skill_name
        )

        self.session.add(skill)

        await self.session.flush()

        return skill
