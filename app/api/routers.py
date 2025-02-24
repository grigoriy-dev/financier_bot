from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
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

@router.post("/users")
async def add_user():
    session = await db.get_db_with_commit()
    user_data = UserSchema(telegram_id=325236, name="Armonte")
    added_user = await MainGeneric(UserSchema).add_one(session, user_data)
    return added_user