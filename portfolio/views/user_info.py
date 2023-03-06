from fastapi import Depends, Request 
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.BL.user_info_handlers import (
    get_user_info,
    add_user_data,
    update_user_data,
    add_skill_to_user,
    modify_skill_on_user,
    delete_skill_from_user,
    add_link_to_user,
    modify_link_on_user,
    delete_link_from_user
)
from portfolio.db.models import UserInfo
from portfolio.db.session import get_db
from portfolio.dependencies import user
from portfolio.models import (
    FullUserData,
    InfoData,
    LinkInfo,
    SkillInfo,
    NewSkillInfo,
    UpdateUserData
)

user_info = APIRouter()


@user_info.get("/", response_model=FullUserData)
async def get_my_data(
    request: Request, db: AsyncSession = Depends(get_db)
) -> FullUserData:
    user_obj = user(request)
    try:
        return await get_user_info(user_obj, db)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied {err}"
        )


@user_info.post("/", response_model=FullUserData)
async def add_my_data(
    request: Request, data: InfoData, db: AsyncSession = Depends(get_db)
) -> FullUserData:
    user_obj = user(request)
    if isinstance(user_obj.info, UserInfo):
        raise HTTPException(
            status_code=400,
            detail="UserInfo already exists on you, you can modify it at "
                    "PUT /"
        )
    try:
        return await add_user_data(user_obj, data, db)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@user_info.put("/", response_model=FullUserData)
async def update_my_data(
    request: Request,
    data: UpdateUserData,
    db: AsyncSession = Depends(get_db)
) -> FullUserData:
    user_obj = user(request)
    try:
        return await update_user_data(user_obj, data, db)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@user_info.post("/skill/", response_model=SkillInfo)
async def add_skill(
    request: Request, data: NewSkillInfo, db: AsyncSession = Depends(get_db)
) -> SkillInfo:
    user_obj = user(request)
    try:
        return await add_skill_to_user(user_obj, data, db)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@user_info.put("/skill/{name}", response_model=SkillInfo)
async def modify_skill(
    request: Request,
    name: str,
    data: SkillInfo,
    db: AsyncSession = Depends(get_db)
) -> SkillInfo:
    user_obj = user(request)
    try:
        return await modify_skill_on_user(user_obj, name, data, db)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@user_info.delete("/skill/{name}", response_model=SkillInfo)
async def delete_skill(
    request: Request,
    name: str,
    db: AsyncSession = Depends(get_db)
) -> SkillInfo:
    user_obj = user(request)
    try:
        return await delete_skill_from_user(user_obj, name, db)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@user_info.post("/link/", response_model=LinkInfo)
async def add_link(
    request: Request, data: LinkInfo, db: AsyncSession = Depends(get_db)
) -> LinkInfo:
    user_obj = user(request)
    try:
        return await add_link_to_user(user_obj, data, db)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@user_info.put("/link/{resorce}", response_model=LinkInfo)
async def modify_link(
    request: Request,
    resource: str,
    data: LinkInfo,
    db: AsyncSession = Depends(get_db)
) -> LinkInfo:
    user_obj = user(request)
    try:
        return await modify_link_on_user(user_obj, resource, data, db)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@user_info.delete("/link/{resorce}", response_model=LinkInfo)
async def delete_link(
    request: Request,
    resource: str,
    db: AsyncSession = Depends(get_db)
) -> LinkInfo:
    user_obj = user(request)
    try:
        return await delete_link_from_user(user_obj, resource, db)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )
