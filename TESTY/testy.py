import asyncio

from app.dao.base import engine, Base
from app.dao.schemas import UserSchema
from app.api.routers import home_page, get_model_data, get_user, add_one_model_data


class GETY:
    @staticmethod
    async def test_get_tables():
        print(await home_page())

    @staticmethod
    async def test_get_model_data():
        model_name = "User"
        users = await get_model_data(model_name)
        for user in users: 
            print(user.to_dict())

    @staticmethod
    async def test_get_user():
        model_name = "User"
        tg_id = 65942554
        user = await get_user(model_name, tg_id)
        if user:
            print(user.to_dict())


class POTY:
    @staticmethod
    async def test_add_one_model_data():
        model_name = "User"
        user_data = {"telegram_id": 84779623, "username": "BobaFett"}
        await add_one_model_data(model_name=model_name, user_data=user_data)
