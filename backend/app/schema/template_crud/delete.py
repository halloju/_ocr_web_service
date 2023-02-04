from pydantic import BaseModel, Field
from datetime import datetime


class DeleteTemplateRequest(BaseModel):
    template_id: str = Field(..., title="範本影像編號", example="1352020220930134411")
