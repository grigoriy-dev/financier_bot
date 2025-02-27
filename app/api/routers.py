"""
Модуль API для работы с базой данных через FastAPI.

Этот модуль предоставляет эндпоинты для выполнения CRUD-операций
с использованием SQLAlchemy и асинхронного взаимодействия с базой данных.

Основные функции:
- Получение списка всех таблиц в базе данных.
- Получение всех записей для указанной модели с возможностью фильтрации.
- Получение одной записи по идентификатору.
- Добавление одной или нескольких записей в указанную модель.

Структура модуля:
- `handle_model_errors`: Декоратор для обработки ошибок, связанных с моделями.
- `home_page`: Эндпоинт для получения списка таблиц в базе данных.
- `get_model_data`: Эндпоинт для получения всех записей модели с фильтрацией.
- `get_user`: Эндпоинт для получения одной записи User по telegram id.
- `add_one_model_data`: Эндпоинт для добавления одной записи в модель.
- `add_many_model_data`: Эндпоинт для добавления нескольких записей в модель.

Примечание:
- Модели должны быть заранее зарегистрированы в `/app/dao/models.py/MODELS`.
"""

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

# Создание роутера для API
router = APIRouter()

# Декоратор для обработки ошибок, связанных с моделями
def handle_model_errors(func):
    """
    Декоратор для обработки ошибок, связанных с моделями.
    Проверяет, существует ли модель, и обрабатывает исключения.
    """
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
    """
    Домашняя страница API.
    Возвращает список всех таблиц в базе данных.
    """
    print("Welcome to home_page.")
    async with engine.connect() as connection:
        tables = await connection.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
        return {"tables": tables}


@router.get("/{model_name}/get_many")
@handle_model_errors
async def get_many_model_data(
        model, 
        filters: Optional[Dict[str, Any]] = None,
        page: int = 1,
        page_size = None
        ):
    """
    Получение записей по фильтрам с пагинацией для указанной модели.
    
    Args:
        model: Модель SQLAlchemy.
        filters: Словарь фильтров для поиска записей (опционально).
    
    Returns:
        Список записей, соответствующих фильтрам.
    """
    async with DB.get_session(commit=False) as session:
        result = await MainGeneric(model).find_many(
            session=session, 
            filters=filters,
            page=page,
            page_size=page_size
            )
        return result


@router.get("/{model_name}/get_one")
@handle_model_errors
async def get_user(model, tg_id: int):
    """
    Получение одной записи по идентификатору пользователя (tg_id).
    
    Args:
        model: Модель SQLAlchemy.
        tg_id: Идентификатор пользователя в Telegram.
    
    Returns:
        Запись, соответствующая указанному tg_id.
    """
    async with DB.get_session(commit=False) as session:
        result = await MainGeneric(model).find_user(session=session, tg_id=tg_id)
        return result


@router.post("/{model_name}/add_one")
@handle_model_errors
async def add_one_model_data(model, values):
    """
    Добавление одной записи в указанную модель.
    
    Args:
        model: Модель SQLAlchemy.
        values: Данные для добавления (словарь или объект Pydantic).
    
    Returns:
        Добавленная запись.
    """
    async with DB.get_session(commit=True) as session:
        return await MainGeneric(model).add_one(session=session, values=values)


@router.post("/{model_name}/add_many")
@handle_model_errors
async def add_many_model_data(model, values):
    """
    Добавление нескольких записей в указанную модель.

    Args:
        model: Модель SQLAlchemy.
        values: Список данных для добавления (список словарей или объектов Pydantic).
    
    Returns:
        Список добавленных записей.
    """
    async with DB.get_session(commit=True) as session:
        return await MainGeneric(model).add_many(session=session, values=values)
