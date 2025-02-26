from typing import Type, Generic, List, Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from loguru import logger

from app.dao.schemas import PyBaseModel


class MainGeneric:
    def __init__(self, model: Type):
        self.model = model

    async def find_all(self, session: AsyncSession, filters: Optional[Dict[str, Any]] = None) -> List[Any]:
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
