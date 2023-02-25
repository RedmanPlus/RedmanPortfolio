from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.BL.auth_handlers import (
    authenticate,
    login,
    handle_email_token
)
from portfolio.db.session import get_db
from portfolio.dependencies import session
from portfolio.models import OutputUser, LoginUser, NewOutputUser


auth = APIRouter()


@auth.post("/login", response_model=OutputUser)
async def login_user(
    data: LoginUser, request: Request, db: AsyncSession = Depends(get_db)
) -> OutputUser:
    user = await authenticate(data, db)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User with these credantials does not exists"
        )

    session_obj = await session(request)

    await login(user, session_obj, db)

    return OutputUser(
        username=user.username,
        email=user.email
    )


@auth.post("/logout")
async def logout_user(
    request: Request, db: AsyncSession = Depends(get_db)
):
    session_obj = await session(request)

    session_obj.user = None
    session_obj.uid = None

    db.add(session_obj)
    await db.flush()

    return {"success": "you've logged out"}


@auth.get("/confirm", response_model=NewOutputUser)
async def confirm_user_from_email_token(
    request: Request, token: str, db: AsyncSession = Depends(get_db)
):
    session_obj = await session(request)
    user = await handle_email_token(session_obj, token, db)

    return NewOutputUser(
        email=user.email
    )
