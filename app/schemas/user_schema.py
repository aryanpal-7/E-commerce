from pydantic import BaseModel, Field


# Using this pydantic model to request and validate user registration data
class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: str
    password: str = Field(..., min_length=5, max_length=18)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "example@email.com",
                "password": "Strong@123",
            }
        }


# Using this pydantic model to request and validate user Login details
class UserLogin(BaseModel):
    email: str
    password: str = Field(..., min_length=5, max_length=18)
