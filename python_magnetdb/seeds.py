import asyncio

from .db import async_session, perform_migrations

from sqlalchemy import select

from .models.material import Material


async def seeds():
    async with async_session() as session:
        session.add_all([
            Material(name="Hello")
        ])

        print((await session.execute(select(Material))).fetchall()[0])

asyncio.run(perform_migrations())
asyncio.run(seeds())
