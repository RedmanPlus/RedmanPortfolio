from pydantic import BaseModel, EmailStr


class ORMModel(BaseModel):

    class Config:

        orm_mode = True


class InputUser(ORMModel):
    email: EmailStr


class LoginUser(ORMModel):
    username: str
    password: str


class UserData(BaseModel):
    username: str
    password_1: str
    password_2: str


class NewOutputUser(ORMModel):
    email: EmailStr


class OutputUser(ORMModel):
    username: str
    email: EmailStr
