from datetime import date
from typing import List, Optional

from pydantic import BaseModel

from portfolio.models import ORMModel
from portfolio.models.project import ShortProjectInfo
from portfolio.models.skill import SkillInfo


class NewWorkplace(BaseModel):

    workplace_name: str
    work_start_date: date
    work_end_date: Optional[date]
    is_current_workplace: Optional[bool]
    company_link: Optional[str]
    workplace_description: Optional[str]


class WorkplaceInfo(ORMModel):

    workplace_name: str
    work_start_date: date
    work_end_date: Optional[date]
    is_current_workplace: Optional[bool]
    company_link: Optional[str]
    workplace_description: Optional[str]
    skills: Optional[List[SkillInfo]] = None
    projects: Optional[List[ShortProjectInfo]] = None
