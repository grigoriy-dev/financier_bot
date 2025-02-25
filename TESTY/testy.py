import asyncio

from app.dao.base import engine, Base
from app.dao.schemas import UserSchema
from app.api.routers import home_page, get_model_data


class GETY:
    @staticmethod
    async def test_get_tables():
        # показываем таблицы
        print(await home_page())

    @staticmethod
    async def test_get_model_data():
        users = await get_model_data("User")
        for user in users: 
            print(user.to_dict())


class POTY:
    @staticmethod
    async def test_post():
        user_data = {"telegram_id": 325346463, "name": "Asoka"}
        await add_user(user_data)
