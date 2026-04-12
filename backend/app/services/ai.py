import os
import json
import logging
import asyncio
import random
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
import tenacity
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log, retry_if_exception_type

logger = logging.getLogger(__name__)

# =========================================================
# 🔑 [키 로테이션 설정]
# Render 환경변수 'GOOGLE_API_KEYS'에서 쉼표로 구분된 키들을 불러옵니다.
# =========================================================
API_KEYS_STR = os.getenv("GOOGLE_API_KEYS", "")
API_KEYS = [k.strip() for k in API_KEYS_STR.split(",") if k.strip()]

if not API_KEYS:
    logger.warning("⚠️ 경고: GOOGLE_API_KEYS 환경 변수가 설정되지 않았습니다.")

# =========================================================
# 🔄 [재시도(Retry) 로직 설정]
# 일시적인 오류나 과부하 시 지수 백오프(Exponential Backoff)로 재시도합니다.
# =========================================================
@retry(
    retry=retry_if_exception_type(
        (google_exceptions.ResourceExhausted, 
         google_exceptions.DeadlineExceeded, 
         google_exceptions.ServiceUnavailable)
    ),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    stop=stop_after_attempt(3), # 키가 많으므로 빠르게 실패하고 다른 키로 넘어가는 게 낫습니다.
    before_sleep=before_sleep_log(logger, logging.INFO)
)
async def generate_gemini_content_with_retry(model, system_prompt: str):
    """
    tenacity를 사용하여 재시도 로직을 적용한 Gemini API 호출 함수
    """
    return await model.generate_content_async(
        system_prompt,
        request_options={"timeout": 30}
    )

async def get_ai_analysis_async(
    prompt_filename: str,
    stat_data: dict,
    semaphore: asyncio.Semaphore,
    comparison_stats: dict = None,
    most_character_number: int = None
):
    """
    주어진 프롬프트 파일과 데이터를 기반으로 AI 분석을 비동기적으로 수행합니다.
    (gemini-2.0-flash-lite 전용)
    """
    # 1. 데이터 검증
    if not stat_data or stat_data.get('no_record'):
        return "분석할 데이터가 부족하다요. 게임을 좀 더 하고 오라요!"

    # 2. API 키 검증
    if not API_KEYS:
        return "AI API 키가 설정되지 않아 점을 볼 수 없다요. (서버 설정 오류)"

    # 3. 프롬프트 파일 로드
    try:
        current_file_path = os.path.abspath(__file__)
        services_dir = os.path.dirname(current_file_path)
        app_dir = os.path.dirname(services_dir)
        backend_dir = os.path.dirname(app_dir)
        prompt_path = os.path.join(backend_dir, 'prompt', prompt_filename)
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            base_prompt = f.read()
            
    except FileNotFoundError:
        logger.error(f"프롬프트 파일을 찾을 수 없습니다: {prompt_path}")
        return f"시스템 오류: '{prompt_filename}' 파일을 찾을 수 없다요."
    except Exception as e:
        logger.error(f"프롬프트 로드 중 오류: {e}")
        return "시스템 오류: 프롬프트 파일을 읽는 중 문제가 생겼다요."

    # 4. 프롬프트 포맷팅
    try:
        system_prompt = base_prompt.format(
            most_character_number=most_character_number,
            stat_data=stat_data,
            comparison_stats=comparison_stats or {},
            stat_data_json=json.dumps(stat_data, indent=2, ensure_ascii=False),
            comparison_stats_json=json.dumps(comparison_stats or {}, indent=2, ensure_ascii=False)
        )
    except KeyError as e:
        logger.error(f"프롬프트 포맷팅 오류 ({prompt_filename}): 키 {e} 누락")
        return "시스템 오류: 프롬프트와 데이터 형식이 맞지 않는다요."

    # 5. [핵심] 키 로테이션 및 API 호출
    # 호출할 때마다 10개의 키 중 하나를 랜덤으로 뽑습니다.
    selected_key = random.choice(API_KEYS)
    genai.configure(api_key=selected_key)

    async with semaphore:
        try:
            # ✨ [모델 설정] gemini-2.0-flash 단독 사용
            model = genai.GenerativeModel('models/gemma-3-27b-it')
            
            response = await generate_gemini_content_with_retry(model, system_prompt)
            
            # 성공 로그 (키 뒷자리 로깅)
            logger.info(f"✨ AI 분석 성공 ({prompt_filename}) - Key: ...{selected_key[-4:]}")
            return response.text

        except tenacity.RetryError:
            # 3번 재시도 후에도 실패한 경우 (높은 확률로 할당량 초과)
            logger.warning(f"🚨 최대 재시도 초과 ({prompt_filename}) - 할당량 부족 추정")
            return (
                "지금 접속자가 너무 많아 아디나의 신력이 바닥났다요! 😵\n"
                "잠시 후에 다시 시도해주라요. (할당량 초과)"
            )

        except Exception as e:
            # 그 외 알 수 없는 에러
            logger.error(f"❌ AI 분석 중 오류: {type(e).__name__}: {e}", exc_info=True)
            return "점을 보는 도중 수정구슬이 깨졌다요... (알 수 없는 오류 발생)"