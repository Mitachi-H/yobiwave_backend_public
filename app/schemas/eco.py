from pydantic import BaseModel

from typing import List

class LCIs(BaseModel):
    LCIName: str
    amount: float

class HazardousSubstance(BaseModel):
    group: str
    subgroup: str
    name: str
    normalized_name: str

    CO2: float
    CVC11: float
    U_235: float
    NMVOC: float
    disease: float
    CTUh_noncarcinogenic: float
    CTUh_carcinogenic: float
    H_plus: float
    Eutrophication_freshwater: float
    Eutrophication_Marine: float
    Eutrophication_Land: float
    CTUe: float
    Pt: float
    m3_depriv: float
    MJ: float
    Sb: float

class TotalHazardousSubstance(BaseModel):
    name: str
    CO2: float
    CVC11: float
    U_235: float
    NMVOC: float
    disease: float
    CTUh_noncarcinogenic: float
    CTUh_carcinogenic: float
    H_plus: float
    Eutrophication_freshwater: float
    Eutrophication_Marine: float
    Eutrophication_Land: float
    CTUe: float
    Pt: float
    m3_depriv: float
    MJ: float
    Sb: float

class TotalScore(BaseModel):
    name: str
    penguin_score: float
    turtle_score: float
    orangutan_score: float