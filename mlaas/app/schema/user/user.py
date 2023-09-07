from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    user_id: str = Field(..., title="員編", example="12345")
    name: str = Field(..., title="員編", example="小美")
    role: str = Field(..., title="員編", example="user")


class AuthModel(BaseModel):
    email: str = Field(..., title="隊長信箱", example="test-1@gmail.com")
    code: str = Field(..., title="OTP", example="734857")
