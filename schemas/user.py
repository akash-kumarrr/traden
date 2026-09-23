from pydantic import BaseModel, EmailStr, computed_field
from datetime import datetime
from core.security import hash_password

class UserBase(BaseModel):
    name : str
    email : EmailStr

class UserCreate(UserBase):
    password : str

class UserResponse(UserBase):
    id : str
    created_at : datetime
    updated_at : datetime

    class Config : 
        from_attributes = True