import asyncio

from app.dao.base import engine, Base
from TESTY.testy import GETY, POTY


# Функция для инициализации схемы базы данных
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    # Получаем список таблиц
    await GETY.test_get_tables()
    # Получаем все строки из выбранной таблицы
    await GETY.test_get_model_data()
    # Получаем пользователя по telegram_id
    await GETY.test_get_user()

    # Добавляем нового пользователя
    #await POTY.test_add_one_model_data()


if __name__ == "__main__":
    # Инициализация базы данных
    asyncio.run(init_db())
    # Запуск основной логики
    asyncio.run(main())
