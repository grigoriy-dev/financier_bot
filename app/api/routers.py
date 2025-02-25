from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import inspect
from typing import List, Dict, Type

from app.dao.base import DatabaseSession as DB, engine
from app.dao.schemas import UserSchema
from app.dao.models import User, Category, Subcategory, Transaction
from app.dao.generic import MainGeneric


router = APIRouter()

@router.get("/")
async def home_page():
    print("Welcome to home_page.")
    async with engine.connect() as connection:
        tables = await connection.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
        return {"tables": tables}

MODELS: Dict[str, Type] = {
    "users": User,
    "categories": Category,
    "subcategories": Subcategory,
    "transactions": Transaction,
}

async def get_db_session():
    async with DB.get_session(commit=False) as session:
        yield session

@router.get("/{model_name}")
async def get_model_data(
    model_name: str,
    session: AsyncSession = Depends(get_db_session)
):
    # Получаем модель из словаря
    model = MODELS.get(model_name)
    if not model:
        raise HTTPException(status_code=404, detail="Модель не найдена")

    # Используем MainGeneric для получения данных
    return await MainGeneric(model).find_all(session=session)


@router.post("/users")
async def add_user(user_data: UserSchema):
    async with DB.get_session(commit=True) as session:
        return await MainGeneric(User).add_one(session=session, values=user_data)