from typing import List
from typing import Optional
from urllib import request
from app.schema.template import UpdateTemplateRequest


class UpdateTemplateForm:
    def __init__(self, request: UpdateTemplateRequest):
        self.request: UpdateTemplateRequest = request
        self.errors: List = []

    async def load_data(self):
        self.template_id = self.request.template_id
        self.bbox = self.request.bbox
        self.template_name = self.request.template_name

    async def is_valid(self):
        if not self.template_id or not len(self.template_id) == 19:
            self.errors.append("template_id should be 19 chars")
        if not self.errors:
            return True
        return False
