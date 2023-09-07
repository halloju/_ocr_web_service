from typing import List
from app.schema.template_crud.read import GetAvailableTemplatesRequest, GetTemplateDetailRequest


class GetAvailableTemplatesForm:
    def __init__(self, request: GetAvailableTemplatesRequest):
        self.request: GetAvailableTemplatesRequest = request
        self.errors: List = []

    async def load_data(self):
        self.user_id = self.request.user_id

    async def is_valid(self):
        if not self.user_id or not len(self.user_id) == 5:
            self.errors.append("user_id should be 5 chars")
        if not self.errors:
            return True
        return False


class GetTemplateDetailForm:
    def __init__(self, request: GetTemplateDetailRequest):
        self.request: GetTemplateDetailRequest = request
        self.errors: List = []

    async def load_data(self):
        self.template_id = self.request.template_id

    async def is_valid(self):
        if not self.template_id or not len(self.template_id) == 19:
            self.errors.append("template_id should be 19 chars")
        if not self.errors:
            return True
        return False
