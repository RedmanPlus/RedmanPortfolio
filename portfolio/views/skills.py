from typing import List

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.BL.skill_handlers import get_skills, create_skill
from portfolio.db.session import get_db
from portfolio.models import SkillData, BaseSkillInfo

skills = APIRouter()


@skills.get("/", response_model=list[BaseSkillInfo])
async def get_all_skills(
    db: AsyncSession = Depends(get_db)
) -> List[BaseSkillInfo]:
    try:
        return await get_skills(db)
    except Exception as err:
        raise HTTPException(
            status_code=500, detail=f"Exception occured: {err}"
        )


@skills.post("/", response_model=BaseSkillInfo)
async def add_skill(
    data: SkillData, db: AsyncSession = Depends(get_db)
) -> BaseSkillInfo:
    try:
        return await create_skill(data, db)
    except IntegrityError as err:
        raise HTTPException(
            status_code=500, detail=f"Database error: {err}"
        )
