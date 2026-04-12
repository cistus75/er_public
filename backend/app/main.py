# app/main.py

import asyncio
import logging
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
from .db.db import connect_to_mongo, close_mongo_connection
from .routers import user, jobs, route
from .exceptions.error import (
    UserNotFoundException,
    NoRecentGamesException,
    user_not_found_exception_handler,
    no_recent_games_exception_handler,
    generic_exception_handler,
)

# --- 로거 설정 ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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

