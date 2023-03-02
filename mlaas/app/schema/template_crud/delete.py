from pydantic import BaseModel, Field, StrictStr, conlist
from datetime import datetime
from typing import Optional


class DeleteTemplateRequest(BaseModel):
    template_id: str = Field(..., title="範本影像編號", example="1352020220930134411")

class DeleteTemplateResponse(BaseModel):
    status_code: StrictStr = Field(
        title='服務狀態碼',
        description='''
        API 服務正常："0000"
        程式碼錯誤："0001"
        template_id 不存在: "5407"
        ''',
        example='0000'
    )
    status_msg: StrictStr = Field(
        title='服務狀態內容',
        description='''
        API 服務正常："OK"
        程式碼錯誤："code error"
        template_id 不存在: "template_id not exist"
        ''',
        example='OK'
    )
    err_detail: Optional[dict] = Field(
        title='錯誤訊息',
        description='''
        '''
    )