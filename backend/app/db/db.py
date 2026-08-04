import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from ..core.setting import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class Database:
    client: AsyncIOMotorClient = None
    db_instance: AsyncIOMotorDatabase = None

db = Database()

async def connect_to_mongo():
    logger.info("MongoDB에 연결 중...")
    db.client = AsyncIOMotorClient(settings.MONGO_URI)
    
    db.db_instance = db.client[settings.MONGO_DB_NAME]
    
    try:
        # 데이터베이스 선택과 별개로 서버 연결 상태를 확인합니다.
        await db.client.admin.command('ping')
        logger.info(f"MongoDB '{settings.MONGO_DB_NAME}' 데이터베이스에 성공적으로 연결되었습니다.")
    except Exception as e:
        logger.critical("MongoDB 연결 실패 — 앱을 시작할 수 없습니다: %s", e)
        db.client = None
        db.db_instance = None
        raise  # 앱 시작 단계에서 연결 실패를 알립니다.

async def close_mongo_connection():
    logger.info("MongoDB 연결을 닫습니다.")
    if db.client:
        db.client.close()

async def get_database() -> AsyncIOMotorDatabase:
    # lifespan에서 연결을 확인하므로 요청마다 새 연결을 만들지 않습니다.
    return db.db_instance
