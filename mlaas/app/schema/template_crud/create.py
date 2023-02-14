import os
from typing import List
from pydantic import BaseModel, Field


filepath = os.path.join(os.getcwd(), "app", "image-base64-string.txt")
with open(filepath, 'r') as f:
    img_base64_string = f.read()


class CreateTemplateRequest(BaseModel):
    user_id: str = Field(..., title="員編", example="13520")
    image: str = Field(..., title='範本影像', example=img_base64_string)
    bbox: List = Field(..., title='使用者拉框留存的範本資訊', example=[{'type': 'text', 'tag': '姓名', 'x_min': 0, 'y_min': 0, 'x_max': 100, 'y_max': 100}, {'type': 'box', 'tag': '是否為範本', 'x_min': 130, 'y_min': 200, 'x_max': 200, 'y_max': 270}, {'type': 'mask', 'tag': None, 'x_min': 0, 'y_min': 0, 'x_max': 100, 'y_max': 100}])
    template_name: str = Field(..., title='範本名稱', example='身分證')
    is_public: bool = Field(False, title='是否為公用模板 (僅 admin 可用)', example=False)
    is_no_ttl: bool = Field(False, title='是否永久保存 (僅 admin 可用)', example=False)

class CreateTemplateResponse(BaseModel):
    template_id: str = Field(..., title="範本影像編號", example="1352020220930134411")

