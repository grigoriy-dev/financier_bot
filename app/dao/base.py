from typing import AsyncGenerator
from sqlalchemy import Integer, inspect
from contextlib import asynccontextmanager
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.ext.declarative import declared_attr

from app.settings.config import database_url


engine = create_async_engine(url=database_url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    """
    Абстрактный базовый класс для моделей базы данных.
    """
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    def to_dict(self):
        """
        Преобразует объект модели в словарь.

        Returns:
            dict: Словарь, где ключи — это названия колонок, а значения — данные из модели.
        """
        # Используем inspect для получения информации о колонках модели
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        

class DatabaseSession:
    @staticmethod
    @asynccontextmanager
    async def get_session(commit: bool = False) -> AsyncSession:
        async with async_session_maker() as session:
            try:
                yield session
                if commit:
                    await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
