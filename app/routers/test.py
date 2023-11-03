from fastapi import APIRouter, Depends
# from pydantic import BaseModel
from typing import List
from ..database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from ..cruds import test
from ..schemas import test as test_schema

router = APIRouter(tags = ['test'])

@router.get("/test", response_model=List[test_schema.TestItem])
async def get_test(session: AsyncSession = Depends(get_session)) -> str:
    return (await test.get_test_items(session))

@router.post("/test")
async def add_test(test_item: test_schema.TestItem, session: AsyncSession = Depends(get_session)) -> bool:
    return (await test.add_test_item(session, test_item))