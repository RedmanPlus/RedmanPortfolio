from fastapi import UploadFile
from miniopy_async import Minio
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.db.models import User
from portfolio.db.dal.user_info import UserInfoDAL
from portfolio.models import (
    FullUserData,
    InfoData,
    LinkInfo,
    SkillData, 
    SkillInfo,
    NewSkillInfo,
    UpdateUserData,
    UserPhoto
)


async def get_user_info(user: User, db: AsyncSession) -> FullUserData:
    if user.is_anonymous:
        raise Exception(
            "You cannot see your profile cause you're not logged in"
        )
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


async def update_user_data(
    user: User, data: UpdateUserData, db: AsyncSession
) -> FullUserData:
    async with db.begin():

        dal = UserInfoDAL(db)

        user_info = await dal.update_user_data(user, data)

        links = [LinkInfo.from_orm(obj) for obj in user_info._links]
        skills = [
            SkillInfo(
                skill_name=obj.skill.skill_name,
                skill_lvl=obj.skill_lvl
            )
            for obj in user_info.skills
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


async def add_link_to_user(
    user: User, data: LinkInfo, db: AsyncSession
) -> LinkInfo:
    async with db.begin():
        dal = UserInfoDAL(db)

        link = await dal.add_link_to_user(user, data)

        return LinkInfo(
            resource=link.resource,
            url=link.url
        )


async def modify_link_on_user(
    user: User, resource: str, data: LinkInfo, db: AsyncSession
) -> LinkInfo:
    async with db.begin():
        dal = UserInfoDAL(db)

        link = await dal.modify_link_on_user(user, resource, data)

        return LinkInfo(
            resource=link.resource,
            url=link.url
        )


async def delete_link_from_user(
    user: User, resource: str, db: AsyncSession
) -> LinkInfo:
    async with db.begin():
        dal = UserInfoDAL(db)

        link = await dal.delete_link_from_user(user, resource)

        return LinkInfo(
            resource=link.resource,
            url=link.url
        )


async def add_user_photo(
    user: User, photo: UploadFile, minio: Minio, db: AsyncSession
) -> UserPhoto:
    if user.is_anonymous:
        raise Exception("You're not logged in")

    result = await minio.put_object(
        "photos",
        f"{user.username}_{photo.filename}",
        photo.file,
        length=-1,
        part_size=10*1024*1024
    )

    result_link = f"http://127.0.0.1:9000/photo/{result._object_name}"

    async with db.begin():
        dal = UserInfoDAL(db)

        await dal.add_photo_to_user(user, result_link)

    return UserPhoto(photo_link=result_link)
