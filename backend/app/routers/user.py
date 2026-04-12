# app/routers/user.py

import logging
from fastapi import APIRouter, Request, Depends, HTTPException
import httpx
from motor.motor_asyncio import AsyncIOMotorClient
from ..db.db import get_database
from ..core.setting import get_settings
from ..exceptions.error import UserNotFoundException, NoRecentGamesException
from ..services import orchestrator
from ..dependencies import get_er_client, get_gemini_semaphore

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/users", tags=["Users"])
settings = get_settings()

# --- API 엔드포인트 ---
@router.get("/num/{nickname}")
async def get_user_num_api(nickname: str, client: httpx.AsyncClient = Depends(get_er_client)):
    url = "/v1/user/nickname"
    params = {"query": nickname}
    response = await client.get(url, params=params)
    if response.status_code != 200:
        raise UserNotFoundException(nickname=nickname)
    data = response.json()
    if data.get('code') == 200 and data.get('user'):
        return {"nickname": nickname, "userId": data['user']['userId']}
    raise UserNotFoundException(nickname=nickname)

@router.get("/stat/{userId}")
async def get_user_stat_api(
    userId: str,
    er_client: httpx.AsyncClient = Depends(get_er_client),
    gemini_semaphore = Depends(get_gemini_semaphore),
    db: AsyncIOMotorClient = Depends(get_database)
):
    profile_data = await orchestrator.get_user_profile_data(
        userId, er_client, gemini_semaphore, db
    )
    if profile_data is None:
        raise NoRecentGamesException()
    return profile_data