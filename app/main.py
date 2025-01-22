import asyncio

from app.dao.base import engine, Base
from app.dao.generic import BigGeneric


async def main():
    async with engine.begin() as conn:
        # Ваш код здесь
        await conn.run_sync(Base.metadata.create_all)

    BG = BigGeneric()

asyncio.run(main())
