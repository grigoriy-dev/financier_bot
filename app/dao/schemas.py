from pydantic import BaseModel, Field


class PyBaseModel(BaseModel):
    """ Базовая pydantic модель с общими надстройками. """

    class Config:
        from_attributes = True
        protected_namespaces = ()
        validate_assignment = True


class User(PyBaseModel):
    telegram_id: int
    name: str
    
class Category(PyBaseModel):
    name: str

class Subcategory(PyBaseModel):
    category_id: int
    name: str

class Transaction(PyBaseModel):
    date: str
    user_id: int
    category_id: int
    subcategory_id: int
    amount: int
    comment: str
