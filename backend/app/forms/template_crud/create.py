from typing import List
from app.schema.template_crud.create import CreateTemplateRequest


class CreateTemplateForm:
    def __init__(self, request: CreateTemplateRequest):
        self.request: CreateTemplateRequest = request
        self.errors: List = []

    async def load_data(self):
        self.image = self.request.image
        self.points_list = self.request.points_list
        self.template_name = self.request.template_name

    async def is_valid(self):
        if not self.errors:
            return True
        return False
