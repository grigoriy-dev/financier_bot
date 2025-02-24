from typing import Type, TypeVar, Generic, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from loguru import logger

from app.dao.schemas import PyBaseModel

T = TypeVar('T', bound=PyBaseModel)
M = TypeVar('M')

class MainGeneric:
    def __init__(self, model: Type):
        self.model = model

    async def find_all(self, session: AsyncSession) -> List[Any]:
        logger.info(f"Поиск записей {self.model}:")
        try:
            result = await session.execute(select(self.model))
            records = result.scalars().all()
            logger.info(f"Найдено {len(records)} записей.")
            return records
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске всех записей: {e}")
            raise

    async def add_one(self, session: AsyncSession, values):
        pass
