from typing import List
from app.schema.ocr.gp_ocr import GpocrUpload, GpocrPredict


class GpocrUploadForm:
    def __init__(self, request: GpocrUpload):
        self.request: GpocrUpload = request
        self.errors: List = []

    async def load_data(self):
        self.imageDict = self.request.image
        self.model_name = self.request.model_name

    async def is_valid(self):
        if not self.errors:
            return True
        return False


class GpocrPredictForm:
    def __init__(self, request: GpocrPredict):
        self.request: GpocrPredict = request
        self.errors: List = []

    async def load_data(self):
        self.imageDict = self.request.image
        self.model_name = self.request.model_name

    async def is_valid(self):
        if not self.errors:
            return True
        return False
