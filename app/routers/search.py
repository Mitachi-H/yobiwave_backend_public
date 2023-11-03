from fastapi import APIRouter, Depends
# from pydantic import BaseModel
from typing import List
from ..database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from ..cruds import eco
from ..schemas import eco as eco_schema

router = APIRouter(tags = ['search'])

@router.get("/search/{LCIName}", response_model=eco_schema.HazardousSubstance)
async def get_hazardous_substance(LCIName: str, session: AsyncSession = Depends(get_session)):
    return (await eco.get_hazardous_substance(LCIName, session))