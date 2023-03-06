from pydantic import BaseModel, Field, StrictStr, conlist
from datetime import datetime
from typing import Optional


class DeleteTemplateRequest(BaseModel):
    template_id: str = Field(..., title="範本影像編號", example="1352020220930134411")
