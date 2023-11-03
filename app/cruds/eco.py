from typing import List
from sqlalchemy import select, delete, update, bindparam
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.db_models import HazardousSubstance
from ..schemas import eco as eco_schema

def normalize_string(s: str) -> str:
    return s.lower().replace(" ", "").replace(",", "")

async def get_hazardous_substance(LCIName: str, session: AsyncSession) -> eco_schema.HazardousSubstance:
    statement = select(HazardousSubstance).where(HazardousSubstance.normalized_name == normalize_string(LCIName))
    result = await session.execute(statement)
    ## dbモデルからpydanticモデルに変換
    return eco_schema.HazardousSubstance(**result.scalars().first().__dict__)