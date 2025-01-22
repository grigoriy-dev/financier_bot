from sqlalchemy import DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.base import Base


class User(Base):
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=True)

class Category(Base):
    name: Mapped[str] = mapped_column(String, unique=True)
    # связь с подкатегориями
    subcategory: Mapped["Subcategory"] = relationship(back_populates="categorys")
    # связь с транзакциями
    transaction: Mapped["Transaction"] = relationship(back_populates="categorys")

class Subcategory(Base):
    category_id: Mapped[int] = mapped_column(ForeignKey("categorys.id"))
    name: Mapped[str] = mapped_column(String, unique=True)
    # связь с категориями
    category: Mapped["Category"] = relationship(back_populates="subcategorys")
    # связь с транзакциями
    transaction: Mapped["Transaction"] = relationship(back_populates="subcategorys")

class Transaction(Base):
    date: Mapped[DateTime] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categorys.id"))
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("subcategorys.id"))
    amount: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(String, nullable=True)
    # связь с пользователем
    user: Mapped["User"] = relationship(back_populates="transactions")
    # связь с категориями
    category: Mapped["Category"] = relationship(back_populates="transactions")
    # связь с подкатегориями
    subcategory: Mapped["Subcategory"] = relationship(back_populates="transactions")
