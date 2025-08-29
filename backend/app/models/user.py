


from pydantic import BaseModel, EmailStr
from typing import Optional
from bson import ObjectId



class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        json_schema = handler(core_schema)
        json_schema["type"] = "string"
        return json_schema


class UserBase(BaseModel):
    email: EmailStr
    user_name: str


class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    id: Optional[PyObjectId] = None
    hashed_password: str
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserInDB(User):
    pass

class UserPublic(BaseModel):
    class Config:
        json_encoders = {ObjectId: str}
    id: Optional['PyObjectId'] = None
    email: EmailStr
    user_name: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserPublic

class TokenData(BaseModel):
    email: Optional[str] = None