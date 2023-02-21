from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.BL.user_handlers import create_user
from portfolio.db.session import get_db
from portfolio.models import InputUser, OutputUser

users = APIRouter()


@users.get("/")
async def test():
    return {"hi": "mom"}


@users.post("/", response_model=OutputUser)
async def create_user(
    body: InputUser, db: AsyncSession = Depends(get_db)
) -> OutputUser:
    try:
        return await create_user(body, db)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database Error: {err}")
