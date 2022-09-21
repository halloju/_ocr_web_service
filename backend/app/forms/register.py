from typing import List
from typing import Optional
from urllib import request
from app.schema.users import RegisterRequest

class UserCreateForm:
    def __init__(self, request: RegisterRequest):
        self.request: RegisterRequest = request
        self.errors: List = []
    
    async def load_data(self):
        self.account = self.request.account
        self.name = self.request.name
        self.birthday = self.request.birthday
        self.password = self.request.password
    
    async def is_valid(self):
        if not self.account or not len(self.account) == 8:
            self.errors.append("Username should be 8 chars")
        if not self.name:
            self.errors.append("Name should not be empty")
        if not self.birthday or not len(self.birthday) == 8:
            self.errors.append("birthday should be 8 chars")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("Password must be >= 4 chars")
        if not self.errors:
            return True
        return False
