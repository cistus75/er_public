# app/services/ai.py

import os
import json
import logging
import asyncio
import random
from functools import lru_cache

import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
import tenacity
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log, retry_if_exception_type

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
# 🔄 [재시도(Retry) 로직]
# 일시적 오류 및 과부하 시 지수 백오프(Exponential Backoff)로 재시도합니다.
# =========================================================
@retry(
    retry=retry_if_exception_type(
        (
            google_exceptions.ResourceExhausted,
            google_exceptions.DeadlineExceeded,
            google_exceptions.ServiceUnavailable,
        )
    ),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    stop=stop_after_attempt(3),
    before_sleep=before_sleep_log(logger, logging.INFO),
)
async def _generate_with_retry(model, system_prompt: str):
    """tenacity 재시도 로직이 적용된 Gemini API 호출 함수."""
    return await model.generate_content_async(
        system_prompt,
        request_options={"timeout": 30},
    )


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
        return "AI API 키가 설정되지 않아 점을 볼 수 없다요. (서버 설정 오류)"

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

    # 5. API 키 선택 및 호출
    # [레이스 컨디션 수정]
    # genai.configure()는 프로세스 전역 상태를 변경합니다.
    # 세마포어 내부에서 configure → model 생성을 연속 실행하면,
    # asyncio의 단일 스레드 특성상 두 호출 사이에 문맥 전환이 없어 안전합니다.
    async with semaphore:
        selected_key = random.choice(API_KEYS)
        genai.configure(api_key=selected_key)
        model = genai.GenerativeModel("models/gemma-3-27b-it")

        try:
            response = await _generate_with_retry(model, system_prompt)
            logger.info(
                "AI 분석 성공 | prompt=%s | key=...%s",
                prompt_filename,
                selected_key[-4:],
            )
            return response.text

        except tenacity.RetryError:
            logger.warning(
                "AI 분석 재시도 한도 초과 | prompt=%s | key=...%s (할당량 부족 추정)",
                prompt_filename,
                selected_key[-4:],
            )
            return (
                "지금 접속자가 너무 많아 아디나의 신력이 바닥났다요! 😵\n"
                "잠시 후에 다시 시도해주라요. (할당량 초과)"
            )

        except Exception:
            logger.exception(
                "AI 분석 중 예기치 않은 오류 | prompt=%s", prompt_filename
            )
            return "점을 보는 도중 수정구슬이 깨졌다요... (알 수 없는 오류 발생)"