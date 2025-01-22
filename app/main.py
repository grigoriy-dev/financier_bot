import asyncio

from app.dao.base import engine, Base


async def main():
    async with engine.begin() as conn:
        # Ваш код здесь
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(main())
