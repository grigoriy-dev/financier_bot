from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.dao.base import db
from app.dao.schemas import UserSchema
from app.dao.models import User
from app.dao.generic import MainGeneric


router = APIRouter()


@router.get("/")
async def home_page():
    return {
        "message": "Hello. My name is Captain Capital"}

@router.get("/users")
async def get_users():
    session = await db.get_db()
    return await MainGeneric(User).find_all(session=session)

@router.get("/users")
async def get_user():
    session = await db.get_db()
    # поиск по id

@router.post("/users")
async def add_user():
    session = await db.get_db()
    user_data = UserSchema(telegram_id=245678, name="Anatoly")
    values = User(**user_data.dict())
    return await MainGeneric(User).add_one(session=session, values=values)
