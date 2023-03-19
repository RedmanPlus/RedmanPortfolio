from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.BL.workplace_handlers import (
    get_user_workplace,
    add_user_workplace,
    get_workplace_by_username,
    get_workplace_by_name,
    update_workplace_by_name,
    delete_workplace_by_name
)
from portfolio.db.session import get_db
from portfolio.dependencies import user
from portfolio.models.workplace import (
    NewWorkplace,
    WorkplaceInfo,
    UpdateWorkplace
)

workplace = APIRouter()


@workplace.get("/", response_model=list[WorkplaceInfo])
async def get_my_workplaces(
    request: Request, db: AsyncSession = Depends(get_db)
) -> List[WorkplaceInfo]:
    user_obj = user(request)
    try:
        return await get_user_workplace(user_obj, db)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@workplace.post("/", response_model=NewWorkplace)
async def add_my_workplace(
    request: Request, data: NewWorkplace, db: AsyncSession = Depends(get_db)
) -> NewWorkplace:
    user_obj = user(request)
    try:
        return await add_user_workplace(user_obj, data, db)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@workplace.get("/of/{username}/", response_model=list[WorkplaceInfo])
async def get_user_workplaces_by_username(
    username: str, db: AsyncSession = Depends(get_db)
) -> List[WorkplaceInfo]:
    try:
        return await get_workplace_by_username(username, db)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@workplace.get("/{workplace_name}/", response_model=WorkplaceInfo)
async def get_workplace(
    workplace_name: str, db: AsyncSession = Depends(get_db)
) -> WorkplaceInfo:
    try:
        return await get_workplace_by_name(workplace_name, db)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@workplace.put("/{workplace_name}/", response_model=WorkplaceInfo)
async def update_workplace_info(
    request: Request,
    workplace_name: str,
    data: UpdateWorkplace,
    db: AsyncSession = Depends(get_db)
) -> WorkplaceInfo:
    user_obj = user(request)
    try:
        return await update_workplace_by_name(
            user_obj, workplace_name, data, db
        )
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@workplace.delete("/{workplace_name}/", response_model=WorkplaceInfo)
async def delete_workplace(
    request: Request, workplace_name: str, db: AsyncSession = Depends(get_db)
) -> WorkplaceInfo:
    user_obj = user(request)
    try:
        return await delete_workplace_by_name(user_obj, workplace_name, db)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )
