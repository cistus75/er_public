# app/routers/user.py

import logging
from fastapi import APIRouter, Request, Depends, HTTPException
import httpx
# ✨ 1. DB 관련 모듈 import 추가
from motor.motor_asyncio import AsyncIOMotorClient
from ..db.db import get_database

from ..core.setting import get_settings
from ..exceptions.error import UserNotFoundException, NoRecentGamesException
from ..services import orchestrator

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/users", tags=["Users"]) # ✨ prefix 경로 수정 제안
settings = get_settings()

# --- 의존성 주입 ---
def get_er_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.er_client

def get_gemini_semaphore(request: Request):
    return request.app.state.gemini_semaphore

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
    # ✨ 2. `db` 객체를 의존성 주입으로 받아오도록 추가
    db: AsyncIOMotorClient = Depends(get_database)
):
    # 이제 `db`는 이 함수 안에서 정상적으로 인식되는 변수입니다.
    profile_data = await orchestrator.get_user_profile_data(
        userId, er_client, gemini_semaphore, db  # <- 이제 에러 없이 전달 가능
    )
    if profile_data is None:
        raise NoRecentGamesException()
    return profile_data