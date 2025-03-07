from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    category = State()
    subcategory = State()
    amount = State()
