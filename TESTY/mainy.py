import asyncio

from app.dao.base import engine, Base
from TESTY.testy import GETY, POTY


# Функция для инициализации схемы базы данных
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    """Тесты GET запросов"""
    print("=== Получаем список таблиц:")
    await GETY.test_get_tables()
    print("=== Получаем записи по фильтрам с пагинацией:")
    await GETY.test_get_many_model_data()
    print("=== Получаем пользователя по telegram_id:")
    #await GETY.test_get_user()

    """Тесты POST запросов"""
    print("=== Добавляем одного пользователя:")
    #await POTY.test_add_one_user()
    print("=== Добавляем несколько пользователей:")
    #await POTY.test_add_many_user()
    print("=== Добавляем несколько категорий:")
    #await POTY.test_add_many_categories()
    print("=== Добавляем несколько подкатегорий:")
    #await POTY.test_add_many_subcategories()
    print("=== Добавляем несколько (50) рандомных транзакций:")
    #await POTY.test_add_many_transactions()
    print("=== ")

if __name__ == "__main__":
    # Инициализация базы данных
    asyncio.run(init_db())
    # Запуск основной логики
    asyncio.run(main())
