from pydantic import BaseModel
from typing import List, Optional
from pydantic.fields import Field

class CreateControlSchema(BaseModel):
    name: str
    description: Optional[str] =  Field(default=None)
    basic_controls: List[dict]
    
    
    
#   "description": "this is a description",

