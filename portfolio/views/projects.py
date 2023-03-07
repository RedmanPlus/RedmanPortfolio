from fastapi import Depends, HTTPException, Request
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.BL.project_handlers import add_project
from portfolio.db.session import get_db
from portfolio.dependencies import user
from portfolio.models import ProjectInfo, ProjectData

projects = APIRouter()


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
