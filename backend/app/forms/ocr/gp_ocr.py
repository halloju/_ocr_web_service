from typing import List
from urllib import request
from app.schema.ocr.gp_ocr import GpocrRequest


class GpocrForm:
    def __init__(self, request: GpocrRequest):
        self.request: GpocrRequest = request
        self.errors: List = []

    async def load_data(self):
        self.image = self.request.image
        self.image_complexity = self.request.image_complexity
        self.model_name = self.request.model_name

    async def is_valid(self):
        if not self.image_complexity:
            self.errors.append("image_complexity should be medium or high")
        if not self.errors:
            return True
        return False
