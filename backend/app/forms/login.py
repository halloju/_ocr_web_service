from typing import List
from typing import Optional

from app.schema.users import LoginRequest


class LoginForm:
    def __init__(self, request: LoginRequest):
        self.request: LoginRequest = request
        self.errors: List = []

    async def load_data(self):
        self.account = self.request.account
        self.password = self.request.password

    async def is_valid(self):
        if not self.account or not len(self.account) == 8:
            self.errors.append("Username should be 8 chars")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("Password must be >= 4 chars")
        if not self.errors:
            return True
        return False