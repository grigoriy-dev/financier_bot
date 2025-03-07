"""
Модуль для обработки транзакций в Telegram-боте.

Этот модуль содержит хэндлеры для управления финансовыми транзакциями:
- Добавление доходов и расходов.
- Выбор категорий и подкатегорий.
- Ввод суммы транзакции.
- Сохранение данных в базу данных.

Основные компоненты:
- `start`: Обработчик команды /start. Отправляет приветственное сообщение и главное меню.
- `process_category`: Обработчик выбора категории (Доход/Расход). Запрашивает подкатегории.
- `process_subcategory`: Обработчик выбора подкатегории. Переводит в состояние ввода суммы.
- `process_amount`: Обработчик ввода суммы. Сохраняет транзакцию в базу данных.

Логирование:
- Все ключевые действия пользователей логируются для упрощения отладки.
- Логи включают идентификатор пользователя и детали выполняемых операций.
"""

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

@router.message(Command("start"))
async def start(message: types.Message):
    """
    Обработчик команды /start. Отправляет приветственное сообщение и главное меню.
    """
    keyboard = get_main_keyboard()
    logger.info(f"Пользователь {message.from_user.id} запустил бота. Отправлена главная клавиатура: {keyboard}")
    await message.answer(
        "Добро пожаловать! Я Ваш финансовый помощник.\n"
        "Выберите действие:",
        reply_markup=keyboard
    )

@router.message(lambda message: message.text in ["Доход", "Расход"])
async def process_category(message: types.Message, state: FSMContext):
    """
    Обработчик выбора категории (Доход/Расход). Запрашивает подкатегории и переводит в состояние выбора подкатегории.
    """
    category = message.text
    logger.info(f"Пользователь {message.from_user.id} выбрал категорию: {category}")
    await state.update_data(category=category)  # Сохраняем категорию

    categories = {"Доход": 1, "Расход": 2}
    category_id = categories.get(category)

    # Получаем подкатегории
    subcategories = await get_many_model_data(
        model_name="Subcategory",
        filters={"category_id": category_id}
    )
    subcategories = [{"id": sc.id, "name": sc.name} for sc in subcategories["records"]]
    logger.info(f"Получены подкатегории для {category}: {subcategories}")

    # Сохраняем подкатегории в состояние
    await state.update_data(subcategories=subcategories)

    # Создаем клавиатуру с подкатегориями
    subcategory_names = [subcat["name"] for subcat in subcategories]
    await message.answer(
        "Выберите подкатегорию:",
        reply_markup=get_subcategories_keyboard(subcategory_names)
    )

    await state.set_state(Form.subcategory)  # Переходим в состояние выбора подкатегории

@router.message(Form.subcategory)
async def process_subcategory(message: types.Message, state: FSMContext):
    """
    Обработчик выбора подкатегории. Переводит в состояние ввода суммы или возвращает в главное меню.
    """
    if message.text == "Назад":
        logger.info(f"Пользователь {message.from_user.id} нажал 'Назад'.")
        await state.clear()
        await message.answer(
            "Выберите действие:",
            reply_markup=get_main_keyboard()
        )
        return

    subcategory_name = message.text
    logger.info(f"Пользователь {message.from_user.id} выбрал подкатегорию: {subcategory_name}")
    data = await state.get_data()
    subcategories = data.get("subcategories")

    # Находим выбранную подкатегорию
    selected_subcategory = next((sc for sc in subcategories if sc["name"] == subcategory_name), None)
    if not selected_subcategory:
        logger.warning(f"Подкатегория {subcategory_name} не найдена для пользователя {message.from_user.id}.")
        await message.answer("Подкатегория не найдена.")
        return

    # Сохраняем subcategory_id в состояние
    await state.update_data(subcategory_id=selected_subcategory["id"])

    await message.answer("Введите сумму:")
    await state.set_state(Form.amount)  # Переходим в состояние ввода суммы

@router.message(Form.amount)
async def process_amount(message: types.Message, state: FSMContext):
    """
    Обработчик ввода суммы. Сохраняет транзакцию в БД или возвращает к выбору подкатегории.
    """
    if message.text == "Назад":
        logger.info(f"Пользователь {message.from_user.id} нажал 'Назад'")
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
        logger.info(f"Пользователь {message.from_user.id} ввел сумму: {amount}")
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
        response = await add_one_model_data(model_name="Transaction", values=transaction_data)
        logger.info(f"Транзакция сохранена для пользователя {message.from_user.id}. Ответ API: {response}")

        await message.answer("Данные успешно сохранены!")
        await state.clear()

        # Возврат в главное меню
        await message.answer(
            "Выберите действие:",
            reply_markup=get_main_keyboard()
        )

    except ValueError:
        logger.warning(f"Пользователь {message.from_user.id} ввел некорректную сумму: {message.text}")
        await message.answer("Пожалуйста, введите корректную сумму.")
