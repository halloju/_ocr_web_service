import os
from typing import Optional, List
from pydantic import BaseModel, Field, StrictStr, validator, Extra, conlist
from app.schema.common import img_base64_string


class GpocrRequest(BaseModel):
    image: StrictStr = Field(
        title='base64 字串的影像',
        description='''
        ''',
        example=img_base64_string
    )
    image_complexity: Optional[StrictStr] = Field(
        default='medium',
        title='影像複雜度',
        description='''
        中等："medium"
        高："high"
        ''',
        example='medium'
    )
    filters: conlist(StrictStr, min_items=1) = Field(
        title='框的過濾器',
        example=['tchinese', 'english', 'number', 'symbol'],
        default=['tchinese', 'english', 'number', 'symbol']
    )

    @validator("image", allow_reuse=True)
    def image_check(cls, v):
        if v == '':
            raise ValueError("影像不得為空字串")
        return v

    @validator("image_complexity", allow_reuse=True)
    def image_complexity_check(cls, v):
        if v not in ['medium', 'high']:
            raise ValueError("影像複雜度僅可為 medium 或 high")
        return v


class OcrPredict(BaseModel, extra=Extra.forbid):
    points: List = Field(
        title='文字區域的點位',
        example=[[1, 2], [1, 3], [1, 5], [1, 8]]
    )
    text: StrictStr = Field(
        title='辨識結果',
        example="F1234567"
    )
    det_prob: float = Field(
        title='偵測機率值',
        example=0.9586
    )
    rec_prob: float = Field(
        title='辨識機率值',
        example=0.9586
    )


class GpocrResponse(BaseModel):
    status_code: StrictStr = Field(
        title='服務狀態碼',
        description='''
        API 服務正常："0000"
        程式碼錯誤："0001"
        重複 request ID: "5401"
        圖檔格式錯誤: "5402"
        ''',
        example='0000'
    )
    status_msg: StrictStr = Field(
        title='服務狀態內容',
        description='''
        API 服務正常："OK"
        程式碼錯誤："code error"
        重複 request ID: "unique violation"
        圖檔格式錯誤: "image type error"
        ''',
        example='OK'
    )
    err_detail: Optional[dict] = Field(
        title='錯誤訊息',
        description='''
        '''
    )
    image_cv_id: Optional[StrictStr] = Field(
        title='影像註冊的 key 值',
        description='''
        ''',
        example='2022/09/20/19/30/438ffd10-1090-4687-be84-8f6c36be463a'
    )
    data_results: Optional[List[OcrPredict]]
