import asyncio

from app.dao.base import engine, Base
from app.dao.schemas import UserSchema
from app.api.routers import get_model_data


class TestGet:
    @staticmethod
    async def get_model_data():
        # Выводим юзеров с помощью метода модели
        users = await get_model_data("users")
        for user in users: 
            print(user.to_dict())

    @staticmethod
    async def test_get_user_from_pydantic():
        # Выводим юзеров с помощью сериализации через схему Pydantic
        users = await get_users()
        for user in users: 
            print(UserSchema.model_validate(user).model_dump())


class TestPost:
    @staticmethod
    async def test_post():
        user_data = {"telegram_id": 325346463, "name": "Asoka"}
        await add_user(user_data)
