import base64
import uuid

from celery.result import AsyncResult
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import JSONResponse
from logger import Logger
from pydantic.typing import List
from worker import predict_image

logger = Logger(__name__)

router = APIRouter()

@router.get("/get_image/{image_id}", summary="拉圖片")
async def get_images(image_id: str, request: Request):
    # Get the Redis connection from the app state
    redis = request.app.state.redis
    image_string = await redis.get(image_id)
    return JSONResponse(status_code=200, content=image_string)

@router.post("/predict_images", summary="模板辨識")
async def process(request: Request, model_name: str = Form(...), template_id: str = Form(...), files: List[UploadFile] = File(...)):
    tasks = []
    try:
        for file in files:
            try:
                image_id = str(uuid.uuid4())

                # Read and encode the file data as base64
                image_data = await file.read()
                encoded_data = base64.b64encode(image_data).decode("utf-8")

                # Store the encoded image data in Redis using the image ID as the key
                await request.app.state.redis.set(image_id, encoded_data)
                # Set an expiration time of 1 day (86400 seconds) for the key
                await request.app.state.redis.expire(image_id, 86400)

                # Store the file name in Redis using the image ID as the key
                await request.app.state.redis.set(image_id + '_file_name', file.filename)
                # Set an expiration time of 1 day (86400 seconds) for the key
                await request.app.state.redis.expire(image_id + '_file_name', 86400)

                # start task prediction
                image_complexity = "" # template 的 image_complexity 設定空值
                task_id = predict_image.delay(image_id, action='template_ocr', input_params={'template_id': template_id, 'model_name': model_name})
                tasks.append({'task_id': str(task_id), 'status': 'PROCESSING', 'url_result': f'/ocr/result/{task_id}', 'image_id': image_id})
            except Exception as ex:
                logger.error({'task_id': task_id, 'image_id': image_id, 'error_msg': str(ex)})
                tasks.append({'task_id': str(task_id), 'status': 'ERROR', 'url_result': f'/ocr/result/{task_id}'})
        return JSONResponse(status_code=202, content=tasks)
    except Exception as ex:
        logger.error({'error_msg': str(ex)})
        return JSONResponse(status_code=400, content=[])


@router.get('/result/{task_id}')
async def result(task_id: str):
    task = AsyncResult(task_id)

    # Task Not Ready
    if not task.ready():
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': task.status, 'result': '', 'file_name': ''})

    # Task done: return the value
    task_result = task.get()
    # Task Result is None
    if task_result is None:
        return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': 'FAIL', 'result': 'Task result is None', 'file_name': ''})

    result = task_result.get('result')
    return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': task_result.get('status'), 'result': result, 'file_name': task_result.get('file_name')})


@router.get('/status/{task_id}')
async def status(task_id: str):
    task = AsyncResult(task_id)
    return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': task.status, 'result': '', 'file_name': ''})
