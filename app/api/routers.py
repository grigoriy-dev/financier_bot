"""
Модуль API для работы с базой данных через FastAPI.

Этот модуль предоставляет эндпоинты для выполнения CRUD-операций
с использованием SQLAlchemy и асинхронного взаимодействия с базой данных.

Основные функции:
- Получение списка всех таблиц в базе данных.
- Получение всех записей для указанной модели с возможностью фильтрации и пагинации.
- Получение одной записи по идентификатору (например, telegram_id).
- Добавление одной или нескольких записей в указанную модель.
- Получение транзакций с объединением данных из связанных таблиц (пользователи, категории, подкатегории).

Структура модуля:
- `handle_model_errors`: Декоратор для обработки ошибок, связанных с моделями.
- `home_page`: Эндпоинт для получения списка таблиц в базе данных.
- `get_many_model_data`: Эндпоинт для получения всех записей модели с фильтрацией и пагинацией.
- `get_many_transactions`: Эндпоинт для получения транзакций с объединением данных из связанных таблиц.
- `get_user`: Эндпоинт для получения одной записи User по telegram_id.
- `add_one_model_data`: Эндпоинт для добавления одной записи в модель.
- `add_many_model_data`: Эндпоинт для добавления нескольких записей в модель.

Примечание:
- Модели должны быть заранее зарегистрированы в `/app/dao/models.py/MODELS`.
- Для работы с транзакциями используется метод `find_transactions`, который объединяет данные из таблиц `Transaction`, `User`, `Category` и `Subcategory`.
- Логирование и обработка ошибок интегрированы в каждый эндпоинт.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import inspect
from functools import wraps
import pandas as pd
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

# Вспомогательная функция для получения данных о транзакциях
async def fetch_transactions(
    period: str = "all",
    filters: Optional[Dict[str, Any]] = None,
    paginate: bool = False,
    page: int = 1,
    page_size: int = 10
) -> Dict[str, Any]:
    """
    Вспомогательная функция для получения данных о транзакциях.

    Args:
        period (str): Период, за который нужно получить данные. По умолчанию "all".
        filters (Optional[Dict[str, Any]]): Фильтры для выборки данных. По умолчанию None.
        paginate (bool): Флаг, указывающий, нужно ли использовать пагинацию. По умолчанию False.
        page (int): Номер страницы для пагинации. По умолчанию 1.
        page_size (int): Количество записей на странице. По умолчанию 20.

    Returns:
        Dict[str, Any]: Результат запроса, содержащий записи и метаданные (если используется пагинация).
    """
    model = MODELS["Transaction"]
    async with DB.get_session(commit=False) as session:
        result = await MainGeneric(model).find_transactions(
            session=session,
            filters=filters,
            paginate=paginate,
            page=page,
            page_size=page_size,
            period=period
        )
    return result


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
async def get_many_model_data(model, filters: Optional[Dict[str, Any]] = None):
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
            )
        return result


@router.get("/{model_name}/get_many")
async def get_many_transactions(
    period: str = "all",
    filters: Optional[Dict[str, Any]] = None,
    paginate: bool = True,
    page: int = 1,
    page_size: int = 10
) -> Dict[str, Any]:
    """
    Получение записей по фильтрам за указанный период с пагинацией по Транзакциям с объединением данных из связанных таблиц.

    Args:
        period (str): Период, за который нужно получить данные. По умолчанию "all".
        filters (Optional[Dict[str, Any]]): Фильтры для выборки данных. По умолчанию None.
        paginate (bool): Флаг, указывающий, нужно ли использовать пагинацию. По умолчанию True.
        page (int): Номер страницы для пагинации. По умолчанию 1.
        page_size (int): Количество записей на странице. По умолчанию 20.

    Returns:
        Dict[str, Any]: Результат запроса, содержащий записи и метаданные (если используется пагинация).
    """
    return await fetch_transactions(period, filters, paginate, page, page_size)


@router.get("/{model_name}/{period}/report")
async def get_report(
    period: str = "all",
    filters: Optional[Dict[str, Any]] = None,
    paginate: bool = False,
    page: int = 1,
    page_size: int = 20,
    format: str = "csv"
) -> Dict[str, str]:
    """
    Формирование отчёта в формате CSV или XLSX на основе данных о транзакциях.
    """
    try:
        report = await fetch_transactions(period, filters, paginate, page, page_size)

        # Создаем DataFrame из полученных данных
        df = pd.DataFrame(report["records"])

        if format == "csv":
            filename = 'data/output.csv'
            df.to_csv(filename, index=False)
            return {"msg": "Данные выгружены в CSV"}
        elif format == "xlsx":
            filename = 'data/output.xlsx'
            df.to_excel(filename, index=False)
            return {"msg": "Данные выгружены в XLSX"}
        else:
            raise HTTPException(
                status_code=400,
                detail="Неподдерживаемый формат выгрузки. Доступные форматы: csv, xlsx"
            )



    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Произошла ошибка при выгрузке данных: {str(e)}"
        )   


@router.get("/user/get_one")
async def get_user(model, tg_id: int):
    """
    Получение одной записи по идентификатору пользователя (tg_id).
    
    Args:
        model: Модель SQLAlchemy.
        tg_id: Идентификатор пользователя в Telegram.
    
    Returns:
        Запись, соответствующая указанному tg_id.
    """
    model = MODELS["User"]
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
