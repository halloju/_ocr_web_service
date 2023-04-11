from typing import Any, Dict, Optional
import os
from pydantic import BaseModel, Field


filepath = os.path.join(os.getcwd(), "app", "image-base64-string.txt")
with open(filepath, 'r') as f:
    img_base64_string = f.read()


class Response(BaseModel):
    error: bool = Field(False, title="是否錯誤")
    data: Any = Field(None, title="回傳內容")
