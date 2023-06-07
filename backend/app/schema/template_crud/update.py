from typing import List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist, Extra
from datetime import datetime


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
        title='框的類型',
        example='姓名'
    )
    points: conlist(List, min_items=4, max_items=4) = Field(
        title='框的點位',
        example=[[0, 0], [100, 0], [100, 100], [0, 100]]
    )

class UpdateTemplateRequest(BaseModel):
    template_id: str = Field(..., title="範本影像編號", example="1352020220930134411")
    points_list: conlist(PointDict, min_items=1) = Field(..., title='使用者拉框留存的範本資訊', example=[{'type': 'text', 'tag': '姓名', 'points': [[0, 0], [100, 0], [100, 100], [0, 100]]}, {'type': 'box', 'tag': '是否為範本', 'points': [[130, 200], [200, 200], [200, 270], [130, 270]]}, {'type': 'mask', 'tag': None, 'points': [[130, 200], [200, 200], [200, 270], [130, 270]]}])
    template_name: str = Field(..., title='範本名稱', example='身分證')

class UpdateTemplateResponse(BaseModel):
    template_id: Optional[str] = Field(title="範本影像編號", example="1352020220930134411")
