# app/exceptions/error.py

import logging
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

# --- 커스텀 예외 클래스 ---
class UserNotFoundException(Exception):
    def __init__(self, nickname: str):
        self.nickname = nickname

class NoRecentGamesException(Exception):
    pass

# --- 예외 핸들러 ---
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": f"유저 '{exc.nickname}'을(를) 찾을 수 없습니다."},
    )

async def no_recent_games_exception_handler(request: Request, exc: NoRecentGamesException):
    return JSONResponse(
        status_code=404,
        content={"detail": "분석할 최근 게임 기록(랭크/일반)을 찾을 수 없습니다."},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """예상치 못한 모든 예외를 처리하는 최후의 보루"""
    logger.error(f"처리되지 않은 예외 발생: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "서버 내부 오류가 발생했습니다."},
    )