from typing import AsyncGenerator
from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.ext.declarative import declared_attr

from app.settings.config import database_url


engine = create_async_engine(url=database_url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    """
    Абстрактный базовый класс для моделей базы данных.
    
    Методы __tablename__: 
    Автоматически генерирует имя таблицы на основе имени класса в нижнем регистре.
    """
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'


class DatabaseSession:
    @staticmethod
    async def get_session(commit: bool = False) -> AsyncGenerator[AsyncSession, None]:
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

    @staticmethod
    async def get_db() -> AsyncGenerator[AsyncSession, None]:
        """Dependency для получения сессии без автоматического коммита"""
        async for session in DatabaseSession.get_session(commit=False):
            yield session

    @staticmethod
    async def get_db_with_commit() -> AsyncGenerator[AsyncSession, None]:
        """Dependency для получения сессии с автоматическим коммитом"""
        async for session in DatabaseSession.get_session(commit=True):
            yield session


# Создаем экземпляр для удобного импорта
db = DatabaseSession()