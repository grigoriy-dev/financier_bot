from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import inspect
from functools import wraps
from typing import List, Optional, Dict, Any

from app.dao.base import DatabaseSession as DB, engine
from app.dao.schemas import UserSchema
from app.dao.models import MODELS
from app.dao.generic import MainGeneric


router = APIRouter()

# Декаротор для исключений
def handle_model_errors(func):
    @wraps(func)
    async def wrapper(model_name: str, *args, **kwargs):
        model = MODELS.get(model_name)
        if not model:
            raise HTTPException(status_code=404, detail="Model not found")
        try:
            return await func(model, *args, **kwargs)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return wrapper


@router.get("/")
async def home_page():
    print("Welcome to home_page.")
    async with engine.connect() as connection:
        tables = await connection.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
        return {"tables": tables}


@router.get("/{model_name}/get_all")
@handle_model_errors
async def get_model_data(model, filters: Optional[Dict[str, Any]] = None):
    async with DB.get_session(commit=False) as session:
        result = await MainGeneric(model).find_all(session=session, filters=filters)
        return result


@router.get("/{model_name}/get_one")
@handle_model_errors
async def get_user(model, tg_id: int):
    async with DB.get_session(commit=False) as session:
        result = await MainGeneric(model).find_user(session=session, tg_id=tg_id)
        return result


@router.post("/{model_name}/add_one")
@handle_model_errors
async def add_one_model_data(model, values):
    async with DB.get_session(commit=True) as session:
        return await MainGeneric(model).add_one(session=session, values=values)


@router.post("/{model_name}/add_many")
@handle_model_errors
async def add_many_model_data(model, values):
    async with DB.get_session(commit=True) as session:
        return await MainGeneric(model).add_many(session=session, values=values)
        