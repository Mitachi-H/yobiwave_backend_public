from ..schemas import eco as eco_schema
from ..cruds import eco as eco_crud
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

# =AE4*0.4+AM4*0.2+AD4*0.15+AK4*0.1+AQ4*0.05+AR4*0.03+AO4*0.03+AP4*0.02+AI4*0.01+AJ4*0.01
penguin_weight = {
        "CO2" : 0.15,
        "CVC11" : 0.4,
        "U_235" : 0,
        "NMVOC" : 0,
        "disease" : 0,
        "CTUh_noncarcinogenic" : 0.01,
        "CTUh_carcinogenic" : 0.01,
        "H_plus" : 0,
        "Eutrophication_freshwater" : 0,
        "Eutrophication_Marine" : 0.1,
        "Eutrophication_Land" : 0,
        "CTUe" : 0.03,
        "Pt" : 0.02,
        "m3_depriv" : 0.05,
        "MJ" : 0.03,
        "Sb" : 0,
}
# =AM5*0.35+AQ5*0.2+AD5*0.15+AI5*0.1+AK5*0.05+AE5*0.05+AP5*0.04+AR5*0.03+AJ5*0.02+AO5*0.01
turtle_weight = {
        "CO2" : 0.15,
        "CVC11" : 0.05,
        "U_235" : 0,
        "NMVOC" : 0,
        "disease" : 0,
        "CTUh_noncarcinogenic" : 0.1,
        "CTUh_carcinogenic" : 0.02,
        "H_plus" : 0.05,
        "Eutrophication_freshwater" : 0,
        "Eutrophication_Marine" : 0.35,
        "Eutrophication_Land" : 0,
        "CTUe" : 0.01,
        "Pt" : 0.04,
        "m3_depriv" : 0.2,
        "MJ" : 0.03,
        "Sb" : 0,
}
# =AP4*0.4+AQ4*0.2+AO4*0.15+AI4*0.1+AH4*0.05+AL4*0.03+AK4*0.03+AD4*0.02+AJ4*0.01
orangutan_weight = {
        "CO2" : 0.02,
        "CVC11" : 0,
        "U_235" : 0,
        "NMVOC" : 0,
        "disease" : 0.05,
        "CTUh_noncarcinogenic" : 0.1,
        "CTUh_carcinogenic" : 0.01,
        "H_plus" : 0.03,
        "Eutrophication_freshwater" : 0.03,
        "Eutrophication_Marine" : 0,
        "Eutrophication_Land" : 0,
        "CTUe" : 0.15,
        "Pt" : 0.4,
        "m3_depriv" : 0.2,
        "MJ" : 0,
        "Sb" : 0,
}

def cal_total_score(product_name: str, total_hazardous_substance: eco_schema.TotalHazardousSubstance) -> eco_schema.TotalScore:
    total_score = {"name": product_name,
                   "penguin_score": 0,
                   "turtle_score": 0,
                   "orangutan_score": 0}
    # Do the weighted sum for each attribute in the TotalHazardousSubstance class
    for key, value in total_hazardous_substance.__dict__.items():
        if key != 'name':
            total_score["penguin_score"] += value * penguin_weight[key]
            total_score["turtle_score"] += value * turtle_weight[key]
            total_score["orangutan_score"] += value * orangutan_weight[key]
    return eco_schema.TotalScore(**total_score)

async def cal_hazardous_substances(product_name: str, LCIs: List[eco_schema.LCIs], session: AsyncSession) -> eco_schema.TotalHazardousSubstance:
    total_hazardous_substance = {
        "name" : product_name,
        "CO2" : 0,
        "CVC11" : 0,
        "U_235" : 0,
        "NMVOC" : 0,
        "disease" : 0,
        "CTUh_noncarcinogenic" : 0,
        "CTUh_carcinogenic" : 0,
        "H_plus" : 0,
        "Eutrophication_freshwater" : 0,
        "Eutrophication_Marine" : 0,
        "Eutrophication_Land" : 0,
        "CTUe" : 0,
        "Pt" : 0,
        "m3_depriv" : 0,
        "MJ" : 0,
        "Sb" : 0,
    }
    
    for LCI in LCIs:
        hazardous_substance = (await eco_crud.get_hazardous_substance(LCI.LCIName, session))
        print(hazardous_substance)
        if hazardous_substance:
            # Do the weighted sum for each attribute in the HazardousSubstance class
            for key, value in hazardous_substance.__dict__.items():
                if key != 'name' and key != 'group' and key != 'subgroup' and key != 'normalized_name':
                    total_hazardous_substance[key] += LCI.amount * value
    print("---total---")
    print(total_hazardous_substance)
    print(type(total_hazardous_substance))
    print("---*---")
    return eco_schema.TotalHazardousSubstance(**total_hazardous_substance)