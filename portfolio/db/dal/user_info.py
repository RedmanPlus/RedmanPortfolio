from typing import Tuple

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
    NewSkillInfo,
    SkillData,
    SkillInfo,
    LinkInfo,
    UpdateUserData
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

        links = [LinkInfo.from_orm(link) for link in info._links]

        return FullUserData(
            first_name=info.first_name,
            last_name=info.last_name,
            description=info.description,
            photo_link=info.photo_link,
            skills=skills,
            links=links
        )

    async def create_user_info(
        self, user: User, data: InfoData
    ) -> Tuple[UserInfo, SkillUserM2M, Link]:

        info = UserInfo(
            user=user,
            first_name=data.first_name,
            last_name=data.last_name,
            description=data.descrption
        )
        user.info = info
        self.session.add(user)
        
        skill_query = select(Skill)\
            .where(Skill.skill_id.in_(
                tuple([obj.skill_id for obj in data.skill_ids])
            ))

        skills = await self.session.scalars(skill_query)
        skills = skills.unique().fetchall()
        skill_lvls = [obj.skill_lvl for obj in data.skill_ids]

        for skill, lvl in zip(skills, skill_lvls):
            m2m = SkillUserM2M(
                skill=skill,
                skill_lvl=lvl,
                user=info
            )
            self.session.add(m2m)
        links = [
            Link(resource=obj.resource, url=obj.url, _user=info)
            for obj in data.links
        ]
        self.session.add_all(links)

        self.session.add(info)
        await self.session.flush()

        return info, skills, links

    async def update_user_data(
        self, user: User, data: UpdateUserData
    ) -> UserInfo:
        info = user.info

        info.first_name = data.first_name \
                if data.first_name != "string" else info.first_name
        info.last_name = data.last_name \
                if data.last_name != "string" else info.last_name
        info.description = data.description \
                if data.description != "string" else info.description

        self.session.add(info)

        await self.session.flush()

        return info

    async def add_skill_to_user(
        self, user: User, data: NewSkillInfo
    ) -> Skill:
        
        info = user.info

        query = select(Skill).where(Skill.skill_id == data.skill_id)
        skill = await self.session.scalars(query)
        skill = skill.first()

        m2m = SkillUserM2M(
            user=info,
            skill=skill,
            skill_lvl=data.skill_lvl
        )

        self.session.add(m2m)
        await self.session.flush()

        return skill

    async def modify_skill_on_user(
        self, user: User, name: str, data: SkillInfo
    ) -> SkillUserM2M:

        info = user.info

        for m2m in info.skills:
            if m2m.skill.skill_name == name:
                m2m.skill_lvl = data.skill_lvl
                self.session.add(m2m)
                await self.session.flush()

                return m2m
        
        raise Exception("No such skill on user")

    async def delete_skill_from_user(
        self, user: User, name: str 
    ) -> SkillUserM2M:

        info = user.info

        for m2m in info.skills:
            if m2m.skill.skill_name == name:
                await self.session.delete(m2m)
                await self.session.flush()

                return m2m
        
        raise Exception("No such skill on user")

    async def add_link_to_user(self, user: User, data: LinkInfo) -> Link:

        info = user.info

        link = Link(
            resource=data.resource,
            url=data.url,
            _user=info
        )

        self.session.add(link)

        return link

    async def modify_link_on_user(
        self, user: User, resource: str, data: LinkInfo
    ) -> Link:

        info = user.info

        for link in info._links:
            if link.resource == resource:
                link.resource = data.resource
                link.url = data.url
                self.session.add(link)
                await self.session.flush()

                return link

        raise Exception("No such link on user")

    async def delete_link_from_user(
        self, user: User, resource: str
    ) -> Link:

        info = user.info

        for link in info._links:
            if link.resource == resource:
                await self.session.delete(link)
                await self.session.flush()

                return link

        raise Exception("No such link on user")

    async def add_photo_to_user(self, user: User, photo_link: str):

        info = user.info
        info.photo_link = photo_link

        self.session.add(info)
        await self.session.flush()
