import asyncio
from fastapi import FastAPI
import uvicorn

from app.api.routers import router as model_router
from app.dao.base import engine, Base
from app.bot.init_bot import dp, bot


# Функция для инициализации схемы базы данных
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Функция для инициализации API
async def init_api():
    app = FastAPI()
    app.include_router(model_router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Инициализация базы данных
    asyncio.run(init_db())
    # Инициализация API
    asyncio.run(init_api())
    # Запуск основной логики
    asyncio.run(main())
