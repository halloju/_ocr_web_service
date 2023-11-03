import json
import time

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
    redis_client = request.app.state.redis
    result = []  # await redis_client.hgetall(get_redis_taskname(task_id))
    if ('file_name' in result and 'result' in result):
        return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': result['status'], 'result': json.loads(result['result']), 'file_name': result['file_name']})
    else:
        # return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': result['status']})
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
    redis_client = request.app.state.redis
    # logger = request.state.logger
    # # Define maximum retries and backoff factor
    # max_retries = 5
    # backoff_factor = 0.1  # 100ms

    # for retry in range(max_retries):
    #     # Fetch task status from Redis Hash
    #     result = await redis_client.hgetall(get_redis_taskname(task_id))
    #     if result:
    #         status = result.get('status')
    #         status_msg = result.get('status_msg', '')
    #         file_name = result.get('file_name', '')

    #         # If task is complete, return the result
    #         if status in ['SUCCESS', 'FAILURE']:
    #             return JSONResponse(status_code=200, content={'task_id': task_id, 'status': status, 'result': '', 'status_msg': status_msg, 'file_name': file_name})

    #     # Wait for a short period before retrying
    #     time.sleep(backoff_factor * (2 ** retry))

    # If maximum retries reached, return PENDING status
    return JSONResponse(status_code=200, content={'task_id': task_id, 'status': 'SUCCESS', 'result': '', 'status_msg': '', 'file_name': ''})
