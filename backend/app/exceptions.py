from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

import traceback

class CustomException(HTTPException):
    def __init__(self, status_code: int = 400, message: str = "") -> None:
        super().__init__(status_code=status_code)
        self.message = message


class ImageTypeError(Exception):
    """Image type validate error """


class MlaasRequestError(HTTPException):
    """mlaas request error """

    def __init__(self, status_code: str = '0001', status_msg: str = "", image_cv_id: str = "") -> None:
        super().__init__(status_code=500)  # internal error
        self.message = status_msg
        self.mlaas_code = status_code
        self.image_cv_id = image_cv_id


class TaskProcessingException(Exception):
    def __init__(self, task, message="Task processing failed"):
        self.task = task
        self.message = f"{message}: Filename {task.file_name}"
        super().__init__(self.message)


class PredictionAPIException(Exception):
    def __init__(self, task, original_exception, message="Prediction API error"):
        self.task = task
        self.original_exception = original_exception
        self.message = f"{message}: {str(original_exception)} for File: {task.file_name}"
        super().__init__(self.message)


class GeneralException(Exception):
    def __init__(self, task, original_exception, message="An error occurred"):
        self.task = task
        self.original_exception = original_exception
        self.message = f"{message}: {str(original_exception)} for File: {task.file_name}"
        super().__init__(self.message)


def exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code, content={
            "error": True, "msg": exc.message}
    )


def mlaas_request_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code, content={
            "mlaas_code": exc.mlaas_code, "msg": exc.message, "image_cv_id": exc.image_cv_id}
    )
