from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.BL.workplace_handlers import add_user_workplace
from portfolio.db.session import get_db
from portfolio.dependencies import user
from portfolio.models.workplace import NewWorkplace, WorkplaceInfo


workplace = APIRouter()


@workplace.post("/", response_model=WorkplaceInfo)
async def add_my_workplace(
    request: Request, data: NewWorkplace, db: AsyncSession = Depends(get_db)
) -> WorkplaceInfo:
    user_obj = user(request)
    try:
        return await add_user_workplace(user_obj, data, db)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )
