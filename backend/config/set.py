import os
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

load_dotenv()

ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")

if not ASYNC_DATABASE_URL:
    raise RuntimeError("环境变量 ASYNC_DATABASE_URL 没有设置，请检查 .env 文件")

# 创建异步数据库引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=5,
    pool_pre_ping=True,
)

# 创建 session 工厂
async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 依赖注入：每次请求给一个数据库 session
async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()