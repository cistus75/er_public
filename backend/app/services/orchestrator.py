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
    
    if tier != 'unrank':
        # 데미갓 이상 통계가 쌓이기 전까지 미스릴 통계를 공통 기준으로 사용합니다.
        query_tier = tier if tier not in ['demigod', 'titan', 'immortal'] else 'mithril'
        tasks.append(db.tier_overall_stats.find_one({'tier': query_tier}, {'_id': 0}))
    else:
        tasks.append(asyncio.sleep(0, result=None))

    if not rank_stat.get('no_record') and (code := rank_stat.get('most_used_character_code')):
        tasks.append(db.high_mmr_char_stats.find_one({'character_code': code}, {'_id': 0}))
    else:
        tasks.append(asyncio.sleep(0, result=None))

    if not normal_stat.get('no_record') and (code := normal_stat.get('most_used_character_code')):
        tasks.append(db.high_mmr_char_stats.find_one({'character_code': code}, {'_id': 0}))
    else:
        tasks.append(asyncio.sleep(0, result=None))

    results = await asyncio.gather(*tasks)
    
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
    import time
    total_start = time.perf_counter()

    er_start = time.perf_counter()
    rank_result, (rank_stat, normal_stat, cobalt_stat, retry_count) = await asyncio.gather(
        er.get_user_rank_async(er_client, userId),
        er.get_user_games_all_modes_async(er_client, userId),
    )
    er_duration = time.perf_counter() - er_start

    # 분석할 기록이 없으면 라우터에서 404로 처리할 수 있도록 None을 반환합니다.
    if rank_stat.get('no_record') and normal_stat.get('no_record'):
        return None

    mmr = rank_result.get('mmr', -1) if rank_result else -1
    rank = rank_result.get('rank', -1) if rank_result else -1
    tier = get_tier(mmr, rank)
    nickname = rank_result.get('nickname') if rank_result else rank_stat.get('nickname', '알 수 없음')

    db_start = time.perf_counter()
    tier_stats_result, rank_most_char_dia_stats, normal_most_char_dia_stats = await get_comparison_stats(
        db, tier, rank_stat, normal_stat
    )
    db_duration = time.perf_counter() - db_start

    tasks = {}
    if not rank_stat.get('no_record'):
        # 동기 배지 계산이 이벤트 루프를 막지 않도록 별도 스레드에서 실행합니다.
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

    # 일부 AI 작업이 실패해도 나머지 결과는 계속 반환합니다.
    ai_start = time.perf_counter()
    task_results = await asyncio.gather(*tasks.values(), return_exceptions=True)
    results_dict = dict(zip(tasks.keys(), task_results))
    ai_duration = time.perf_counter() - ai_start

    ai_status = []
    for key, label in [('rank_ai', 'R'), ('normal_ai', 'N'), ('cobalt_ai', 'C'), ('angpyeong_ai', 'A')]:
        value = results_dict.get(key)
        if value is None:
            ai_status.append(f"{label}:-")
        elif isinstance(value, Exception):
            logger.error(f"AI 분석 실패 [{key}]: {value}")
            results_dict[key] = f"분석 실패 ({key})"
            ai_status.append(f"{label}:ERR")
        else:
            ai_status.append(f"{label}:OK")

    def get_count(s): return s.get('total_games_analyzed', 0) if not s.get('no_record') else 0
    m_counts = f"R:{get_count(rank_stat)} N:{get_count(normal_stat)} C:{get_count(cobalt_stat)}"
    most_char = rank_stat.get('most_used_character_name', '없음')

    total_duration = time.perf_counter() - total_start
    
    logger.info(
        f"[Search Summary] Nick: {nickname} ({tier.upper()}/{most_char}) | Matches: ({m_counts}) | "
        f"Total: {total_duration:.2f}s (API:{er_duration:.2f}s | AI:{ai_duration:.2f}s) | "
        f"Retry: {retry_count}회 | AI Status: [{' '.join(ai_status)}]"
    )

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
