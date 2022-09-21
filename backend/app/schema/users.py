from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    account: str
    name: str
    birthday: str
    password: str

class ShowUser(BaseModel):
    username: str
    name: str
    birthday: str
    is_active: bool

    class Config():
        orm_mode = True

class ResetRequest(BaseModel):
    account: str = Field(..., title="員編", example="ESB12366")
    birthday: str = Field(..., title="生日", example="19991231")
    password: str = Field(..., title="密碼", example="esun1313")

class RegisterRequest(ResetRequest):
    name: str = Field(..., title="姓名", example="陳小美")

class ModifyRequest(BaseModel):
    account: str = Field(..., title="員編", example="ESB12366")
    name: str = Field(..., title="姓名", example="陳大美")
    password: str = Field(..., title="密碼", example="esun1212")

class LoginRequest(BaseModel):
    account: str = Field(..., title="員編", example="ESB12366")
    password: str = Field(..., title="密碼", example="esun1313")