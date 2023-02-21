from pydantic import BaseModel, EmailStr


class ORMModel(BaseModel):

    class Config:

        orm_mode = True


class InputUser(ORMModel):
    username: str
    password: str
    email: EmailStr


class LoginUser(ORMModel):
    username: str
    password: str


class OutputUser(ORMModel):
    username: str
    email: EmailStr
