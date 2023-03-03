from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.db.models import (
    User,
    UserInfo,
    Skill,
    SkillUserM2M,
    Link
)


class UserInfoDAL:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_info(user: User) -> UserInfo:

        info: UserInfo = user.info
        skill_m2m = info.skills
        skills = [m2m.skill for m2m in skill_m2m]

