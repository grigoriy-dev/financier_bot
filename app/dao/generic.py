"""
Модуль для работы с базой данных через универсальный класс MainGeneric.

Этот модуль предоставляет класс `MainGeneric`, который реализует базовые CRUD-операции
для моделей SQLAlchemy с использованием асинхронных сессий.

Основные возможности:
- Поиск всех записей модели с возможностью фильтрации.
- Поиск одной записи по уникальному идентификатору (например, telegram_id).
- Добавление одной или нескольких записей в модель.
- Обработка ошибок и логирование операций (Loguru).

Классы:
- `MainGeneric`: Универсальный класс для работы с моделями SQLAlchemy.

Примечания:
- Модели должны быть заранее определены и использовать SQLAlchemy.
- Логирование выполняется с использованием библиотеки Loguru.
"""

from typing import Type, Generic, List, Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from loguru import logger

from app.dao.schemas import PyBaseModel


class MainGeneric:
    """
    Универсальный класс для выполнения базовых CRUD операций с моделями SQLAlchemy
    с использованием асинхронных сессий SQLAlchemy.

    Attributes:
        model (Type): Модель SQLAlchemy, с которой работает класс.
    """
    def __init__(self, model: Type):
        self.model = model

    async def find_all(self, session: AsyncSession, filters: Optional[Dict[str, Any]] = None) -> List[Any]:
        """
        Поиск всех записей модели с возможностью фильтрации.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            filters (Optional[Dict[str, Any]]): Словарь фильтров или объект PyBaseModel.

        Returns:
            List[Any]: Список найденных записей.

        Raises:
            SQLAlchemyError: Если произошла ошибка при выполнении запроса.
        """
        logger.info(f"Поиск записей {self.model.__name__} по фильтрам: {filters}:")
        if filters is not None and isinstance(filters, PyBaseModel):
            filter_dict = filters.dict() 
        else:
            filter_dict = filters if filters is not None else {}
        try:
            query = select(self.model).filter_by(**filter_dict)
            result = await session.execute(query)
            records = result.scalars().all()
            logger.info(f"Найдено {len(records)} записей.")
            return records
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске всех записей: {e}.")
            raise

    async def find_user(self, session: AsyncSession, tg_id: int):
        """
        Поиск записи по идентификатору пользователя (telegram_id).

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            tg_id (int): Идентификатор пользователя в Telegram.

        Returns:
            Any: Найденная запись или None, если запись не найдена.

        Raises:
            SQLAlchemyError: Если произошла ошибка при выполнении запроса.
        """
        logger.info(f"Поиск {self.model.__name__} по telegram_id={tg_id}:")
        try:
            query = select(self.model).where(self.model.telegram_id==tg_id)
            result = await session.execute(query)
            user = result.scalars().first()
            if user:
                logger.info(f"Пользователь найден: {user.to_dict()}.")
            else:
                logger.info(f"Пользователь с telegram_id={tg_id} не найден.")
            return user
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записи: {e}.")
            raise

    async def add_one(self, session: AsyncSession, values: Dict[str, Any]):
        """
        Добавление одной записи в модель.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            values (Dict[str, Any]): Данные для добавления (словарь или объект PyBaseModel).

        Returns:
            Any: Добавленная запись.

        Raises:
            SQLAlchemyError: Если произошла ошибка при добавлении записи.
        """
        logger.info(f"Добавление записи в {self.model.__name__}:")
        try:
            new_record = self.model(**values.dict() if isinstance(values, PyBaseModel) else values)
            session.add(new_record)
            await session.flush()
            await session.refresh(new_record)

            logger.info(f"Запись успешно добавлена: {new_record.to_dict()}.")
            return new_record
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при добавлении записи: {e}.")
            await session.rollback()
            raise

    async def add_many(self, session: AsyncSession, values: List[Dict[str, Any]]):
        """
        Добавление нескольких записей в модель.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            values (List[Dict[str, Any]]): Список данных для добавления.

        Returns:
            List[Any]: Список добавленных записей.

        Raises:
            SQLAlchemyError: Если произошла ошибка при добавлении записей.
        """
        logger.info(f"Добавление нескольких записей в {self.model.__name__}:")
        try:
            new_records = [
                self.model(**value.dict() if isinstance(value, PyBaseModel) else value)
                for value in values
            ]
            session.add_all(new_records)
            await session.flush()
            for record in new_records:
                await session.refresh(record)

            logger.info(f"Успешно добавлено {len(new_records)} записей.")
            return new_records
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при добавлении записей: {e}.")
            await session.rollback()
            raise
