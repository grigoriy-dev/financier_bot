from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Доход"), KeyboardButton(text="Расход")],
        [KeyboardButton(text="Отчёт"), KeyboardButton(text="Помощь")]
    ], resize_keyboard=True)
    return keyboard

def get_subcategories_keyboard(subcategories):
    buttons = [[KeyboardButton(text=name)] for name in subcategories]
    buttons.append([KeyboardButton(text="Назад")])
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

def get_report_period_keyboard():
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Месяц"), KeyboardButton(text="3 месяца")],
        [KeyboardButton(text="Полдгода"), KeyboardButton(text="Год")],
        [KeyboardButton(text="Всё время")], [KeyboardButton(text="Назад")]
    ], resize_keyboard=True)
    return keyboard
