from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class CustomException(HTTPException):
    def __init__(self, status_code: int = 400, message: str = "") -> None:
        super().__init__(status_code=status_code)
        self.message = message


class ImageTypeError(Exception):
    """Image type validate error """
    pass


def exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code, content={
            "error": True, "msg": exc.message}
    )
