from pydantic import BaseModel, Field, validator
from typing import Optional
from app.common.schema import img_base64_string


class Back_PredictInput(BaseModel):
    image: str = Field(...,
                       description='''base64 字串的影像<br /><br />''',
                       example=img_base64_string)

    @validator("image", allow_reuse=True)
    def image_check(cls, v):
        if v == '':
            raise ValueError("影像不得為空字串")
        return v


class Back_PredictOutput(BaseModel):
    status_code: str = Field(...,
                             description='''服務狀態碼<br /><br />
                                            狀態碼：<br />
                                            API 服務正常："0000"<br />
                                            程式碼錯誤："0001"<br />
                                            DB相關錯誤："0002"<br />
                                            request_id 重複呼叫："5401"<br />
                                            ''',
                             example="0000")
    status_msg: str = Field(...,
                            description='''服務狀態內容<br /><br />
                                           狀態內容<br />
                                           API 服務正常："OK"<br />
                                           程式碼錯誤："code error"<br />
                                           DB相關錯誤："DB error"<br />
                                           request_id 重複呼叫："unique violation"<br />
                                           ''',
                            example="OK")
    err_detail: Optional[dict] = Field(
        title="錯誤訊息",
        description="""
        """,
    )
    account: str = Field(...,
                         description='''帳號<br /><br />
                                        帳號內容<br />
                                        回辨識過後的帳號："0129979143656"<br />
                                        若帳號格式為分行代碼+S20，則如實回傳："0015S20"<br />
                                        若帳號長度超逾或不足13碼，則回傳空字串：""<br />
                                        ''',
                         example="OK")
