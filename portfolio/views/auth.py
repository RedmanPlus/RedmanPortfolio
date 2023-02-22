from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.BL.auth_handlers import authenticate, login
from portfolio.db.session import get_db
from portfolio.dependencies import session
from portfolio.models import OutputUser, LoginUser


auth = APIRouter()


@auth.post("/login", response_model=OutputUser)
async def login_user(
    data: LoginUser, request: Request
) -> OutputUser:
    user = await authenticate(data)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User with these credantials does not exists"
        )

    session_obj = await session(request)

    await login(user, session_obj)

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
