from pydantic import BaseModel

from typing import List

class TestItem(BaseModel):
    name: str
    lastname: str
    age: int