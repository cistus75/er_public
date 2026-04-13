import logging
from fastapi import APIRouter, Depends, HTTPException
import httpx

# --- 필요한 서비스 및 유틸리티 함수 import ---
from ..services import er
from ..common.utils import get_tier
from ..dependencies import get_er_client  # 공통 의존성 모듈에서 가져옵니다

# 로거 설정
logger = logging.getLogger(__name__)

# API 경로의 접두사(/api/routes)와 태그(Routes)를 설정합니다.
router = APIRouter(prefix="/api/routes", tags=["Routes"])


@router.get("/{route_id}", summary="루트 상세 정보 조회")
async def get_route_details_api(
    route_id: int,
    er_client: httpx.AsyncClient = Depends(get_er_client)
):
    """
    루트 ID를 받아 루트의 핵심 정보(이름, 승률, 추천수, 업데이트 일자)와
    해당 루트 제작자의 티어 정보를 조합하여 반환합니다.
    """
    
    # --- 1. 루트 정보 API 호출 ---
    # er.py 서비스에 있는 get_route_async 함수를 호출합니다.
    route_data = await er.get_route_async(er_client, route_id)
    
    # 만약 API로부터 받은 데이터가 없으면 404 에러를 반환합니다.
    if not route_data:
        raise HTTPException(status_code=404, detail=f"Route ID '{route_id}'를 찾을 수 없습니다.")

    # 필요한 루트 정보가 담긴 객체를 안전하게 추출합니다.
    route_info = route_data.get('recommendWeaponRoute', {})
    userNickname = route_info.get('userNickname') # 제작자 티어 조회를 위해 닉네임을 가져옵니다.

    # --- 2. 제작자 랭크 정보 API 호출 및 티어 계산 ---
    creator_tier = "Unranked" # API 호출 실패 등을 대비한 기본값 설정
    if userNickname:
        # 먼저 닉네임으로 UID(userId)를 조회합니다.
        userId = await er.get_user_id_by_nickname_async(er_client, userNickname)
        if userId:
            # er.py의 get_user_rank_async 함수를 호출합니다.
            creator_rank_data = await er.get_user_rank_async(er_client, userId)
        if creator_rank_data:
            mmr = creator_rank_data.get('mmr', -1)
            rank = creator_rank_data.get('rank', -1)
            # common/utils.py의 get_tier 함수로 티어를 계산합니다.
            creator_tier = get_tier(mmr, rank)
    
    # --- 3. 프론트엔드에 전달할 최종 데이터 조합 ---
    # MVP에 필요한 5가지 핵심 정보만 모아서 반환합니다.
    return {
        "routeName": route_info.get('title'),
        "characterCode":route_info.get('characterCode'),
        "winRate": route_info.get('v2WinRate'),
        "likes": route_info.get('v2Like'),
        "lastUpdated": route_info.get('updateDtm'), # 프론트에서 날짜 형식으로 변환 필요
        "creatorTier": creator_tier
    }