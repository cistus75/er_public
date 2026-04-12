# app/dependencies.py
# 라우터 간 공유되는 공통 의존성 함수를 단일 모듈로 관리합니다.

import asyncio
import httpx
from fastapi import Request


def get_er_client(request: Request) -> httpx.AsyncClient:
    """앱 lifespan에서 생성된 ER API 클라이언트를 반환합니다."""
    return request.app.state.er_client


def get_gemini_semaphore(request: Request) -> asyncio.Semaphore:
    """앱 lifespan에서 생성된 Gemini API 세마포어를 반환합니다."""
    return request.app.state.gemini_semaphore
