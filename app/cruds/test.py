from typing import List
from sqlalchemy import select, delete, update, bindparam
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.db_models import Test
from ..schemas import test as test_schema

async def get_test_items(session: AsyncSession) -> List[Test]:
   
    statement = select(Test)

    result = await session.execute(statement)
    return result.scalars().all()

async def add_test_item(session: AsyncSession, test_item: test_schema.TestItem) -> bool:
    test_model = Test(**test_item.dict())
    session.add(test_model)
    await session.commit()
    return True