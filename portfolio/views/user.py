from fastapi import Depends, Request 
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.BL.user_handlers import (
    create_user,
    get_user_by_id,
    get_user_by_email,
    update_user,
)
from portfolio.db.session import get_db
from portfolio.dependencies import user
from portfolio.models import InputUser, OutputUser, NewOutputUser, UserData

users = APIRouter()


@users.get("/me", response_model=NewOutputUser)
async def get_me(request: Request) -> NewOutputUser:

    me = user(request)
    if me.is_anonymous:
        raise HTTPException(
            status_code=404, detail="You're not logged in"
        )
    return NewOutputUser(
        email=me.email
    )


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


@users.post("/", response_model=NewOutputUser)
async def post_user(
    body: InputUser, db: AsyncSession = Depends(get_db)
) -> NewOutputUser:
    try:
        return await create_user(body, db)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database Error: {err}")


@users.put("/{user_id}", response_model=OutputUser)
async def fill_out_user_data(
    user_id: int, body: UserData, db: AsyncSession = Depends(get_db)
) -> OutputUser:
    try:
        return await update_user(user_id, body, db)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database Error: {err}")
