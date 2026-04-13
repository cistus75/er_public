# app/services/eternal_return.py

import logging
import httpx

# ✨ get_user_games.py 파일의 GameStatsAnalyzer 클래스를 직접 import 합니다.
# 이 클래스도 나중에 이 서비스 파일 안으로 옮기는 것을 고려할 수 있습니다.
from .get_user_games import GameStatsAnalyzer
from..core.setting import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

async def get_user_id_by_nickname_async(client: httpx.AsyncClient, nickname: str):
    """닉네임을 통해 사용자의 내부 UID(userId)를 가져옵니다."""
    url = f"/v1/user/nickname?query={nickname}"
    try:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get('code') == 200:
            return data.get('user', {}).get('uid')
        return None
    except Exception as e:
        logger.error(f"UID 조회 실패 (nickname: {nickname}): {e}")
        return None

async def get_user_rank_async(client: httpx.AsyncClient, userId: str)  :
    """지정된 유저의 랭크 정보를 비동기적으로 가져옵니다."""
    url = f"/v1/rank/uid/{userId}/{settings.SEASON_ID}/3"
    try:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        userRank = data.get('userRank')
        if userRank and userRank.get('mmr') == 2400 and userRank.get('rank') == 0:
            return {'mmr': -1, 'rank': -1}
        return userRank
    except Exception as e:
        logger.error(f"유저 랭크 정보 조회 실패 (userId : {userId}): {e}")
        return None

async def get_user_games_all_modes_async(client: httpx.AsyncClient, userId: str):
    """
    GameStatsAnalyzer를 사용하여 유저의 랭크/일반/코발트 게임 통계를 모두 가져옵니다.
    """
    try:
        analyzer = GameStatsAnalyzer(userId, client, settings.SEASON_ID)
        await analyzer.collect_match_data(20)
        rank_stat = analyzer.get_detailed_stats('ranked')
        normal_stat = analyzer.get_detailed_stats('normal')
        cobalt_stat = analyzer.get_detailed_stats('cobalt')
        return rank_stat, normal_stat, cobalt_stat
    except Exception as e:
        logger.error(f"유저 게임 통계 분석 중 오류 발생 (userId: {userId}): {e}")
        # 실패 시 모든 모드에 대해 'no_record'를 반환하여 오류를 전파합니다.
        no_record_stat = {"no_record": True}
        return no_record_stat, no_record_stat, no_record_stat
    

async def get_route_async(client: httpx.AsyncClient, route_id: int):
    """지정된 루트 ID의 상세 정보를 비동기적으로 가져옵니다."""
    url = f"/v1/weaponRoutes/recommend/{route_id}"
    try:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get('code') == 200:
            return data.get('result')
        return None
    except Exception as e:
        logger.error(f"루트 정보 조회 실패 (route_id: {route_id}): {e}")
        return None