"""

"""

from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import pandas as pd

from app.dao.base import DatabaseSession as DB
from app.dao.generic import MainGeneric
from app.dao.models import MODELS


router = APIRouter(prefix="/reports", tags=["Reports"])
