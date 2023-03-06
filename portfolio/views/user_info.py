from fastapi import Depends, Request 
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.BL.user_info_handlers import (
    get_user_info,
    add_user_data,
    add_skill_to_user,
    modify_skill_on_user,
    delete_skill_from_user,
)
from portfolio.db.session import get_db
from portfolio.dependencies import user
from portfolio.models import (
    FullUserData,
    InfoData,
    SkillInfo,
    NewSkillInfo
)

user_info = APIRouter()


@user_info.get("/me", response_model=FullUserData)
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
    try:
        return await add_user_data(user_obj, data, db)
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
