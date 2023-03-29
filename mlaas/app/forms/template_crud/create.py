from typing import List
from typing import Optional
from urllib import request
from app.schema.template_crud.create import CreateTemplateRequest


class CreateTemplateForm:
    def __init__(self, request: CreateTemplateRequest):
        self.request: CreateTemplateRequest = request
        self.errors: List = []

    async def load_data(self):
        self.user_id = self.request.user_id
        self.image = self.request.image
        self.is_no_ttl = self.request.is_no_ttl
        self.points_list = self.request.points_list
        self.template_name = self.request.template_name
        self.is_public = self.request.is_public

    async def is_valid(self):
        if not self.user_id or not len(self.user_id) == 5:
            self.errors.append("user_id should be 5 chars")
        if not self.errors:
            return True
        return False
