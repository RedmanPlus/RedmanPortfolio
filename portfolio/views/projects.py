from typing import List

from fastapi import Depends, HTTPException, Request
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from portfolio.BL.project_handlers import (
    get_projects,
    add_project,
    get_users_projects,
    get_user_project_by_id,
    update_user_project_by_id,
    publish_project_by_id,
    delete_project_by_id,
    get_project_blocks_by_id,
    add_block_to_project,
    link_blocks_in_project,
    get_project_block_by_name,
    update_project_block_by_name,
    delete_project_block_by_name,
    get_project_block_tree_by_id,
)
from portfolio.db.session import get_db
from portfolio.dependencies import user
from portfolio.models import (
    BlockInfo,
    BlockM2M,
    LinkBlock,
    ProjectInfo,
    ProjectData,
    PublichProjectData,
    UpdateProjectData,
    EdgeId
)

projects = APIRouter()


@projects.get("/", response_model=list[ProjectInfo])
async def get_all_projects(
    request: Request, db: AsyncSession = Depends(get_db)
) -> List[ProjectInfo]:
    user_obj = user(request)
    try:
        return await get_projects(user_obj, db)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@projects.post("/", response_model=ProjectInfo)
async def create_project(
    request: Request, data: ProjectData, db: AsyncSession = Depends(get_db)
) -> ProjectInfo:
    user_obj = user(request)
    if user_obj.is_anonymous:
        raise HTTPException(
            status_code=403,
            detail="You cannot create new projects"
        )

    try:
        return await add_project(user_obj, data, db)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@projects.get("/{username}/", response_model=list[ProjectInfo])
async def get_user_projects(
    request: Request, username: str, db: AsyncSession = Depends(get_db)
) -> List[ProjectInfo]:
    user_obj = user(request)
    try:
        return await get_users_projects(user_obj, username, db)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@projects.get("/{username}/{project_id}/", response_model=ProjectInfo)
async def get_project_by_id(
    request: Request,
    username: str,
    project_id: int,
    db: AsyncSession = Depends(get_db)
) -> ProjectInfo:
    user_obj = user(request)
    try:
        return await get_user_project_by_id(
            user_obj, username, project_id, db
        )
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@projects.put("/{username}/{project_id}/", response_model=ProjectInfo)
async def update_project_by_id(
    request: Request,
    username: str,
    project_id: int,
    data: UpdateProjectData,
    db: AsyncSession = Depends(get_db)
) -> ProjectInfo:
    user_obj = user(request)
    try:
        return await update_user_project_by_id(
            user_obj, username, project_id, data, db
        )
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@projects.patch("/{username}/{project_id}/", response_model=ProjectInfo)
async def publish_project(
    request: Request,
    username: str,
    project_id: int,
    data: PublichProjectData,
    db: AsyncSession = Depends(get_db)
) -> ProjectInfo:
    user_obj = user(request)
    try:
        return await publish_project_by_id(
            user_obj, username, project_id, data, db
        )
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@projects.delete("/{username}/{project_id}/", response_model=ProjectInfo)
async def delete_project(
    request: Request,
    username: str,
    project_id: int,
    db: AsyncSession = Depends(get_db)
) -> ProjectInfo:
    user_obj = user(request)
    try:
        return await delete_project_by_id(
            user_obj, username, project_id, db
        )
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@projects.get(
    "/{username}/{project_id}/blocks",
    response_model=list[BlockInfo]
)
async def get_project_blocks(
    request: Request,
    username: str,
    project_id: int,
    db: AsyncSession = Depends(get_db)
) -> List[BlockInfo]:
    user_obj = user(request)
    try:
        return await get_project_blocks_by_id(
            user_obj, username, project_id, db
        )
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@projects.post(
    "/{username}/{project_id}/blocks",
    response_model=BlockInfo
)
async def add_project_block(
    request: Request,
    username: str,
    project_id: int,
    data: BlockInfo,
    db: AsyncSession = Depends(get_db)
) -> BlockInfo:
    user_obj = user(request)
    try:
        return await add_block_to_project(
            user_obj, username, project_id, data, db
        )
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@projects.put(
    "/{username}/{project_id}/blocks",
    response_model=BlockM2M
)
async def link_project_blocks(
    request: Request,
    username: str,
    project_id: int,
    data: LinkBlock,
    db: AsyncSession = Depends(get_db)
) -> BlockM2M:
    user_obj = user(request)
    try:
        return await link_blocks_in_project(
            user_obj, username, project_id, data, db
        )
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@projects.get(
    "/{username}/{project_id}/blocks/{block_name}/",
    response_model=BlockInfo
)
async def get_block_by_name(
    request: Request,
    username: str,
    project_id: int,
    block_name: str,
    db: AsyncSession = Depends(get_db)
) -> BlockInfo:
    user_obj = user(request)
    try:
        return await get_project_block_by_name(
            user_obj, username, project_id, block_name, db
        )
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@projects.put(
    "/{username}/{project_id}/blocks/{block_name}/",
    response_model=BlockInfo
)
async def update_block_by_name(
    request: Request,
    username: str,
    project_id: int,
    block_name: str,
    data: BlockInfo,
    db: AsyncSession = Depends(get_db)
) -> BlockInfo:
    user_obj = user(request)
    try:
        return await update_project_block_by_name(
            user_obj, username, project_id, block_name, data, db
        )
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@projects.delete(
    "/{username}/{project_id}/blocks/{block_name}/",
    response_model=BlockInfo
)
async def delete_block_by_name(
    request: Request,
    username: str,
    project_id: int,
    block_name: str,
    db: AsyncSession = Depends(get_db)
) -> BlockInfo:
    user_obj = user(request)
    try:
        return await delete_project_block_by_name(
            user_obj, username, project_id, block_name, db
        )
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )


@projects.get("/{username}/{project_id}/block_tree/", response_model=list[EdgeId])
async def get_project_block_tree(
    request: Request,
    username: str,
    project_id: int,
    db: AsyncSession = Depends(get_db)
) -> List[EdgeId]:
    user_obj = user(request)
    try:
        return await get_project_block_tree_by_id(
            user_obj, username, project_id, db
        )
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Error occupied: {err}"
        )
