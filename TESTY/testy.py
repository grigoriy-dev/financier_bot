import asyncio

from app.dao.base import engine, Base
from app.dao.schemas import UserSchema
from app.api.routers import home_page, get_user, add_one_model_data, add_many_model_data, get_many_model_data, get_many_transactions
from app.api.reports import get_report
from TESTY.data_generator import generate_data


class GETY:
    @staticmethod
    async def test_get_tables():
        print(await home_page())

    @staticmethod
    async def test_get_many_model_data():
        model_name = "User"
        filters = {}
        records = await get_many_model_data(model_name, filters, page=1)
        print(f"Страница {records['page']} / {records['total_pages']}:")
        for record in records["records"]:
            print(record.to_dict())
        print("Всего записей:", records["total_records"])


    @staticmethod
    async def test_get_many_transactions():
        filters = {}
        records = await get_many_transactions(filters)
        print(f"Страница {records['page']} / {records['total_pages']}:")
        for record in records["records"]:
            print(record)
        print("Всего записей:", records["total_records"])
    

    @staticmethod
    async def test_get_report():
        period = "month"
        filters = {}
        records = await get_report(period, filters)
        print(f"Страница {records['page']} / {records['total_pages']}:")
        for record in records["records"]:
            print(record)
        print("Всего записей:", records["total_records"])


    @staticmethod
    async def test_get_user():
        model_name = "User"
        tg_id = 12345678
        user = await get_user(model_name, tg_id)
        if user:
            print(user.to_dict())


class POTY:
    @staticmethod
    async def test_add_one_user():
        model_name = "User"
        values = {"telegram_id": 84779623, "username": "BobaFett"}
        await add_one_model_data(model_name=model_name, values=values)

    @staticmethod
    async def test_add_many_user():
        model_name = "User"
        values = [
            {"telegram_id": 12345678, "username": "LandoCalrissian"},
            {"telegram_id": 87654321, "username": "ObiWanKenobi"},
            {"telegram_id": 98765432, "username": "HanSolo"},
            {"telegram_id": 56781234, "username": "PrincessLeia"},
            {"telegram_id": 43218765, "username": "MaceWindu"},
            {"telegram_id": 67358500, "username": "SkyWalker"}
]
        await add_many_model_data(model_name=model_name, values=values)

    @staticmethod
    async def test_add_many_categories():
        model_name = "Category"
        values = [
            {"name": "Доход"},
            {"name": "Расход"}
]
        await add_many_model_data(model_name=model_name, values=values)

    @staticmethod
    async def test_add_many_subcategories():
        model_name = "Subcategory"
        values = [
            {"category_id": 1, "name": "Зарплата"},
            {"category_id": 1, "name": "Инвестиции"},
            {"category_id": 1, "name": "Фриланс"},
            {"category_id": 1, "name": "Подарки"},
            {"category_id": 1, "name": "Другое"},
            {"category_id": 2, "name": "Еда"},
            {"category_id": 2, "name": "Транспорт"},
            {"category_id": 2, "name": "Жилье"},
            {"category_id": 2, "name": "Одежда"},
            {"category_id": 2, "name": "Здоровье"},
            {"category_id": 2, "name": "Развлечения"},
            {"category_id": 2, "name": "Подарки"},
            {"category_id": 2, "name": "Связь"},
            {"category_id": 2, "name": "Путешествия"},
            {"category_id": 2, "name": "Долги"},
            {"category_id": 2, "name": "Другое"}
]
        await add_many_model_data(model_name=model_name, values=values)

    @staticmethod
    async def test_add_many_transactions():
        model_name = "Transaction"
        values = generate_data()
        await add_many_model_data(model_name=model_name, values=values)
