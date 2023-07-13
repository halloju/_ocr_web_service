# auth_middleware.py
import fnmatch
import os

import jwt
from fastapi import HTTPException, status
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # List of paths that should bypass authentication
        bypass_auth_paths = ["/docs", "/docs/oauth2-redirect", "/redoc", "/openapi.json", "/auth", "/static"]

        # Check if the requested path starts with any of the paths in the bypass_auth_paths list
        if any(request.url.path.startswith(path) for path in bypass_auth_paths):
            request.state.user_id = 'nan'
            return await call_next(request)

        # Extract the token from the headers
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        # Decode the token and extract user ID
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            uid = payload.get("sub")
            if uid is None:
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Could not validate credentials"})
            request.state.user_id = uid
        except jwt.PyJWTError:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Could not validate credentials"})
        except Exception as e:
            print('AuthMiddleware error', e)
            raise HTTPException(status_code=500, detail="Internal server error")

        # Continue processing
        response = await call_next(request)
        return response
