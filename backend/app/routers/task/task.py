import json

from celery.result import AsyncResult
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from route_utils import get_redis_taskname
from starlette.requests import Request

router = APIRouter()

@router.get("/get_image/{image_id}", summary="拉圖片")
async def get_images(image_id: str, request: Request):
    # Get the Redis connection from the app state
    redis = request.app.state.redis
    image_string = await redis.get(image_id)
    return JSONResponse(status_code=200, content=image_string)

@router.get('/result/{task_id}')
async def result(task_id: str, request: Request):
    logger = request.state.logger
    redis = request.app.state.redis
    result = await redis.get(get_redis_taskname(task_id))
    if (result):
        result = json.loads(result)
        if ('file_name' in result and 'result' in result): 
            return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': result['status'], 'result': result['result'], 'file_name': result['file_name']})

    task = AsyncResult(task_id)
    # Task Not Ready
    if not task.ready():
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': task.status, 'result': '', 'status_msg': ''})

    task_result = task.get()
    if task_result is None:
        return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': 'FAIL', 'status_msg': '', 'result': 'Task result is None'})
    # Task done: return the value
    result = task_result.get('result')
    logger.debug(f"result: {result}")
    return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': task_result.get('status'), 'result': result, 'file_name': task_result.get('file_name'), 'status_msg': task_result.get('status_msg')})

@router.get('/status/{task_id}')
async def status(task_id: str, request: Request):
    redis = request.app.state.redis
    result = await redis.get(get_redis_taskname(task_id))
    if (result):
        result = json.loads(result)
        if ('status' in result and 'status_msg' in result):
            return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': result['status'], 'result': '', 'status_msg': result['status_msg'], 'file_name': result['file_name']})
    task = AsyncResult(task_id)
    if (task.status != 'PENDING'):  # 在 pending 應該沒有 result，可能要想一下怎麼改寫 file name 的存法
        task_result = task.get()
        result = task_result.get('result')
        return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': task.status, 'result': result, 'status_msg': task_result.get('status_msg'), 'file_name': task_result.get('file_name')})
    return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': task.status, 'status_msg': '', 'result': ''})
