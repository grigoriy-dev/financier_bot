from datetime import datetime
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from loguru import logger

from app.bot.keyboards import get_main_keyboard, get_subcategories_keyboard
from app.api.routers import get_many_model_data, add_one_model_data
from app.bot.states import Form

# Создаем роутер для хэндлеров
router = Router()

# Приветственное сообщение
@router.message(Command("start"))
async def start(message: types.Message):
    keyboard = get_main_keyboard()
    logger.info(f"Клавиатура: {keyboard}")
    await message.answer(
        "Добро пожаловать! Я ваш финансовый помощник.\n"
        "Выберите действие:",
        reply_markup=keyboard
    )

# Обработка кнопок "Доход" и "Расход"
@router.message(lambda message: message.text in ["Доход", "Расход"])
async def process_category(message: types.Message, state: FSMContext):
    category = message.text
    await state.update_data(category=category)  # Сохраняем категорию

    categories = {"Доход": 1, "Расход": 2}
    category_id = categories.get(category)

    # Получаем подкатегории
    subcategories = await get_many_model_data(
        model_name="Subcategory",
        filters={"category_id": category_id}
    )
    subcategories = [{"id": sc.id, "name": sc.name} for sc in subcategories["records"]]
    logger.info(f"Подкатегории: {subcategories}")

    # Сохраняем подкатегории в состояние
    await state.update_data(subcategories=subcategories)

    # Создаем клавиатуру с подкатегориями
    subcategory_names = [subcat["name"] for subcat in subcategories]
    await message.answer(
        "Выберите подкатегорию:",
        reply_markup=get_subcategories_keyboard(subcategory_names)
    )

    await state.set_state(Form.subcategory)  # Переходим в состояние выбора подкатегории

# Обработка выбора подкатегории
@router.message(Form.subcategory)
async def process_subcategory(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.clear()
        await message.answer(
            "Выберите действие:",
            reply_markup=get_main_keyboard()
        )
        return

    subcategory_name = message.text
    data = await state.get_data()
    subcategories = data.get("subcategories")

    # Находим выбранную подкатегорию
    selected_subcategory = next((sc for sc in subcategories if sc["name"] == subcategory_name), None)
    if not selected_subcategory:
        logger.info(f"Подкатегория {subcategories} не найдена.")
        await message.answer("Подкатегория не найдена.")
        return

    # Сохраняем subcategory_id в состояние
    await state.update_data(subcategory_id=selected_subcategory["id"])

    await message.answer("Введите сумму:")
    await state.set_state(Form.amount)  # Переходим в состояние ввода суммы

# Обработка ввода суммы
@router.message(Form.amount)
async def process_amount(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.set_state(Form.subcategory)
        data = await state.get_data()
        subcategories = data.get("subcategories")
        subcategory_names = [sc["name"] for sc in subcategories]
        await message.answer(
            "Выберите подкатегорию:",
            reply_markup=get_subcategories_keyboard(subcategory_names)
        )
        return

    try:
        amount = float(message.text)
        data = await state.get_data()

        # Формируем данные для транзакции
        transaction_data = {
            "date": datetime.now(),
            "user_telegram_id": message.from_user.id,
            "category_id": 1 if data["category"] == "Доход" else 2,
            "subcategory_id": data["subcategory_id"],
            "amount": amount,
            "comment": "" 
        }

        # Сохраняем данные в БД
        await add_one_model_data(model_name="Transaction", values=transaction_data)

        await message.answer("Данные успешно сохранены!")
        await state.clear()

        # Возврат в главное меню
        await message.answer(
            "Выберите действие:",
            reply_markup=get_main_keyboard()
        )

    except ValueError:
        await message.answer("Пожалуйста, введите корректную сумму.")
