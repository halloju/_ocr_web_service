import os
from typing import List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist
from datetime import datetime


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

class TemplateDetail(BaseModel, extra=Extra.forbid):
    image: str = Field(..., title='範本影像', example=img_base64_string)
    points_list: conlist(PointDict, min_items=1) = Field(..., title='使用者拉框留存的範本資訊', example=[{'type': 'text', 'tag': '姓名', 'points': [[0, 0], [100, 0], [100, 100], [0, 100]]}, {'type': 'box', 'tag': '是否為範本', 'points': [[130, 200], [200, 200], [200, 270], [130, 270]]}, {'type': 'mask', 'tag': None, 'points': [[130, 200], [200, 200], [200, 270], [130, 270]]}])
    template_name: str = Field(..., title='範本名稱', example='身分證')
    updated_at: datetime = Field(..., title='更新時間', example='2022-10-04T05:12:14.084870+00:00')

class AvailableTemplates(BaseModel):
    template_id: str = Field(..., title="範本影像編號", example="1352020220930134411")
    template_name: str = Field(..., title='範本名稱', example='身分證')
    updated_at: datetime = Field(..., title='更新時間', example='2022-10-04T05:12:14.084870+00:00')

class GetAvailableTemplatesRequest(BaseModel):
    user_id: StrictStr = Field(..., title="員編", example="13520")

class GetTemplateDetailRequest(BaseModel):
    template_id: StrictStr = Field(..., title="範本影像編號", example="1352020220930134411")

class GetAvailableTemplatesResponse(BaseModel):
    status_code: StrictStr = Field(
        title='服務狀態碼',
        description='''
        同 apihub
        ''',
        example='0000'
    )
    status_msg: StrictStr = Field(
        title='服務狀態內容',
        description='''
        同 apihub
        ''',
        example='OK'
    )
    err_detail: Optional[dict] = Field(
        title='錯誤訊息',
        description='''
        '''
    )
    template_infos: Optional[List[AvailableTemplates]] = Field(..., title="user_id 可取用的 template", example=[])

class GetTemplateDetailResponse(BaseModel):
    status_code: StrictStr = Field(
        title='服務狀態碼',
        description='''
        同 apihub
        ''',
        example='0000'
    )
    status_msg: StrictStr = Field(
        title='服務狀態內容',
        description='''
        同 apihub
        ''',
        example='OK'
    )
    err_detail: Optional[dict] = Field(
        title='錯誤訊息',
        description='''
        '''
    )
    template_detail: Optional[TemplateDetail]
