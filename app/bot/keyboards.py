"""
Модуль для создания клавиатур в Telegram-боте.

Этот модуль содержит функции для генерации Reply-клавиатур, которые используются в боте:
- Главное меню.
- Меню выбора подкатегорий.
- Меню выбора периода для отчетов.

Основные функции:
- `get_main_keyboard`: Создает главное меню с кнопками "Доход", "Расход", "Отчёт" и "Помощь".
- `get_subcategories_keyboard`: Создает клавиатуру для выбора подкатегорий.
- `get_report_period_keyboard`: Создает клавиатуру для выбора периода отчета.

Все клавиатуры автоматически изменяют размер под экран пользователя (resize_keyboard=True).
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    """
    Создает главное меню с кнопками "Доход", "Расход", "Отчёт" и "Помощь".

    Returns:
        ReplyKeyboardMarkup: Главное меню с кнопками.
    """
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Доход"), KeyboardButton(text="Расход")],
        [KeyboardButton(text="Отчёт"), KeyboardButton(text="Помощь")]
    ], resize_keyboard=True)
    return keyboard

def get_subcategories_keyboard(subcategories):
    """
    Создает клавиатуру для выбора подкатегорий.

    Args:
        subcategories (list): Список названий подкатегорий.

    Returns:
        ReplyKeyboardMarkup: Клавиатура с кнопками подкатегорий и кнопкой "Назад".
    """
    buttons = [[KeyboardButton(text=name)] for name in subcategories]
    buttons.append([KeyboardButton(text="Назад")])
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

def get_report_period_keyboard():
    """
    Создает клавиатуру для выбора периода отчета.

    Returns:
        ReplyKeyboardMarkup: Клавиатура с кнопками периодов и кнопкой "Назад".
    """
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Месяц"), KeyboardButton(text="3 месяца")],
        [KeyboardButton(text="Полгода"), KeyboardButton(text="Год")],
        [KeyboardButton(text="Всё время")], [KeyboardButton(text="Назад")]
    ], resize_keyboard=True)
    return keyboard