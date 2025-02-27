"""
Модуль для работы с базой данных через универсальный класс MainGeneric.

Этот модуль предоставляет класс `MainGeneric`, который реализует базовые CRUD-операции
для моделей SQLAlchemy с использованием асинхронных сессий.

Основные возможности:
- Поиск всех записей модели с возможностью пагинации и фильтрации.
- Поиск одной записи по уникальному идентификатору (например, telegram_id).
- Добавление одной или нескольких записей в модель.
- Поиск транзакций с объединением данных из связанных таблиц (пользователи, категории, подкатегории).
- Обработка ошибок и логирование операций (Loguru).

Классы:
- `MainGeneric`: Универсальный класс для работы с моделями SQLAlchemy.

Примечания:
- Модели должны быть заранее определены и использовать SQLAlchemy.
- Логирование выполняется с использованием библиотеки Loguru.
- Метод `find_transactions` предназначен для работы с моделью `Transaction` и объединяет данные из связанных таблиц.
"""

from typing import Type, Generic, List, Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import select, func
from loguru import logger

from app.dao.schemas import PyBaseModel
from app.dao.models import User, Transaction, Category, Subcategory


class MainGeneric:
    """
    Универсальный класс для выполнения базовых CRUD операций с моделями SQLAlchemy
    с использованием асинхронных сессий SQLAlchemy.

    Attributes:
        model (Type): Модель SQLAlchemy, с которой работает класс.
    """
    def __init__(self, model: Type):
        self.model = model

    async def find_many(
            self, session: AsyncSession, 
            filters: Optional[Dict[str, Any]] = None,
            page: int = 1,
            page_size: int = 10
            ) -> List[Any]:
        """
        Возвращает список записей с пагинацией на основе заданных фильтров.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов.
            filters (Optional[Dict[str, Any]]): Словарь / объект Pydantic / None. 
            page (int): Номер страницы для пагинации. Начинается с 1. По умолчанию 1.
            page_size (int): Количество записей на одной странице. По умолчанию 10.

        Returns:
            Dict[str, Any]: Словарь, содержащий:
                - "records": Список записей для текущей страницы.
                - "total_records": Общее количество записей, удовлетворяющих фильтрам.
                - "total_pages": Общее количество страниц.

        Raises:
            SQLAlchemyError: Если произошла ошибка при выполнении запроса к базе данных.
        """
        logger.info(f"Поиск записей {self.model.__name__} по фильтрам: {filters}:")
        if filters is not None and isinstance(filters, PyBaseModel):
            filter_dict = filters.dict() 
        else:
            filter_dict = filters if filters is not None else {}
        try:
            # Запрос для подсчета общего количества записей
            count_query = select(func.count()).select_from(self.model).filter_by(**filter_dict)
            total_records = (await session.execute(count_query)).scalar()

            # Вычисляем offset
            offset = (page - 1) * page_size

            # Запрос для получения записей с пагинацией
            records_query = (
                select(self.model)
                .filter_by(**filter_dict)
                .order_by(self.model.id.asc())
                .limit(page_size)
                .offset(offset)
            )
            records_result = await session.execute(records_query)
            records = records_result.scalars().all()

            # Возвращаем записи и общее количество
            return {
                "page": page,
                "records": records,
                "total_records": total_records,
                "total_pages": (total_records + page_size - 1) // page_size
            }
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске всех записей: {e}.")
            raise

    async def find_transactions(
                self, session: AsyncSession,
        filters: Optional[Dict[str, Any]] = None,
        page: int = 1,
        page_size: int = 20
        ) -> List[Dict[str, Any]]:
        """
        Возвращает список записей с объединением данных из связанных таблиц.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            filters (Optional[Dict[str, Any]]): Фильтры для поиска.
            page (int): Номер страницы.
            page_size (int): Количество записей на странице.

        Returns:
            Dict[str, Any]: Словарь, содержащий:
                - "records": Список записей с объединенными данными.
                - "total_records": Общее количество записей, удовлетворяющих фильтрам.
                - "total_pages": Общее количество страниц.
        """
        if filters is not None and isinstance(filters, PyBaseModel):
            filter_dict = filters.dict()
        else:
            filter_dict = filters if filters is not None else {}

        try:
            # Подсчет общего количества записей
            count_query = (
                select(func.count())
                .select_from(Transaction)
                .join(User, Transaction.user_telegram_id == User.telegram_id)
                .join(Category, Transaction.category_id == Category.id)
                .join(Subcategory, Transaction.subcategory_id == Subcategory.id)
            )
            
            # Применяем фильтры к запросу подсчета
            for key, value in filter_dict.items():
                if hasattr(Transaction, key):
                    count_query = count_query.filter(getattr(Transaction, key) == value)
                elif hasattr(User, key):
                    count_query = count_query.filter(getattr(User, key) == value)
                elif hasattr(Category, key):
                    count_query = count_query.filter(getattr(Category, key) == value)
                elif hasattr(Subcategory, key):
                    count_query = count_query.filter(getattr(Subcategory, key) == value)

            total_records = (await session.execute(count_query)).scalar()

            # Создаем JOIN-запрос для получения данных
            query = (
                select(
                    Transaction.id,
                    Transaction.date,
                    User.username.label("user_name"),
                    Category.name.label("category_name"),
                    Subcategory.name.label("subcategory_name"),
                    Transaction.amount,
                    Transaction.comment
                )
                .join(User, Transaction.user_telegram_id == User.telegram_id)
                .join(Category, Transaction.category_id == Category.id)
                .join(Subcategory, Transaction.subcategory_id == Subcategory.id)
                .order_by(Transaction.date.asc())
                .limit(page_size)
                .offset((page - 1) * page_size)
            )

            # Применяем фильтры к основному запросу
            for key, value in filter_dict.items():
                if hasattr(Transaction, key):
                    query = query.filter(getattr(Transaction, key) == value)
                elif hasattr(User, key):
                    query = query.filter(getattr(User, key) == value)
                elif hasattr(Category, key):
                    query = query.filter(getattr(Category, key) == value)
                elif hasattr(Subcategory, key):
                    query = query.filter(getattr(Subcategory, key) == value)

            # Выполняем запрос
            result = await session.execute(query)
            records = result.mappings().all()

            # Форматируем дату и возвращаем результат
            formatted_records = []
            for record in records:
                formatted_record = dict(record)
                formatted_record["date"] = formatted_record["date"].strftime("%Y-%m-%d %H:%M:%S")  # Форматируем дату
                formatted_records.append(formatted_record)

            return {
                "page": page,
                "records": formatted_records,
                "total_records": total_records,
                "total_pages": (total_records + page_size - 1) // page_size
            }
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записей с объединением: {e}")
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
