from typing import List, Optional

from pydantic import BaseModel

from portfolio.models.core import ORMModel
from portfolio.models.skill import NewSkillInfo, SkillInfo
from portfolio.models.link import LinkInfo


class InfoData(BaseModel):
    first_name: str
    last_name: str
    descrption: str
    skill_ids: Optional[List[NewSkillInfo]] = None
    links: Optional[List[LinkInfo]] = None


class UpdateUserData(BaseModel):
    first_name: str
    last_name: str
    description: str


class FullUserData(ORMModel):

    first_name: str
    last_name: str
    description: str
    photo_link: Optional[str] = None
    skills: Optional[List[SkillInfo]] = None
    links: Optional[List[LinkInfo]] = None


class ShortUserData(ORMModel):

    first_name: str
    last_name: str
    photo_link: Optional[str] = None


class UserPhoto(BaseModel):

    photo_link: str
