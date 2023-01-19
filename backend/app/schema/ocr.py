from typing import Optional, List
from pydantic import BaseModel, Field, StrictStr, validator, Extra


class CreateGPOCRRequest(BaseModel):
    image: StrictStr = Field(
        title='base64 字串的影像',
        description='''
        ''',
        example='iVBORw0KGgoAAAANSUhEUgAAACwAAAAbCAIAAACImfpDAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAA0SURBVEhL7c4xDQAgEAAx/Jtk5V0wkNPA0qQCuvac7yQiEYlIRCISkYhEJCIRiUhE4plzAes2eXW72BJeAAAAAElFTkSuQmCC'
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
    language: Optional[StrictStr] = Field(
        default='Chinese',
        title='影像複雜度',
        description='''
        中文："Chinese"
        ''',
        example='Chinese'
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
    det_prob: Optional[float] = Field(
        title='偵測機率值',
        example=0.9586
    )
    rec_prob: float = Field(
        title='辨識機率值',
        example=0.9586
    )


class GetGPOCRResponse(BaseModel):
    image_cv_id: StrictStr = Field(
        title='影像註冊的 key 值',
        description='''
        ''',
        example='2022/09/20/19/30/438ffd10-1090-4687-be84-8f6c36be463a'
    )
    ocr_results: List[OcrPredict]
