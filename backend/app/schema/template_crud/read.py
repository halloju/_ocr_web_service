import os
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime


filepath = os.path.join(os.getcwd(), "app", "image-base64-string.txt")
with open(filepath, 'r') as f:
    img_base64_string = f.read()

class AvailableTemplates(BaseModel):
    template_id: str = Field(..., title="範本影像編號", example="1352020220930134411")
    template_name: str = Field(..., title='範本名稱', example='身分證')
    updated_at: datetime = Field(..., title='更新時間', example='2022-10-04T05:12:14.084870+00:00')

class GetAvailableTemplatesResponse(BaseModel):
    available_templates: List[AvailableTemplates] = Field(..., title="user_id 可取用的 template", example=[])

class GetTemplateDetailResponse(BaseModel):
    image: str = Field(..., title='範本影像', example=img_base64_string)
    template_name: str = Field(..., title='範本名稱', example='身分證')
    bbox: List = Field(..., title='使用者拉框留存的範本資訊', example=[{'type': 'text', 'tag': '姓名', 'x_min': 0, 'y_min': 0, 'x_max': 100, 'y_max': 100}, {'type': 'box', 'tag': '是否為範本', 'x_min': 130, 'y_min': 200, 'x_max': 200, 'y_max': 270}, {'type': 'mask', 'tag': None, 'x_min': 0, 'y_min': 0, 'x_max': 100, 'y_max': 100}])
