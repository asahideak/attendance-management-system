"""
勤怠管理システム - データベース接続管理
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# 非同期エンジン作成
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True
)

# 非同期セッション作成
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# ベースクラス
Base = declarative_base()


# データベースセッション依存性
async def get_db() -> AsyncSession:
    """データベースセッション取得"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()