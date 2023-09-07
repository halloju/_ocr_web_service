import os
from typing import List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist, Extra


filepath = os.path.join(os.getcwd(), "app", "image-base64-string.txt")
with open(filepath, 'r') as f:
    img_base64_string = f.read()


class PointDict(BaseModel, extra=Extra.forbid):
    type: StrictStr = Field(
        title='框的類型',
        description='''
            文字: 'text'
            方塊: 'box'
            遮罩: 'mask'
        ''',
        example='text'
    )
    tag: Optional[StrictStr] = Field(
        ...,
        title='框的類型',
        example='姓名'
    )
    points: conlist(List, min_items=4, max_items=4) = Field(
        title='框的點位',
        example=[[0, 0], [100, 0], [100, 100], [0, 100]]
    )


class AvailableTemplates(BaseModel):
    template_id: str = Field(..., title="範本影像編號",
                             example="1352020220930134411")
    template_name: str = Field(..., title='範本名稱', example='身分證')
    creation_time: StrictStr = Field(
        ...,
        title='模型建立時間',
        example='2022-10-04 05:12:14')
    expiration_time: Optional[StrictStr] = Field(
        ...,
        title='模型到期時間',
        description='''
        模型到期後會自動清除，如果回傳 null，則代表沒有期限
        ''',
        example='2022-10-04 05:12:14')


class GetAvailableTemplatesRequest(BaseModel):
    user_id: StrictStr = Field(..., title="員編", example="13520")


class GetTemplateDetailRequest(BaseModel):
    template_id: StrictStr = Field(..., title="範本影像編號",
                                   example="1352020220930134411")


class GetAvailableTemplatesResponse(BaseModel):
    template_infos: Optional[List[AvailableTemplates]] = Field(
        title="user_id 可取用的 template", example=[])


class GetTemplateDetailResponse(BaseModel):
    image: str = Field(..., title='範本影像', example=img_base64_string)
    is_no_ttl: bool = Field(..., title='是否永久保存', example=False)
    points_list: conlist(PointDict, min_items=1) = Field(..., title='使用者拉框留存的範本資訊', example=[{'type': 'text', 'tag': '姓名', 'points': [[0, 0], [100, 0], [100, 100], [0, 100]]}, {
        'type': 'box', 'tag': '是否為範本', 'points': [[130, 200], [200, 200], [200, 270], [130, 270]]}, {'type': 'mask', 'tag': None, 'points': [[130, 200], [200, 200], [200, 270], [130, 270]]}])
    template_name: str = Field(..., title='範本名稱', example='身分證')
    creation_time: StrictStr = Field(
        ...,
        title='模型建立時間',
        example='2022-10-04 05:12:14')
    expiration_time: Optional[StrictStr] = Field(
        ...,
        title='模型到期時間',
        description='''
        模型到期後會自動清除，如果回傳 null，則代表沒有期限
        ''',
        example='2022-10-04 05:12:14')
