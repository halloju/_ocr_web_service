from typing import Any

from pydantic import BaseModel, Field


class Response(BaseModel):
    error: bool = Field(False, title="是否錯誤")
    data: Any = Field(None, title="回傳內容")
