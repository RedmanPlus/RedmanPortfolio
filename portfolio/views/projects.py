from typing import List
from fastapi import Depends, HTTPException, Request
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.BL.project_handlers import (
    get_projects,
    add_project,
    get_users_projects
)
from portfolio.db.session import get_db
from portfolio.dependencies import user
from portfolio.models import ProjectInfo, ProjectData

projects = APIRouter()


@projects.get("/", response_model=list[ProjectInfo])
async def get_all_projects(
    request: Request, db: AsyncSession = Depends(get_db)
) -> List[ProjectInfo]:
    user_obj = user(request)
    try:
        return await get_projects(user_obj, db)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@projects.post("/", response_model=ProjectInfo)
async def create_project(
    request: Request, data: ProjectData, db: AsyncSession = Depends(get_db)
) -> ProjectInfo:
    user_obj = user(request)
    if user_obj.is_anonymous:
        raise HTTPException(
            status_code=403,
            detail="You cannot create new projects"
        )

    try:
        return await add_project(user_obj, data, db)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@projects.get("/{username}/", response_model=list[ProjectInfo])
async def get_user_projects(
    request: Request, username: str, db: AsyncSession = Depends(get_db)
) -> List[ProjectInfo]:
    user_obj = user(request)
    try:
        return await get_users_projects(user_obj, username, db)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )
