from fastapi import Depends, Request 
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.BL.user_info_handlers import get_user_info, add_user_data
from portfolio.db.session import get_db
from portfolio.dependencies import user
from portfolio.models import FullUserData, InfoData

user_info = APIRouter()


@user_info.get("/me", response_model=FullUserData)
async def get_my_data(
    request: Request, db: AsyncSession = Depends(get_db)
) -> FullUserData:
    user_obj = user(request)
    try:
        return await get_user_info(user_obj, db)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Cannot get info on user, perhaps you're logged out"
        )


@user_info.post("/", response_model=FullUserData)
async def add_my_data(
    request: Request, data: InfoData, db: AsyncSession = Depends(get_db)
) -> FullUserData:
    user_obj = user(request)
    try:
        return await add_user_data(user_obj, data, db)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Cannot ad info to user, perhaps you're logged out"
        )
