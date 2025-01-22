from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.base import Base


class User(Base):
    id_user: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)

class Category(Base):
    name: Mapped[str] = mapped_column(String)
    # связь с подкатегориями
    subcategory: Mapped["Subcategory"] = relationship(back_populates="categorys")

class Subcategory(Base):
    category_id: Mapped[int] = mapped_column(ForeignKey("categorys.id"))
    name: Mapped[str] = mapped_column(String)
    # связь с категориями
    category: Mapped["Category"] = relationship(back_populates="subcategorys")