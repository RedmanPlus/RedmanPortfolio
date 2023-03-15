from typing import Optional

from pydantic import BaseModel

from portfolio.models.core import ORMModel


class SkillData(ORMModel):
    skill_name: Optional[str] = None


class BaseSkillInfo(ORMModel):
    skill_id: int
    skill_name: str


class SkillInfo(ORMModel):
    skill_name: str
    skill_lvl: str


class NewSkillInfo(BaseModel):
    skill_id: int
    skill_lvl: str


class SkillID(ORMModel):
    skill_id: int
