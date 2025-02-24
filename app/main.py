import asyncio

from app.dao.base import engine, Base
from app.api.routers import home_page, get_users, add_user


# Функция для инициализации схемы базы данных
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    print(await home_page())
    await get_users()
    await add_user()


if __name__ == "__main__":
    # Инициализация базы данных
    asyncio.run(init_db())

    # Запуск основной логики
    asyncio.run(main())
