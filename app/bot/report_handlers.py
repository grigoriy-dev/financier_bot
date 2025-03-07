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

@router.message(lambda message: message.text in ["Месяц", "3 месяца", "Полгода" "Год", "Всё время", "Назад"])
async def process_report_period(message: types.Message, state: FSMContext):
    logger.info(f"message {message.text}")
    if message.text == "Назад":
        await state.clear()
        await message.answer(
            "Выберите действие:",
            reply_markup=get_main_keyboard()
        )
        return

    periods = {
        "Месяц": "month", 
        "3 месяца":"3months", 
        "Полгода": "6months",
        "Год": "year", 
        "Всё время": "all"
    }
    period = periods.get(message.text)
    response = await get_report(period=period, format="xlsx")

    if response.get("msg") in ["Данные выгружены в XLSX"]:
        file = FSInputFile("data/output.xlsx")
        await message.answer_document(file, caption="Ваш отчёт готов!")
    else:
        await message.answer("Произошла ошибка при формировании отчёта.")

     # Возврат в главное меню
    await message.answer(
        "Выберите действие:",
        reply_markup=get_main_keyboard()
    )   
