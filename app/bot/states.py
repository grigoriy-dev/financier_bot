"""
Модуль для определения состояний (States) в Telegram-боте.

"""

from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    """
    Класс для определения состояний (States) в Telegram-боте.

    Атрибуты:
        category (State): Состояние выбора категории (Доход/Расход).
        subcategory (State): Состояние выбора подкатегории.
        amount (State): Состояние ввода суммы транзакции.
    """
    category = State()
    subcategory = State()
    amount = State()