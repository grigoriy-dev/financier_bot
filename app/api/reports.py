"""

"""

from fastapi import HTTPException
from datetime import datetime, timedelta

from app.api.routers import router
from app.cache.redis import get_redis


@router.get("/reports/get_free_report")
async def get_free_report():
    pass

@router.get("/reports/{period}")
async def get_report(period: str):    
    """
    Получение отчёта за указанный период.
    Поддерживаемые периоды: month, 3months, 6months, year, all.
    """
    # Определяем период для отчёта
    end_date = datetime.now()
    if period == "month":
        start_date = end_date - timedelta(days=30)
    elif period == "3months":
        start_date = end_date - timedelta(days=90)
    elif period == "6months":
        start_date = end_date - timedelta(days=180)
    elif period == "year":
        start_date = end_date - timedelta(days=365)
    elif period == "all":
        start_date = datetime.min  # Начало всех времён
    else:
        raise HTTPException(status_code=400, detail="Неподдерживаемый период")

    # Генерация уникального ключа для кеша
    cache_key = f"report:{period}:{start_date.date()}:{end_date.date()}"

    # Подключение к Redis
    redis = await get_redis()

    # Попытка получить данные из кеша
    cached_report = await redis.get(cache_key)
    if cached_report:
        return json.loads(cached_report)
