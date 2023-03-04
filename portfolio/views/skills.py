from typing import List

from fastapi import Depends, HTTPException, Request
from fastapi.routing import APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.BL.skill_handlers import get_skills, create_skill
from portfolio.db.session import get_db
from portfolio.dependencies import user
from portfolio.models import SkillInfo, SkillData

skills = APIRouter()


@skills.get("/", response_model=list[SkillInfo])
async def get_all_skills(
    db: AsyncSession = Depends(get_db)
) -> List[SkillInfo]:
    try:
        return await get_skills(db)
    except Exception as err:
        raise HTTPException(
            status_code=500, detail=f"Exception occured: {err}"
        )


@skills.post("/", response_model=SkillInfo)
async def add_skill(
    data: SkillData, db: AsyncSession = Depends(get_db)
) -> SkillInfo:
    try:
        return await create_skill(data, db)
    except IntegrityError as err:
        raise HTTPException(
            status_code=500, detail=f"Database error: {err}"
        )
