from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from os import getenv

from .models.application_model import ApplicationModel

engine = create_async_engine(getenv("DATABASE_URL"), echo=True)
async_session = sessionmaker(expire_on_commit=False, class_=AsyncSession, bind=engine)


async def perform_migrations():
    async with engine.begin() as conn:
        await conn.run_sync(ApplicationModel.metadata.create_all)
