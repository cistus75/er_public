import asyncio

import httpx
from fastapi import Request

def get_er_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.er_client


def get_gemini_semaphore(request: Request) -> asyncio.Semaphore:
    return request.app.state.gemini_semaphore
