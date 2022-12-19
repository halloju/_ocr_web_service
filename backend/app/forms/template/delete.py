from typing import List
from typing import Optional
from urllib import request
from app.schema.template import DeleteTemplateRequest


class DeleteTemplateForm:
    def __init__(self, request: DeleteTemplateRequest):
        self.request: DeleteTemplateRequest = request
        self.errors: List = []

    async def load_data(self):
        self.template_id = self.request.template_id

    async def is_valid(self):
        if not self.template_id or not len(self.template_id) == 19:
            self.errors.append("template_id should be 19 chars")
        if not self.errors:
            return True
        return False
