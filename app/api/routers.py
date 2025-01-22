from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def home_page():
    return {
        "message": "Hello. My name is Captain Capital"}