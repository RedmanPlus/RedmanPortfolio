from fastapi import Depends 
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.BL.user_handlers import (
    create_user,
    get_user_by_id,
    get_user_by_email,
)
from portfolio.db.session import get_db
from portfolio.models import InputUser, OutputUser

users = APIRouter()


@users.get("/{user_id}", response_model=OutputUser)
async def get_user_from_id(
    user_id: int, db: AsyncSession = Depends(get_db)
) -> OutputUser:
    try:
        return await get_user_by_id(user_id, db)
    except Exception:
        raise HTTPException(
            status_code=404, detail=f"User by ID {user_id} doesn't exist"
        )


@users.get("/{user_email}", response_model=OutputUser)
async def get_user_from_email(
    user_email: str, db: AsyncSession = Depends(get_db)
) -> OutputUser:
    try:
        return await get_user_by_email(user_email, db)
    except Exception:
        raise HTTPException(
            status_code=404, detail=f"User by email {user_email} doesn't exist"
        )


@users.post("/", response_model=OutputUser)
async def post_user(
    body: InputUser, db: AsyncSession = Depends(get_db)
) -> OutputUser:
    try:
        return await create_user(body, db)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database Error: {err}")
