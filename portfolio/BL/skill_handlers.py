from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.db.dal import SkillDAL
from portfolio.models import SkillInfo, SkillData, BaseSkillInfo


async def get_skills(db: AsyncSession) -> List[BaseSkillInfo]:
    async with db.begin():

        dal = SkillDAL(db)

        skills = await dal.get_skills()

        skills = [BaseSkillInfo.from_orm(obj) for obj in skills]

        return skills


async def create_skill(data: SkillData, db: AsyncSession) -> SkillInfo:
    async with db.begin():

        dal = SkillDAL(db)

        skill = await dal.create_skill(data)

        return SkillInfo.from_orm(skill)
