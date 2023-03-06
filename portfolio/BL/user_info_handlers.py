from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.db.models import User
from portfolio.db.dal.user_info import UserInfoDAL
from portfolio.models import (
    FullUserData,
    InfoData,
    LinkInfo,
    SkillData, 
    SkillInfo,
    NewSkillInfo
)


async def get_user_info(user: User, db: AsyncSession) -> FullUserData:
    async with db.begin():
        dal = UserInfoDAL(db)
        return await dal.get_user_info(user)


async def add_user_data(
    user: User, data: InfoData, db: AsyncSession
) -> FullUserData:
    async with db.begin():

        dal = UserInfoDAL(db)

        user_info, skills, links = await dal.create_user_info(user, data)

        links = [LinkInfo.from_orm(obj) for obj in links]
        skills = [
            SkillInfo(skill_name=obj.skill_name, skill_lvl=data.skill_lvl)
            for obj, data in zip(skills, data.skill_ids)
        ]

        return FullUserData(
            first_name=user_info.first_name,
            last_name=user_info.last_name,
            description=user_info.description,
            links=links,
            skills=skills
        )


async def add_skill_to_user(
    user: User, data: NewSkillInfo, db: AsyncSession
) -> SkillInfo:
    async with db.begin():
        dal = UserInfoDAL(db)

        skill = await dal.add_skill_to_user(user, data)

        return SkillInfo(
            skill_name=skill.skill_name,
            skill_lvl=data.skill_lvl
        )


async def modify_skill_on_user(
    user: User, name: str, data: SkillInfo, db: AsyncSession
) -> SkillInfo:
    async with db.begin():
        dal = UserInfoDAL(db)

        skill = await dal.modify_skill_on_user(user, name, data)

        return SkillInfo(
            skill_name=name,
            skill_lvl=skill.skill_lvl
        )


async def delete_skill_from_user(
    user: User, name: str, db: AsyncSession
) -> SkillInfo:
    async with db.begin():
        dal = UserInfoDAL(db)

        skill = await dal.delete_skill_from_user(user, name)

        return SkillInfo(
            skill_name=name,
            skill_lvl=skill.skill_lvl
        )
