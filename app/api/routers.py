from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import inspect
from typing import List

from app.dao.base import DatabaseSession as DB, engine
from app.dao.schemas import UserSchema
from app.dao.models import User
from app.dao.generic import MainGeneric


router = APIRouter()


@router.get("/")
async def home_page():
    async with engine.connect() as connection:
        tables = await connection.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
        
        return {"tables": tables}

@router.get("/users")
async def get_users():
    async with DB.get_session(commit=False) as session:
        return await MainGeneric(User).find_all(session=session)

@router.post("/users")
async def add_user(user_data: UserSchema):
    async with DB.get_session(commit=True) as session:
        return await MainGeneric(User).add_one(session=session, values=user_data)