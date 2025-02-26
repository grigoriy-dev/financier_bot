from pydantic import BaseModel, Field


class PyBaseModel(BaseModel):
    """ Базовая pydantic модель с общими надстройками. """

    class Config:
        from_attributes = True
        protected_namespaces = ()
        validate_assignment = True


class UserSchema(PyBaseModel):
    telegram_id: int
    username: str
    
class CategorySchema(PyBaseModel):
    name: str

class SubcategorySchema(PyBaseModel):
    category_id: int
    name: str

class TransactionSchema(PyBaseModel):
    date: str
    user_id: int
    category_id: int
    subcategory_id: int
    amount: int
    comment: str
