# app/core/setting.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # Pydantic이 환경 변수를 읽도록 설정 (대소문자 구분 안 함)
    model_config = SettingsConfigDict(case_sensitive=False)

    # ER API
    OPEN_API_KEY: str
    ER_BASE_URL: str = "https://open-api.bser.io"

    # Google Gemini API
    # GEMINI_API_KEY: str
    # GOOGLE_API_KEY 방식으로 변경되어 더 이상 사용하지 않음

    # MongoDB
    MONGO_URI: str
    MONGO_DB_NAME: str = "er-user-insight"

    # Scheduler
    SCHEDULER_SECRET_KEY: str
    
    # App Settings
    APP_NAME: str = "ER User Insight"
    SEASON_ID: int = 37
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        'https://er-user-insight-gsn4.vercel.app',
        'https://adina-crystal-ball.vercel.app',
        'https://adina-test.vercel.app',
    ]

# @lru_cache: Settings 객체를 한 번만 생성하고 캐싱하여 성능 향상
@lru_cache
def get_settings() -> Settings:
    return Settings()