"""
Модуль с моделями SQLAlchemy для работы с базой данных.

Этот модуль содержит определения моделей для таблиц базы данных, таких как пользователи,
категории, подкатегории и транзакции. Модели используются для взаимодействия с базой данных через SQLAlchemy и поддерживают связи между таблицами.

Основные модели:
- `User`: Модель для таблицы пользователей.
- `Category`: Модель для таблицы категорий.
- `Subcategory`: Модель для таблицы подкатегорий.
- `Transaction`: Модель для таблицы транзакций.

Связи между моделями:
- Пользователь (User) может иметь множество транзакций (Transaction).
- Категория (Category) может иметь множество подкатегорий (Subcategory) и транзакций (Transaction).
- Подкатегория (Subcategory) связана с одной категорией и может иметь множество транзакций.
- Транзакция (Transaction) связана с пользователем, категорией и подкатегорией.
"""

from sqlalchemy import DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

from app.dao.base import Base


class User(Base):
    """
    Модель для таблицы пользователей.

    Attributes:
        telegram_id (Mapped[int]): Уникальный идентификатор пользователя в Telegram.
        username (Mapped[str]): Имя пользователя в Telegram (может быть None).
        transactions (Mapped[list["Transaction"]]): Список транзакций, связанных с пользователем.
    """
    __tablename__ = 'users'
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True) 
    username: Mapped[str] = mapped_column(String, nullable=True)
    # Связи
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user")


class Category(Base):
    """
    Модель для таблицы категорий.

    Attributes:
        name (Mapped[str]): Название категории (уникальное).
        subcategories (Mapped[list["Subcategory"]]): Список подкатегорий, связанных с категорией.
        transactions (Mapped[list["Transaction"]]): Список транзакций, связанных с категорией.
    """
    __tablename__ = 'categories'
    name: Mapped[str] = mapped_column(String, unique=True) 
    # Связи
    subcategories: Mapped[list["Subcategory"]] = relationship(back_populates="category")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="category")


class Subcategory(Base):
    """
    Модель для таблицы подкатегорий.

    Attributes:
        category_id (Mapped[int]): Идентификатор категории, к которой относится подкатегория.
        name (Mapped[str]): Название подкатегории.
        category (Mapped["Category"]): Категория, к которой относится подкатегория.
        transactions (Mapped[list["Transaction"]]): Список транзакций, связанных с подкатегорией.
    """
    __tablename__ = 'subcategories'
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id")) 
    name: Mapped[str] = mapped_column(String) 
    category: Mapped["Category"] = relationship(back_populates="subcategories")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="subcategory")


class Transaction(Base):
    """
    Модель для таблицы транзакций.

    Attributes:
        date (Mapped[DateTime]): Дата и время транзакции.
        user_telegram_id (Mapped[int]): Идентификатор пользователя, связанного с транзакцией.
        category_id (Mapped[int]): Идентификатор категории транзакции.
        subcategory_id (Mapped[int]): Идентификатор подкатегории транзакции.
        amount (Mapped[int]): Сумма транзакции.
        comment (Mapped[str]): Комментарий к транзакции (опционально).
        user (Mapped["User"]): Пользователь, связанный с транзакцией.
        category (Mapped["Category"]): Категория, связанная с транзакцией.
        subcategory (Mapped["Subcategory"]): Подкатегория, связанная с транзакцией.
    """
    __tablename__ = 'transactions'
    date: Mapped[DateTime] = mapped_column(DateTime) 
    user_telegram_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id")) 
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("subcategories.id")) 
    amount: Mapped[int] = mapped_column(Integer) 
    comment: Mapped[str] = mapped_column(String, nullable=True)  
    # Связи
    user: Mapped["User"] = relationship(back_populates="transactions")
    category: Mapped["Category"] = relationship(back_populates="transactions")
    subcategory: Mapped["Subcategory"] = relationship(back_populates="transactions")


# Словарь с именами моделей, используется в роутерах API
MODELS = {
    "User": User,
    "Category": Category,
    "Subcategory": Subcategory,
    "Transaction": Transaction,
}