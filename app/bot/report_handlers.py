from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from loguru import logger

from app.api.routers import get_report
from app.bot.keyboards import get_main_keyboard, get_report_period_keyboard


router = Router()

@router.message(lambda message: message.text == "Отчёт")
async def report_command(message: types.Message, state: FSMContext):
    await message.answer("Выберите период для отчёта:", reply_markup=get_report_period_keyboard())

@router.message(lambda message: message.text in ["Месяц", "3 месяца", "Год", "Всё время"])
async def process_report_period(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer(
            "Выберите действие:",
            reply_markup=get_main_keyboard()
        )
        return

    period = message.text
    response = await get_report(period=period, format="csv")

    if response.get("msg") == "Данные выгружены в CSV":
        file = FSInputFile("data/output.csv")
        await message.answer_document(file, caption="Ваш отчёт готов!")
    else:
        await message.answer("Произошла ошибка при формировании отчёта.")
