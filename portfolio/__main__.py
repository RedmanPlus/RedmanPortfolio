import uvicorn

from fastapi import FastAPI, Depends
from fastapi.requests import Request

from portfolio.db.dal import SessionDAL
from portfolio.db.session import get_session
from portfolio.views.views import users
from portfolio.views.login import login


app = FastAPI()

@app.middleware("http")
async def get_user(request: Request, call_next):

    dal = SessionDAL(session=get_session())
    cookies = request.cookies
    
    if session_key := cookies.get("User-Session", False):
        user = await dal.get_user_from_session(session_key=session_key)
    else:
        session = await dal.create_session_key()
        user = session.user
        session_key=session.session_key
        
    request.state.user = user
    responce = await call_next(request)
    responce.set_cookie(key="User-Session", value = session_key)
    return responce

app.include_router(users, prefix="/user", tags=["user"])
app.include_router(login, prefix="/auth", tags=["auth"])


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)
