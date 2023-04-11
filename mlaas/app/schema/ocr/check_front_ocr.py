from pydantic import BaseModel, Field, validator
from typing import Optional
from app.schema.common import img_base64_string


class Front_Out_PredictInput(BaseModel):
    image: str = Field(...,
                       description='''base64 字串的影像<br /><br />''',
                       example=img_base64_string)

    @validator("image", allow_reuse=True)
    def image_check(cls, v):
        if v == '':
            raise ValueError("影像不得為空字串")
        return v


class Front_Out_PredictOutput(BaseModel):
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
    amount: str = Field(...,
                        description='''支票金額<br /><br />
                                    數字靠右左補零 (11碼)<br />
                                    ''',
                        example="00000070000")
    due_date: str = Field(...,
                          description='''支票到期日<br /><br />
                                      共 7 碼<br />
                                      年份為 3 碼的民國年<br />
                                      月份為 2 碼<br />
                                      日期為 2 碼<br />
                                      ''',
                          example="1110111")
