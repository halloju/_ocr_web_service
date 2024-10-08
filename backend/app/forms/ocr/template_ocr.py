from typing import List
from app.schema.ocr.template_ocr import TemplateocrRequest


class TemplateocrForm:
    def __init__(self, request: TemplateocrRequest):
        self.request: TemplateocrRequest = request
        self.errors: List = []

    async def load_data(self):
        self.image = self.request.image
        self.template_id = self.request.template_id
        self.model_name = self.request.model_name

    async def is_valid(self):
        if not self.template_id:
            self.errors.append("there is no template_id")
        if not self.model_name:
            self.errors.append("there is no model_name")
        if not self.errors:
            return True
        return False
