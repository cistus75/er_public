from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 환경 변수 이름의 대소문자를 구분하지 않도록 설정합니다.
    model_config = SettingsConfigDict(case_sensitive=False)

    # ER API
    OPEN_API_KEY: str
    ER_BASE_URL: str = "https://open-api.bser.io"

    # MongoDB
    MONGO_URI: str
    MONGO_DB_NAME: str = "er-user-insight"

    # 스케줄러
    SCHEDULER_SECRET_KEY: str
    
    # 애플리케이션
    APP_NAME: str = "ER User Insight"
    SEASON_ID: int = 39
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "https://er-public.vercel.app",
        "https://er-user-insight-gsn4.vercel.app",
        "https://adina-crystal-ball.vercel.app",
        "https://adina-test.vercel.app",
    ]


# 설정 객체는 프로세스 내에서 한 번만 생성합니다.
@lru_cache
def get_settings() -> Settings:
    return Settings()
