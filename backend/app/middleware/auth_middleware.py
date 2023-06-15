# auth_middleware.py
import jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import os
from fastapi import HTTPException, status
import fnmatch

SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app
    ):
        super().__init__(app)
    async def dispatch(self, request: Request, call_next):
        if fnmatch.fnmatch(request.url.path, "/auth/*"):
            # Continue processing without verifying token
            request.state.user_id = 'auth'
            response = await call_next(request)
            return response
        # Extract the token from the headers
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        # Decode the token and extract user ID
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            uid = payload.get("sub")
            if uid is None:
              raise credentials_exception
            request.state.user_id = uid
        except jwt.PyJWTError:
            raise credentials_exception
        except Exception as e:
            print('AuthMiddleware error', e)
            raise e

        # Continue processing
        response = await call_next(request)
        return response
