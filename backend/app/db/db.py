# app/db/database.py

import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from ..core.setting import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class Database:
    client: AsyncIOMotorClient = None
    # ✨ 1. 실제 데이터베이스 객체를 저장할 변수 추가
    db_instance: AsyncIOMotorDatabase = None

db = Database()

async def connect_to_mongo():
    logger.info("MongoDB에 연결 중...")
    db.client = AsyncIOMotorClient(settings.MONGO_URI)
    
    # ✨ 2. MONGO_DB_NAME 설정값을 사용하여 특정 데이터베이스에 연결
    #    이렇게 하면 코드 다른 부분에서 DB 이름을 신경 쓸 필요가 없습니다.
    db.db_instance = db.client[settings.MONGO_DB_NAME]
    
    try:
        # PING은 client 객체를 통해 보냅니다.
        await db.client.admin.command('ping')
        logger.info(f"MongoDB '{settings.MONGO_DB_NAME}' 데이터베이스에 성공적으로 연결되었습니다.")
    except Exception as e:
        logger.error(f"MongoDB 연결 실패: {e}")
        db.client = None
        db.db_instance = None

async def close_mongo_connection():
    logger.info("MongoDB 연결을 닫습니다.")
    if db.client:
        db.client.close()

async def get_database() -> AsyncIOMotorDatabase:
    # ✨ 3. 가장 큰 변경점:
    #    lifespan에서 이미 연결을 보장하므로, 복잡한 확인 로직 없이
    #    생성된 데이터베이스 인스턴스를 바로 반환합니다.
    return db.db_instance