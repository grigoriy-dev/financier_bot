"""

"""

from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import pandas as pd

from app.dao.base import DatabaseSession as DB
from app.api.routers import get_many_transactions
#from app.cache.redis import get_redis


router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/{period}")
async def get_report(
        period: str = "all",
        filters: Optional[Dict[str, Any]] = None,
        paginate: bool = False,
        page: int = 1,
        page_size: int = 20
        ):    
    report = await get_many_transactions(paginate=False, period=period, filters=filters)
    
    filename_csv = 'data/output.csv'
    filename_xlsx = 'data/output.xlsx'

    df = pd.DataFrame(report["records"])

    # Сохраняем DataFrame
    df.to_csv(filename_csv, index=False)
    df.to_excel(filename_xlsx, index=False)

    return {"msg": "Данные выгружены"}
