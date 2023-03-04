from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.db.models import (
    User,
)
from portfolio.models import FullUserData, SkillInfo, LinkInfo


class UserInfoDAL:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_info(self, user: User) -> FullUserData:
        info = user.info
        skill_m2m = info.skills

        skills = []
        for m2m in skill_m2m:
            skill = m2m.skill
            skills.append(
                SkillInfo(
                    skill_name=skill.skill_name,
                    skill_lvl=m2m.skill_lvl
                )
            )

        links = [LinkInfo.from_orm(link) for link in info.links]

        return FullUserData(
            first_name=info.first_name,
            last_name=info.last_name,
            description=info.description,
            skills=skills,
            links=links
        )
