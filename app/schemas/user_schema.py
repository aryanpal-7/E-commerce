from pydantic import BaseModel, Field
from typing import Optional


# Using this pydantic model to request and validate user registration data
class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: str
    password: str = Field(..., min_length=5, max_length=18)
    role: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "example@email.com",
                "password": "Strong@123",
                "role": "",
            }
        }


class UserResponse(BaseModel):
    name: str
    email: str


class UserLogin(BaseModel):
    email: str
    password: str = Field(..., min_length=5, max_length=18)

    class Config:
        json_schema_extra = {
            "example": {"email": "example@gmail.com", "password": "Strong@123"}
        }


class AdminSchema(UserRegister):
    role: str = "admin"
