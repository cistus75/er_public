import logging
from fastapi import APIRouter, Depends, HTTPException
import httpx

from ..services import er
from ..common.utils import get_tier
from ..dependencies import get_er_client

logger = logging.getLogger(__name__)

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
    
    route_data = await er.get_route_async(er_client, route_id)
    
    # 존재하지 않는 루트는 상세 정보를 만들 수 없습니다.
    if not route_data:
        raise HTTPException(status_code=404, detail=f"Route ID '{route_id}'를 찾을 수 없습니다.")

    route_info = route_data.get('recommendWeaponRoute', {})
    userNickname = route_info.get('userNickname')

    creator_tier = "Unranked"
    if userNickname:
        userId = await er.get_user_id_by_nickname_async(er_client, userNickname)
        if userId:
            creator_rank_data = await er.get_user_rank_async(er_client, userId)
        if creator_rank_data:
            mmr = creator_rank_data.get('mmr', -1)
            rank = creator_rank_data.get('rank', -1)
            creator_tier = get_tier(mmr, rank)
    
    return {
        "routeName": route_info.get('title'),
        "characterCode":route_info.get('characterCode'),
        "winRate": route_info.get('v2WinRate'),
        "likes": route_info.get('v2Like'),
        "lastUpdated": route_info.get('updateDtm'),
        "creatorTier": creator_tier
    }
