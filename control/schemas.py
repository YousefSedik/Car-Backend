from pydantic import BaseModel
from typing import List, Optional
from pydantic.fields import Field

class CreateControlSchema(BaseModel):
    name: str
    description: list[list] =  Field(default=None)
