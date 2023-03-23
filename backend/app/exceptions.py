from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class CustomException(HTTPException):
    def __init__(self, status_code: int = 400, message: str = "") -> None:
        super().__init__(status_code=status_code)
        self.message = message


class ImageTypeError(Exception):
    """Image type validate error """
    pass

class MlaasRequestError(HTTPException):
    """mlaas request error """
    def __init__(self, status_code: str = '0001', status_msg: str = "") -> None:
        super().__init__(status_code=500)
        self.message = status_msg
        self.mlaas_code = status_code


def exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code, content={"error": True, "msg": exc.message}
    )

def mlaas_request_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code, content={"mlaas_code": exc.mlaas_code, "msg": exc.message}
    )
