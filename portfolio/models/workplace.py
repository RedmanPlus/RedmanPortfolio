from datetime import date
from typing import List, Optional

from pydantic import BaseModel

from portfolio.models import ORMModel
from portfolio.models.project import ShortProjectInfo
from portfolio.models.skill import SkillInfo


class NewWorkplace(BaseModel):

    workplace_name: str
    work_start_date: date
    work_end_date: Optional[date] = None
    is_current_workplace: Optional[bool] = None
    company_link: Optional[str] = None
    workplace_description: Optional[str] = None


class WorkplaceInfo(ORMModel):

    workplace_name: str
    work_start_date: date
    work_end_date: Optional[date] = None
    is_current_workplace: Optional[bool] = None
    company_link: Optional[str] = None
    workplace_description: Optional[str] = None
    skills: Optional[List[SkillInfo]] = None
    projects: Optional[List[ShortProjectInfo]] = None


class UpdateWorkplace(BaseModel):

    workplace_name: Optional[str] = None
    work_start_date: Optional[date] = None
    work_end_date: Optional[date] = None
    is_current_workplace: Optional[bool] = None
    company_link: Optional[str] = None
    workplace_description: Optional[str] = None
