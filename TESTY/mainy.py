import asyncio

from app.dao.base import engine, Base
from TESTY.testy import GETY, POTY


# Функция для инициализации схемы базы данных
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    print("=== Получаем список таблиц:")
    await GETY.test_get_tables()
    print("=== Получаем все записи из выбранной таблицы:")
    await GETY.test_get_model_data()
    print("=== Получаем записи по фильтрам:")
    await GETY.test_get_model_data_filters()
    print("=== Получаем пользователя по telegram_id:")
    await GETY.test_get_user()

    print("=== Добавляем одного пользователя:")
    #await POTY.test_add_one_user()
    print("=== Добавляем несколько пользователей:")
    #await POTY.test_add_many_user()
    print("=== Добавляем несколько категорий")
    #await POTY.test_add_many_categories()
    print("=== Добавляем несколько подкатегорий")
    #await POTY.test_add_many_subcategories()
    print("=== ")

if __name__ == "__main__":
    # Инициализация базы данных
    asyncio.run(init_db())
    # Запуск основной логики
    asyncio.run(main())
