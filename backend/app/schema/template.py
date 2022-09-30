from typing import Optional, List
from pydantic import BaseModel, Field


class CreateTemplateRequest(BaseModel):
    user_id: str = Field(..., title="員編", example="13520")
    image: str = Field(..., title='範本影像', example='')
    bbox: List = Field(..., title='使用者拉框留存的範本資訊', example=[{'type': 'text', 'tag': '姓名', 'x_min': 0, 'y_min': 0, 'x_max': 100, 'y_max': 100}, {'type': 'box', 'tag': '是否為範本', 'x_min': 130, 'y_min': 200, 'x_max': 200, 'y_max': 270}, {'type': 'mask', 'tag': None, 'x_min': 0, 'y_min': 0, 'x_max': 100, 'y_max': 100}])
    template_name: str = Field(..., title='範本名稱', example='身分證')


class UpdateTemplateRequest(BaseModel):
    template_id: str = Field(..., title="範本影像編號", example="13520220930134411")
    bbox: List = Field(..., title='使用者拉框留存的範本資訊', example=[{'type': 'text', 'tag': '姓名', 'x_min': 0, 'y_min': 0, 'x_max': 100, 'y_max': 100}, {'type': 'box', 'tag': '是否為範本', 'x_min': 130, 'y_min': 200, 'x_max': 200, 'y_max': 270}, {'type': 'mask', 'tag': None, 'x_min': 0, 'y_min': 0, 'x_max': 100, 'y_max': 100}])


class DeleteTemplateRequest(BaseModel):
    template_id: str = Field(..., title="範本影像編號", example="13520220930134411")

class CreateTemplateResponse(BaseModel):
    template_id: str = Field(..., title="範本影像編號", example="13520220930134411")
