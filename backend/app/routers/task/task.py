import json
import time

from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from aioredis import Redis

from route_utils import get_redis_taskname
from route_utils import get_current_user
from utils.logger import Logger
from route_utils import get_redis, get_minio

router = APIRouter(dependencies=[Depends(get_current_user)])
logger = Logger('task')


@router.get("/get_image/{image_cv_id}", summary="拉圖片")
async def get_images(image_cv_id: str, redis: Redis = Depends(get_redis), minio_storage=Depends(get_minio)):
    # Check if the image is in Redis cache
    image_string = await redis.get(image_cv_id)
    if image_string:
        return JSONResponse(status_code=200, content=image_string)

    # If image is not in Redis cache, get it from Minio
    image = minio_storage.load_image(image_cv_id)
    if image:
        # Store the image in Redis cache
        await redis.set(image_cv_id, image)
        return JSONResponse(status_code=200, content=image)
    else:
        return JSONResponse(status_code=404, content={'message': 'Image not found'})



@router.get('/result/{task_id}')
async def result(task_id: str, redis: Redis = Depends(get_redis)):
    result = await redis.hgetall(get_redis_taskname(task_id))
    return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': result['status'], 'result': json.loads(result['result']), 'file_name': result['file_name']})


@router.get('/status/{task_id}')
async def status(task_id: str, redis: Redis = Depends(get_redis)):
    # Define maximum retries and backoff factor
    max_retries = 5
    backoff_factor = 0.1  # 100ms

    for retry in range(max_retries):
        # Fetch task status from Redis Hash
        result = await redis.hgetall(get_redis_taskname(task_id))
        if not result:
            return JSONResponse(status_code=200, content={'task_id': task_id, 'status': 'ERROR', 'result': '', 'status_msg': 'No such Task', 'file_name': ''})

        status = result.get('status')
        status_msg = result.get('status_msg', '')
        file_name = result.get('file_name', '')
        # If task is complete, return the result
        if status in ['SUCCESS', 'FAIL']:
            return JSONResponse(status_code=200, content={'task_id': task_id, 'status': status, 'result': '', 'status_msg': status_msg, 'file_name': file_name})

        # Wait for a short period before retrying
        time.sleep(backoff_factor * (2 ** retry))

    # If maximum retries reached, return PENDING status
    return JSONResponse(status_code=200, content={'task_id': task_id, 'status': 'PROCESSING', 'result': '', 'status_msg': '', 'file_name': file_name})
