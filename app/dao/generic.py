from typing import Type, TypeVar, Generic, List, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from loguru import logger

from app.dao.schemas import PyBaseModel



class MainGeneric:
    def __init__(self, model: Type):
        self.model = model

    async def find_all(self, session: AsyncSession) -> List[Any]:
        logger.info(f"Поиск записей {self.model.__name__}:")
        try:
            result = await session.execute(select(self.model))
            records = result.scalars().all()
            logger.info(f"Найдено {len(records)} записей.")
            return records
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске всех записей: {e}")
            raise

    async def add_one(self, session: AsyncSession, values: Dict[str, Any]):
        logger.info(f"Добавление записи в {self.model.__name__}:")
        try:
            # Создаем экземпляр модели на основе переданных данных
            new_record = self.model(**values.dict() if isinstance(values, PyBaseModel) else values)
            session.add(new_record)
            await session.flush()  # Фиксируем изменения в базе данных
            await session.refresh(new_record)  # Обновляем объект, чтобы получить данные из БД (например, ID)
            logger.info(f"Запись успешно добавлена: {new_record}")
            return new_record
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при добавлении записи: {e}")
            await session.rollback()
            raise
