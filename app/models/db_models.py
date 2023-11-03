from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DATETIME, Float

from ..database import Base

class Test(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=True)
    lastname = Column(String(128), nullable=True)
    age = Column(Integer, nullable=True)
    created_at = Column(DATETIME, default = datetime.now())
    updated_at = Column(DATETIME, default = datetime.now())

class HazardousSubstance(Base):
    __tablename__ = "hazardous_substance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group = Column(String(128), nullable=True)
    subgroup = Column(String(128), nullable=True)
    name = Column(String(256), nullable=True)
    normalized_name = Column(String(256), nullable=True)

    CO2 = Column(Float, nullable=True)
    CVC11 = Column(Float, nullable=True)
    U_235 = Column(Float, nullable=True)
    NMVOC = Column(Float, nullable=True)
    disease = Column(Float, nullable=True)
    CTUh_noncarcinogenic = Column(Float, nullable=True)
    CTUh_carcinogenic = Column(Float, nullable=True)
    H_plus = Column(Float, nullable=True)
    Eutrophication_freshwater = Column(Float, nullable=True)
    Eutrophication_Marine = Column(Float, nullable=True)
    Eutrophication_Land = Column(Float, nullable=True)
    CTUe = Column(Float, nullable=True)
    Pt = Column(Float, nullable=True)
    m3_depriv = Column(Float, nullable=True)
    MJ = Column(Float, nullable=True)
    Sb = Column(Float, nullable=True)