# app/services/orchestrator.py

import asyncio
import logging
import httpx
from motor.motor_asyncio import AsyncIOMotorClient

from. import ai, er
from ..common.utils import get_tier
from .get_badges import get_badges

logger = logging.getLogger(__name__)

async def get_comparison_stats(
    db: AsyncIOMotorClient, tier: str, rank_stat: dict, normal_stat: dict
):
    """DB에서 비교 통계 데이터를 비동기 병렬로 조회합니다."""
    tasks = []
    
    # 티어 통계 쿼리
    if tier != 'unrank':
        query_tier = tier if tier not in ['titan', 'immortal'] else 'mithril'
        tasks.append(db.tier_overall_stats.find_one({'tier': query_tier}, {'_id': 0}))
    else:
        tasks.append(asyncio.sleep(0, result=None))

    # 랭크 모스트 캐릭터 통계 쿼리
    if not rank_stat.get('no_record') and (code := rank_stat.get('most_used_character_code')):
        tasks.append(db.high_mmr_char_stats.find_one({'character_code': code}, {'_id': 0}))
    else:
        tasks.append(asyncio.sleep(0, result=None))

    # 일반 모스트 캐릭터 통계 쿼리
    if not normal_stat.get('no_record') and (code := normal_stat.get('most_used_character_code')):
        tasks.append(db.high_mmr_char_stats.find_one({'character_code': code}, {'_id': 0}))
    else:
        tasks.append(asyncio.sleep(0, result=None))

    # 모든 DB 쿼리를 동시에 실행
    results = await asyncio.gather(*tasks)
    
    # ✅ 수정된 부분: results 리스트의 각 항목을 순서대로 반환합니다.
    return results[0], results[1], results[2]


async def get_user_profile_data(
    userId: str,
    er_client: httpx.AsyncClient,
    gemini_semaphore: asyncio.Semaphore,
    db: AsyncIOMotorClient
):
    """
    여러 서비스를 조율하여 최종 유저 프로필 데이터를 생성하는 핵심 함수.
    """
    logger.info(f"유저 프로필 데이터 생성 시작 (userId: {userId})")

    # 1. ER API에서 랭크 정보와 게임 통계를 병렬로 수집합니다.
    rank_result, (rank_stat, normal_stat, cobalt_stat) = await asyncio.gather(
        er.get_user_rank_async(er_client, userId),
        er.get_user_games_all_modes_async(er_client, userId),
    )

    # 분석할 게임 기록이 전혀 없는 경우, None을 반환하여 라우터에서 404 처리를 하도록 합니다.
    if rank_stat.get('no_record') and normal_stat.get('no_record'):
        return None

    mmr = rank_result.get('mmr', -1) if rank_result else -1
    rank = rank_result.get('rank', -1) if rank_result else -1
    tier = get_tier(mmr, rank)

    # 2. DB에서 비교 통계 데이터를 비동기 병렬로 수집합니다.
    tier_stats_result, rank_most_char_dia_stats, normal_most_char_dia_stats = await get_comparison_stats(
        db, tier, rank_stat, normal_stat
    )

    # 3. AI 분석 및 뱃지 생성을 병렬로 처리할 작업을 구성합니다.
    tasks = {}
    if not rank_stat.get('no_record'):
        # get_badges는 동기 함수이므로 to_thread로 감싸 이벤트 루프 차단을 방지합니다.
        tasks['badges'] = asyncio.to_thread(get_badges, rank_stat, rank_result)
        tasks['rank_ai'] = ai.get_ai_analysis_async(
            prompt_filename='rank_ai_analysis_prompt.txt',
            stat_data=rank_stat, semaphore=gemini_semaphore,
            comparison_stats=rank_most_char_dia_stats,
        )
        tasks['angpyeong_ai'] = ai.get_ai_analysis_async(
            prompt_filename='angpyeong_ai_analysis_prompt.txt',
            stat_data=rank_stat, semaphore=gemini_semaphore,
            comparison_stats=rank_most_char_dia_stats,
        )

    if not normal_stat.get('no_record'):
        tasks['normal_ai'] = ai.get_ai_analysis_async(
            prompt_filename='normal_ai_analysis_prompt.txt',
            stat_data=normal_stat, semaphore=gemini_semaphore,
            comparison_stats=normal_most_char_dia_stats,
        )

    if not cobalt_stat.get('no_record'):
        tasks['cobalt_ai'] = ai.get_ai_analysis_async(
            prompt_filename='cobalt_ai_analysis_prompt.txt',
            stat_data=cobalt_stat, semaphore=gemini_semaphore,
        )

    # 4. 모든 병렬 작업을 실행하고 결과를 수집합니다.
    # return_exceptions=True를 통해 일부 작업이 실패해도 전체가 중단되지 않습니다.
    task_results = await asyncio.gather(*tasks.values(), return_exceptions=True)
    results_dict = dict(zip(tasks.keys(), task_results))

    # 5. 실패한 작업이 있는지 확인하고 로깅합니다.
    for key, value in results_dict.items():
        if isinstance(value, Exception):
            logger.error(f"병렬 작업 '{key}' 실패: {value}", exc_info=value)
            results_dict[key] = f"작업 '{key}' 처리 중 오류 발생"

    logger.info(f"유저 프로필 데이터 생성 완료 (userId: {userId})")

    # 6. 모든 데이터를 취합하여 최종 응답 객체를 구성합니다.
    return {
        "rank": rank_result,
        "tier": tier,
        "rank_stat": rank_stat,
        "normal_stat": normal_stat,
        "cobalt_stat": cobalt_stat,
        "badges": results_dict.get('badges'),
        "rank_ai_analysis": results_dict.get('rank_ai', "분석할 최근 랭크 게임 기록이 없는거다요."),
        "normal_ai_analysis": results_dict.get('normal_ai', "분석할 최근 일반 게임 기록이 없는거다요."),
        "angpyeong_ai_analysis": results_dict.get('angpyeong_ai', "분석할 최근 랭크 게임 기록이 없는거다요."),
        "cobalt_ai_analysis": results_dict.get('cobalt_ai', "분석할 최근 코발트 게임 기록이 없는거다요."),
        "tier_stats": tier_stats_result,
        "rank_most_char_dia_stats": rank_most_char_dia_stats,
        "normal_most_char_dia_stats": normal_most_char_dia_stats
    }