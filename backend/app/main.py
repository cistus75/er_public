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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(name)s (%(filename)s:%(lineno)d) - %(message)s')
settings = get_settings()

class HealthCheckFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # 헬스 체크 요청은 주기적으로 발생하므로 접근 로그에서 제외합니다.
        return record.getMessage().find("/health") == -1

logging.getLogger("uvicorn.access").addFilter(HealthCheckFilter())

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    
    # 수집기가 갱신한 캐릭터 이름을 API 응답에도 반영합니다.
    try:
        db = await get_database()
        if db is not None:
            doc = await db['metadata'].find_one({'_id': 'character_map'})
            if doc and 'map' in doc:
                set_dynamic_character_map(doc['map'])
                logger.info("MongoDB에서 최신 동적 캐릭터 맵을 메모리에 캐싱 완료했습니다.")
    except Exception as e:
        logger.warning(f"동적 캐릭터 맵 캐싱 실패 (기본 맵 사용): {e}")

    # 연결과 응답에 서로 다른 제한을 두어 외부 API 지연을 구분합니다.
    er_timeout = httpx.Timeout(10.0, connect=30.0)
    app.state.er_client = httpx.AsyncClient(
        base_url=settings.ER_BASE_URL,
        headers={"x-api-key": settings.OPEN_API_KEY},
        timeout=er_timeout
    )
    

    # 동시 AI 요청 수를 제한해 API 과부하를 막습니다.
    app.state.gemini_semaphore = asyncio.Semaphore(5)
    
    yield
    
    await close_mongo_connection()
    await app.state.er_client.aclose()

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

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


app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
app.add_exception_handler(NoRecentGamesException, no_recent_games_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(user.router)
app.include_router(jobs.router)
app.include_router(route.router)
