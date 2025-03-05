"""

"""

from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta

from app.dao.base import DatabaseSession as DB
from app.dao.generic import MainGeneric
from app.dao.models import MODELS
#from app.cache.redis import get_redis


router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/get_free_report")
async def get_free_report():
    pass

@router.get("/{period}")
async def get_report(period: str, filters):    
    pass
