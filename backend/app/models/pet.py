from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
from .user import PyObjectId


class PetBase(BaseModel):
    name: str
    type: str
    age: int
    notes: Optional[str] = ""
    breed: Optional[str] = None

class PetCreate(PetBase):
    pass

class Pet(PetBase):
    id: Optional[PyObjectId] = None
    owner_id: PyObjectId
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class PetInDB(Pet):
    pass