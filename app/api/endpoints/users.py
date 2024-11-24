from fastapi import APIRouter
from mock_data.data import users
from typing import List

router = APIRouter()

@router.get("/users", response_model=List[dict])
async def get_users():
    return users