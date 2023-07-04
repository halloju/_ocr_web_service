from datetime import datetime

from app.logger.logger import Logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


def get_request_id() -> str:  # celery with task_id
    return datetime.now().strftime("%Y/%m/%d/%H/%M/%S/") + 'gpocr_system_test'

class LogMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app
    ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        bypass_auth_paths = ["/docs", "/docs/oauth2-redirect", "/redoc", "/openapi.json", "/auth/is_authenticated", "/auth/refresh_token"]
        if any(request.url.path.startswith(path) for path in bypass_auth_paths):
            return await call_next(request)
        uid = request.state.user_id
        # uid = getattr(request.state, "user_id", None)
        rid = get_request_id()
        request.state.request_id = rid
        request.state.logger = Logger(__name__, uid, rid)
        # Log before processing
        request.state.logger.debug(f"Request {request.method} {request.url} received")

        # Call the next middleware or route handler
        response = await call_next(request)

        # Log after processing
        request.state.logger.debug(f"Response status: {response.status_code}")

        # Return the response
        return response
