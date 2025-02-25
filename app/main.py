import asyncio

from app.dao.base import engine, Base
from TESTY.testy import TestGet as GETY, TestPost as POTY
from app.api.routers import home_page


# Функция для инициализации схемы базы данных
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    # Тесты
    await home_page()
    await GETY.get_model_data()

    # Основная логика


if __name__ == "__main__":
    # Инициализация базы данных
    asyncio.run(init_db())
    # Запуск основной логики
    asyncio.run(main())
