from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import inspect
from typing import List

from app.dao.base import DatabaseSession as DB, engine
from app.dao.schemas import UserSchema
from app.dao.models import User, Category, Subcategory, Transaction
from app.dao.generic import MainGeneric


router = APIRouter()

MODELS = {
    "User": User,
    "Category": Category,
    "Subcategory": Subcategory,
    "Transaction": Transaction,
}

@router.get("/")
async def home_page():
    print("Welcome to home_page.")
    async with engine.connect() as connection:
        tables = await connection.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
        return {"tables": tables}

# Универсальный роут
@router.get("/{model_name}/get_all")
async def get_model_data(model_name: str):
    model = MODELS.get(model_name)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    try:
        async with DB.get_session(commit=False) as session:
            result = await MainGeneric(model).find_all(session=session)
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{model_name}/add_one")
async def add_one_model_data(model_name: str, user_data: UserSchema):
    model = MODELS.get(model_name)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    try:
        async with DB.get_session(commit=True) as session:
            return await MainGeneric(User).add_one(session=session, values=user_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        