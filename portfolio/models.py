from typing import List, Optional

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


class SkillData(BaseModel):
    skill_name: str


class BaseSkillInfo(ORMModel):
    skill_id: int
    skill_name: str


class SkillInfo(ORMModel):
    skill_name: str
    skill_lvl: str


class NewSkillInfo(BaseModel):
    skill_id: int
    skill_lvl: str


class InfoData(BaseModel):
    first_name: str
    last_name: str
    descrption: str
    skill_ids: List[NewSkillInfo]
    links: List[LinkInfo]


class UpdateUserData(BaseModel):
    first_name: str
    last_name: str
    description: str


class FullUserData(ORMModel):

    first_name: str
    last_name: str
    description: str
    photo_link: Optional[str] = None
    skills: List[SkillInfo]
    links: List[LinkInfo]


class ShortUserData(ORMModel):

    first_name: str
    last_name: str
    photo_link: Optional[str] = None


class UserPhoto(BaseModel):

    photo_link: str


class BlockInfo(ORMModel):

    block_name: str
    block_description: Optional[str] = None
    skills: Optional[List[SkillData]] = None
    block_author: Optional[ShortUserData] = None


class BlockIDData(BaseModel):

    block_name: str


class ProjectInfo(ORMModel):

    project_name: str
    short_description: Optional[str] = None
    project_logo: Optional[str] = None
    full_description: Optional[str] = None
    is_public: bool
    blocks: Optional[List[BlockInfo]] = None
    author: ShortUserData


class ProjectData(BaseModel):

    project_name: str


class UpdateProjectData(BaseModel):

    project_name: Optional[str] = None
    short_description: Optional[str] = None
    project_logo: Optional[str] = None
    full_description: Optional[str] = None
    blocks: Optional[List[BlockIDData]] = None
