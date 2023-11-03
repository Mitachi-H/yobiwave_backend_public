from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..openai_api import chat
from typing import List
from ..schemas import eco as eco_schema
from ..cal_score import eco_score
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_session

router = APIRouter(tags = ['eco_scoring'])

@router.get("/LCINames/{product_name}", response_model = List[eco_schema.LCIs])
async def get_LCINames(product_name: str):
    return (await chat.get_LCIs(product_name))

# @router.get("/LCINames/HazardousSubstance/{product_name}", response_model = List[eco_schema.TotalHazardousSubstance])
# async def cal_hazardous_substances(product_name: str, session: AsyncSession = Depends(get_session)):
#     LCIs = await chat.get_LCIs(product_name)
#     return (await eco_score.cal_hazardous_substances(product_name, LCIs, session))

@router.post("/LCINames/HazardousSubstance/{product_name}", response_model = eco_schema.TotalHazardousSubstance)
async def cal_hazardous_substances_test(product_name: str, LCIs: List[eco_schema.LCIs], session: AsyncSession = Depends(get_session)) -> str:
    return (await eco_score.cal_hazardous_substances(product_name, LCIs, session))

@router.post("/LCINames/totalscore/{product_name}", response_model = eco_schema.TotalScore)
async def cal_total_score(product_name: str, total_hazardous_substance: eco_schema.TotalHazardousSubstance):
    return eco_score.cal_total_score(product_name, total_hazardous_substance)