from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.db.models import (
    User,
    Link,
    Skill,
    SkillUserM2M
)
from portfolio.db.models.user_info import UserInfo
from portfolio.models import (
    FullUserData,
    InfoData,
    SkillInfo,
    LinkInfo
)


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

    async def create_user_info(self, user: User, data: InfoData) -> UserInfo:

        info = UserInfo(
            user=user,
            first_name=data.first_name,
            last_name=data.last_name,
            description=data.descrption
        )
        print(user.info)
        self.session.add(user)

        print([obj.skill_id for obj in data.skill_ids])
        skill_query = select(Skill)\
            .where(Skill.skill_id.in_(
                tuple([obj.skill_id for obj in data.skill_ids])
            ))

        skills = await self.session.scalars(skill_query)
        skills = skills.unique().all()

        skill_lvls = [obj.skill_lvl for obj in data.skill_ids]

        for skill, lvl in zip(skills, skill_lvls):

            m2m = SkillUserM2M(
                skill=skill,
                skill_lvl=lvl,
                user=info
            )
            print(m2m)
            info.skills.append(m2m)
            self.session.add(m2m)
        print(info.skills)
        links = [
            Link(resource=obj.resource, url=obj.url, _user=info)
            for obj in data.links
        ]
        self.session.add_all(links)
        for link in links:
            info._links.append(link)

        self.session.add(info)
        await self.session.flush()

        return info
