from typing import List, Optional

from pydantic import BaseModel

from portfolio.models.core import ORMModel
from portfolio.models.skill import SkillID
from portfolio.models.user_info import ShortUserData


class BlockInfo(ORMModel):

    block_name: str
    block_description: Optional[str] = None
    skills: Optional[List[SkillID]] = None
    block_author: Optional[ShortUserData] = None


class LinkBlock(BaseModel):

    block_1_name: str
    block_2_name: str


class BlockM2M(ORMModel):

    left_block: BlockInfo
    right_block: BlockInfo


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


class PublichProjectData(BaseModel):

    is_public: bool


class UpdateProjectData(BaseModel):

    project_name: Optional[str] = None
    short_description: Optional[str] = None
    project_logo: Optional[str] = None
    full_description: Optional[str] = None
    blocks: Optional[List[BlockIDData]] = None


class EdgeId(ORMModel):

    id: int
