# app/services/ai.py

import os
import json
import logging
import asyncio
import itertools
from functools import lru_cache

import httpx

logger = logging.getLogger(__name__)

# =========================================================
# 🔑 [API 키 로테이션 설정]
# 환경변수 'GOOGLE_API_KEYS'에서 쉼표로 구분된 키 목록을 로드합니다.
# =========================================================
API_KEYS_STR = os.getenv("GOOGLE_API_KEYS", "")
API_KEYS = [k.strip() for k in API_KEYS_STR.split(",") if k.strip()]

if not API_KEYS:
    logger.warning("GOOGLE_API_KEYS 환경 변수가 설정되지 않았습니다. AI 분석 기능을 사용할 수 없습니다.")

# =========================================================
# 🎯 [라운드 로빈 키 분배기]
# 동시 요청이 들어와도 각 요청이 서로 다른 프로젝트 키를 자동으로 배정받아
# 특정 프로젝트에 호출이 몰리는 현상을 방지합니다.
# itertools.count는 원자적(atomic)이므로 asyncio 환경에서 안전합니다.
# =========================================================
_key_counter = itertools.count()

def _get_next_key_index() -> int:
    """라운드 로빈 방식으로 다음 키 인덱스를 반환합니다."""
    return next(_key_counter) % len(API_KEYS)


# =========================================================
# 📄 [프롬프트 파일 캐싱]
# 요청마다 디스크를 읽는 대신, 첫 번째 로드 이후 메모리에 캐싱합니다.
# =========================================================
@lru_cache(maxsize=None)
def _load_prompt(prompt_path: str) -> str:
    """프롬프트 파일을 로드하고 결과를 메모리에 캐싱합니다."""
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


def _resolve_prompt_path(prompt_filename: str) -> str:
    """서비스 파일 위치 기준으로 프롬프트 파일의 절대 경로를 반환합니다."""
    services_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(os.path.dirname(services_dir))
    return os.path.join(backend_dir, "prompt", prompt_filename)


