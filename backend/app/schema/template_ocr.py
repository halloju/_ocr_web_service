from typing import Optional, List
from pydantic import BaseModel, Field, StrictStr, validator, Extra


class CreateTemplateOCRRequest(BaseModel):
    image: StrictStr = Field(
        title='base64 字串的影像',
        description='''
        ''',
        example='/9j/4AAQSkZJRgABAQEBLAEsAAD/2w'
    )
    template_id: StrictStr = Field(
        title='alignment 的模板編號（key）',
        description='''
        需先上傳特定模板，才能使用
        ''',
        example='1352020221012111646'
    )
    model_name: Optional[StrictStr] = Field(
        default='template_alignment+cht_ppocr_v1',
        title='文字辨識模型名稱',
        description='''
        格式為：det_model+rec_model
        template_alignment+rec_model
        e.g. template_alignment+cht_ppocr_v1

        目前可使用的detection模型：
        template_alignment

        目前可使用的recognition模型：
        cht_ppocr_v1 (繁體中文模型)
        en_ppocr_v0 (英文模型)
        ''',
        example='template_alignment+cht_ppocr_v1'
    )

    @validator("image", allow_reuse=True)
    def image_check(cls, v):
        if v == '':
            raise ValueError("影像不得為空字串")
        return v

    @validator("template_id", allow_reuse=True)
    def template_id_check(cls, v):
        if len(v) != 19:
            raise ValueError("模板編碼必為19碼")
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
    rec_prob: float = Field(
        title='辨識機率值',
        example=0.9586
    )
    tag: Optional[StrictStr] = Field(
        title='辨識要項',
        example="id")


class GetTemplateOCRResponse(BaseModel):
    image_cv_id: StrictStr = Field(
        title='影像註冊的 key 值',
        description='''
        ''',
        example='2022/09/20/19/30/438ffd10-1090-4687-be84-8f6c36be463a'
    )
    ocr_results: List[OcrPredict]
