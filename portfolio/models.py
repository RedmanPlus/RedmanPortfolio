from typing import List

from pydantic import BaseModel, EmailStr, HttpUrl


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


class LinkInfo(ORMModel):
    resource: str
    url: HttpUrl


class SkillInfo(ORMModel):
    skill_name: str


class FullUserData(ORMModel):

    first_name: str
    last_name: str
    description: str
    skills: List[SkillInfo]
    links: List[LinkInfo]