# =========================================================
# 🔄 [REST API 호출 함수]
# =========================================================
async def _call_gemini_api(api_key: str, system_prompt: str) -> str:
    """httpx를 사용한 REST API 직접 호출 함수"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": system_prompt}]}]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, timeout=10.0)
        if response.status_code != 200:
            logger.error(f"AI 분석 실패 상세 (Status {response.status_code}): {response.text}")
        response.raise_for_status()
        data = response.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as e:
            logger.error(f"예상치 못한 응답 포맷: {data}")
            raise Exception("API 응답 구조 분석 실패") from e


# =========================================================
# 🤖 [AI 분석 메인 함수]
# =========================================================
async def get_ai_analysis_async(
    prompt_filename: str,
    stat_data: dict,
    semaphore: asyncio.Semaphore,
    comparison_stats: dict = None,
) -> str:
    """
    주어진 프롬프트 파일과 통계 데이터를 기반으로 AI 분석을 수행합니다.

    Args:
        prompt_filename: prompt/ 폴더 내 프롬프트 파일명
        stat_data: 분석할 게임 통계 딕셔너리
        semaphore: Gemini API 동시 요청 제어용 세마포어
        comparison_stats: 비교 기준 통계 (선택)
        most_character_number: 최다 사용 캐릭터 코드 (선택)

    Returns:
        AI 분석 결과 문자열
    """
    # 1. 데이터 검증
    if not stat_data or stat_data.get("no_record"):
        return "분석할 데이터가 부족하다요. 게임을 좀 더 하고 오라요!"

    # 2. API 키 검증
    if not API_KEYS:
        return "AI API 키가 설정되지 않아 점을 볼 수 없다요. 관리자에게 문의해라요!"

    # 3. 프롬프트 파일 로드 (캐시 우선)
    try:
        prompt_path = _resolve_prompt_path(prompt_filename)
        base_prompt = _load_prompt(prompt_path)
    except FileNotFoundError:
        logger.error("프롬프트 파일을 찾을 수 없습니다: %s", prompt_filename)
        return f"시스템 오류: '{prompt_filename}' 파일을 찾을 수 없다요."
    except Exception:
        logger.exception("프롬프트 파일 로드 중 예기치 않은 오류가 발생했습니다: %s", prompt_filename)
        return "시스템 오류: 프롬프트 파일을 읽는 중 문제가 생겼다요."

    # 4. 프롬프트 포맷팅
    # stat_data에 character_role과 stat_grades가 이미 포함되어 있으므로 추출해서 주입합니다.
    try:
        character_role = stat_data.get("character_role", "알 수 없음")
        stat_grades = stat_data.get("stat_grades", {})
        system_prompt = base_prompt.format(
            character_role=character_role,
            stat_grades_json=json.dumps(stat_grades, indent=2, ensure_ascii=False),
            stat_data_json=json.dumps(stat_data, indent=2, ensure_ascii=False),
            comparison_stats_json=json.dumps(comparison_stats or {}, indent=2, ensure_ascii=False),
        )
    except KeyError as e:
        logger.error(
            "프롬프트 포맷팅 오류 (%s): 키 %s 누락", prompt_filename, e
        )
        return "시스템 오류: 프롬프트와 데이터 형식이 맞지 않는다요."

    # 5. 라운드 로빈 키 선택 + 실패 시 전체 키 순차 폴백
    is_angpyeong = 'angpyeong' in prompt_filename

    async with semaphore:
        # 라운드 로빈으로 시작 키를 결정하여 프로젝트별 부하를 균등 분배합니다.
        start_idx = _get_next_key_index()
        num_keys = len(API_KEYS)
        last_exception = None

        for i in range(num_keys):
            key_idx = (start_idx + i) % num_keys
            selected_key = API_KEYS[key_idx]

            try:
                response_text = await _call_gemini_api(selected_key, system_prompt)
                logger.info(
                    "AI 분석 성공 | prompt=%s | key=...%s (시도 %d/%d)",
                    prompt_filename,
                    selected_key[-4:],
                    i + 1,
                    num_keys,
                )
                return response_text

            except httpx.HTTPStatusError as e:
                last_exception = e
                status = e.response.status_code
                logger.warning(
                    "AI 분석 API 오류 (Status %d) | prompt=%s | key=...%s | 다음 키로 전환합니다. (%d/%d)",
                    status, prompt_filename, selected_key[-4:], i + 1, num_keys,
                )
                # 429/503은 다른 프로젝트 키로 바꾸면 성공 가능성이 높으므로 짧은 유예 후 전환
                if status in (429, 503):
                    await asyncio.sleep(0.3)
                continue

            except httpx.RequestError as e:
                last_exception = e
                logger.warning(
                    "AI 분석 네트워크/타임아웃 오류 | prompt=%s | key=...%s | 다음 키로 전환합니다. (%d/%d)",
                    prompt_filename, selected_key[-4:], i + 1, num_keys,
                )
                continue

            except Exception as e:
                last_exception = e
                logger.warning(
                    "AI 분석 중 예기치 못한 오류 | prompt=%s | key=...%s | 다음 키로 전환합니다. (%d/%d)",
                    prompt_filename, selected_key[-4:], i + 1, num_keys,
                )
                continue

        # 모든 키를 시도했음에도 성공하지 못한 경우
        logger.warning(
            "AI 분석 전체 키 소진 | prompt=%s | 총 %d개 키 시도 실패 (최종 오류: %s)",
            prompt_filename, num_keys, str(last_exception),
        )
        if is_angpyeong:
            return "짐의 권속들이 너무 많아 피곤하구나! 조금 이따가 오거라!"
        return (
            "지금 접속자가 너무 많아 아디나의 신력이 바닥났다요! \n"
            "잠시 후에 다시 시도해주라요. "
        )