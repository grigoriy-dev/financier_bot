from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.base import db
from app.schemas import User
from app.generic import BigGeneric

router = APIRouter()


@router.get("/")
async def home_page():
    return {
        "message": "Hello. My name is Captain Capital"}

@router.get("/users")
async def get_users(session: AsyncSession = Depends(db.get_db)):
    return await BigGeneric(User).find_all(session=session)
