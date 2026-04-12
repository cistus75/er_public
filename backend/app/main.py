# app/main.py

import asyncio
import logging
import time
import urllib.parse
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

# 분리된 모듈들 import
from .core.setting import get_settings
from .db.db import connect_to_mongo, close_mongo_connection, get_database
from .common.utils import set_dynamic_character_map
from .routers import user, jobs, route
from .exceptions.error import (
    UserNotFoundException,
    NoRecentGamesException,
    user_not_found_exception_handler,
    no_recent_games_exception_handler,
    generic_exception_handler,
)

# --- 로거 설정 ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(name)s (%(filename)s:%(lineno)d) - %(message)s')
settings = get_settings()

class HealthCheckFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # 로그 메시지에 "/health" 문자열이 포함되어 있으면
        # False를 반환하여 로그에서 제외시킵니다.
        return record.getMessage().find("/health") == -1

# Uvicorn의 'access' 로거에 필터를 추가합니다.
logging.getLogger("uvicorn.access").addFilter(HealthCheckFilter())

# --- Lifespan: 앱 시작/종료 시 실행될 로직 (최신 방식) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- 앱 시작 시 ---
    await connect_to_mongo()
    
    # DB에서 수집기가 최신화한 동적 캐릭터 맵을 메모리에 캐싱
    try:
        db = await get_database()
        if db is not None:
            doc = await db['metadata'].find_one({'_id': 'character_map'})
            if doc and 'map' in doc:
                set_dynamic_character_map(doc['map'])
                logger.info("MongoDB에서 최신 동적 캐릭터 맵을 메모리에 캐싱 완료했습니다.")
    except Exception as e:
        logger.warning(f"동적 캐릭터 맵 캐싱 실패 (Fallback 사용할 예정): {e}")

    # 세분화된 타임아웃 설정
    er_timeout = httpx.Timeout(10.0, connect=30.0)
    app.state.er_client = httpx.AsyncClient(
        base_url=settings.ER_BASE_URL,
        headers={"x-api-key": settings.OPEN_API_KEY},
        timeout=er_timeout
    )
    

    # Gemini API 동시 요청 수를 5개로 제한하는 세마포어
    app.state.gemini_semaphore = asyncio.Semaphore(5)
    
    yield # 애플리케이션 실행
    
    # --- 앱 종료 시 ---
    await close_mongo_connection()
    await app.state.er_client.aclose()

# --- FastAPI 앱 생성 및 설정 ---
app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

# Rate Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# --- 병목 추적 및 상세 로깅 미들웨어 ---
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    path = request.url.path
    if path.startswith("/api/users/"):
        decoded_path = urllib.parse.unquote(path)
        status = "성공" if response.status_code == 200 else f"실패({response.status_code})"
        
        if "/num/" in decoded_path:
            nickname = decoded_path.split("/num/")[-1]
            logger.info(f"[유저 번호조회] 닉네임='{nickname}' | 결과={status} | 총 소요시간={process_time:.2f}초")
        elif "/stat/" in decoded_path:
            user_id = decoded_path.split("/stat/")[-1]
            logger.info(f"[통계+AI 분석] 유저번호='{user_id}' | 결과={status} | 총 소요시간={process_time:.2f}초")
            
    return response

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": f"Welcome to the {settings.APP_NAME} API!"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.api_route("/uptime", methods=["GET", "HEAD"])
async def uptime_check():
    return {"status": "uptime health check"}


# 커스텀 예외 핸들러 등록
app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
app.add_exception_handler(NoRecentGamesException, no_recent_games_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# 분리된 라우터 포함
app.include_router(user.router)
app.include_router(jobs.router)
app.include_router(route.router)

