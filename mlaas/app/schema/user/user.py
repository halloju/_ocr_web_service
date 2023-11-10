from pydantic import BaseModel, Field, StrictStr
from typing import Optional


class UserCreate(BaseModel):
    user_id: str = Field(..., title="員編", example="12345")
    name: str = Field(..., title="員編", example="小美")
    role: str = Field(..., title="員編", example="user")


class AuthModel(BaseModel):
    email: str = Field(..., title="隊長信箱", example="test-1@gmail.com")
    code: str = Field(..., title="OTP", example="734857")


class AuthUsereRequest(BaseModel):
    user_id: str = Field(..., title="員編", example="12345")


class AuthUserResponse(BaseModel):
    status_code: StrictStr = Field(
        title='服務狀態碼',
        description='''
        API 服務正常："0000"
        程式碼錯誤："0001"
        資料庫錯誤："0002"
        ''',
        example='0000'
    )
    status_msg: StrictStr = Field(
        title='服務狀態內容',
        description='''
        API 服務正常："OK"
        程式碼錯誤："code error"
        資料庫錯誤："DB error"
        ''',
        example='OK'
    )
    err_detail: Optional[dict] = Field(
        title='錯誤訊息',
        description='''
        '''
    )
    is_authenticated: bool = Field(
        title="使用者是否成功驗證", example=True)
