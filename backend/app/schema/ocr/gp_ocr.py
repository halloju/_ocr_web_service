import os
from typing import List, Optional
from pydantic import BaseModel, Field, StrictStr, validator, Extra


filepath = os.path.join(os.getcwd(), "app", "image-base64-string.txt")
with open(filepath, 'r') as f:
    img_base64_string = f.read()


class GpocrUpload(BaseModel):
    image: str = Field(
        title='base64 字串的影像',
        description='''
        ''',
        example=img_base64_string
    )
    image_id: str = Field(
        title="image id",
        description='''
        ''',
        example="id1"
    )

    @validator("image", allow_reuse=True)
    def image_check(cls, v):
        if v == '':
            raise ValueError("影像不得為空字串")
        return v


class GpocrPredict(BaseModel):
    imageList: List[str] = Field(
        title='單張或多張影像的 image id (Redis)',
        description='''
        ''',
        example=["id1", "id2"]
    )
    model_name: Optional[StrictStr] = Field(
        default='dbnet_v0+cht_ppocr_v1',
        title='文字辨識模型名稱',
        description='''
        格式為: det_model+rec_model
        e.g., dbnet_v0+cht_ppocr_v1

        目前可使用的detection模型:
        dbnet_v0(中文＋英文模型)

        目前可使用的recognition模型:
        cht_ppocr_v1(繁體中文模型)
        en_ppocr_v0(英文模型)
        ''',
        example='dbnet_v0+cht_ppocr_v1'
    )

    @validator("imageList", allow_reuse=True)
    def image_check(cls, v):
        if v == '':
            raise ValueError("影像不得為空字串")
        return v

    @validator("model_name", allow_reuse=True)
    def model_name_check(cls, v):
        if len(v.split("+")) != 2:
            raise ValueError("model_name 格式為: det_model+rec_model")
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
    image_cv_id: StrictStr = Field(
        title='影像註冊的 key 值',
        description='''
        ''',
        example='2022/09/20/19/30/438ffd10-1090-4687-be84-8f6c36be463a'
    )
    data_results: List[OcrPredict]
