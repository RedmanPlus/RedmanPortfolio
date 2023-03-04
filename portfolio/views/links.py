from fastapi import Depends, HTTPException, Request
from fastapi.routing import APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.BL.link_handlers import create_new_link
from portfolio.db.session import get_db
from portfolio.dependencies import user
from portfolio.models import LinkInfo

links = APIRouter()


@links.post("/", response_model=LinkInfo)
async def create_link(
    request: Request, info: LinkInfo, db: AsyncSession = Depends(get_db)
) -> LinkInfo:
    user_obj = user(request)
    try:
        return await create_new_link(user_obj, info, db)
    except IntegrityError as err:
        raise HTTPException(
            status_code=500, detail=f"Database error: {err}"
        )
