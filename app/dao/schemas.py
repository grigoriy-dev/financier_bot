from pydantic import BaseModel, Field


class PyBaseModel(BaseModel):
    """ Базовая pydantic модель с общими надстройками. """

    class Config:
        from_attributes = True
        protected_namespaces = ()
        validate_assignment = True


class User(PyBaseModel):
    telegram_id: int = Field(unique_items=True)
    name: str = Field(nullable=True)
    
class Category(PyBaseModel):
    name: str = Field(unique_items=True)

class Subcategory(PyBaseModel):
    category_id: 
    name: 

class Transaction(PyBaseModel):
    date: 
    user_id: 
    category_id: 
    subcategory_id: 
    amount: 
