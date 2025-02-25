from sqlalchemy import DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

from app.dao.base import Base


class User(Base):
    __tablename__ = 'users'
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    # связи
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user")

    def to_dict(self):
        return {
            "id": self.id,
            "telegram_id": self.telegram_id,
            "name": self.name,
        }

class Category(Base):
    __tablename__ = 'categories'
    name: Mapped[str] = mapped_column(String, unique=True)
    # связи
    subcategories: Mapped[list["Subcategory"]] = relationship(back_populates="category")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="category")

class Subcategory(Base):
    __tablename__ = 'subcategories'
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    name: Mapped[str] = mapped_column(String, unique=True)
    # связи
    category: Mapped["Category"] = relationship(back_populates="subcategories")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="subcategory")

class Transaction(Base):
    __tablename__ = 'transactions'
    date: Mapped[DateTime] = mapped_column(DateTime)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("subcategories.id"))
    amount: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(String, nullable=True)
    # связи
    user: Mapped["User"] = relationship(back_populates="transactions")
    category: Mapped["Category"] = relationship(back_populates="transactions")
    subcategory: Mapped["Subcategory"] = relationship(back_populates="transactions")