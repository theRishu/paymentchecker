from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=1800)
async_session = async_sessionmaker(engine, expire_on_commit=False)
