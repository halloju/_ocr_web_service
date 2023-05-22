from celery.result import AsyncResult
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from logger import Logger
import json

router = APIRouter()
logger = Logger(__name__)

@router.get("/get_image/{image_id}", summary="拉圖片")
async def get_images(image_id: str, request: Request):
    # Get the Redis connection from the app state
    redis = request.app.state.redis
    image_string = await redis.get(image_id)
    return JSONResponse(status_code=200, content=image_string)

@router.get('/result/{task_id}')
async def result(task_id: str, request: Request):
    redis = request.app.state.redis
    result = await redis.get(task_id)
    if(result):
        result = json.loads(result)
        return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': result['status'], 'result': result['result'], 'file_name': result['file_name']})
    task = AsyncResult(task_id)

    # Task Not Ready
    if not task.ready():
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': task.status, 'result': '', 'file_name': ''})

    task_result = task.get()
    if task_result is None:
        return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': 'FAIL', 'result': 'Task result is None', 'file_name': ''})
    # Task done: return the value
    result = task_result.get('result')
    return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': task_result.get('status'), 'result': result, 'file_name': task_result.get('file_name')})

@router.get('/status/{task_id}')
async def status(task_id: str, request: Request):
    redis = request.app.state.redis
    result = await redis.get(task_id)
    if(result):
        result = json.loads(result)
        return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': result['status'], 'result': '', 'file_name': ''})
    task = AsyncResult(task_id)
    return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': task.status, 'result': '', 'file_name': ''})