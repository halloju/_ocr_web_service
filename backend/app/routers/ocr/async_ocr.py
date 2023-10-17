from fastapi import APIRouter, File, Form, Request, UploadFile, Depends
from pydantic.typing import List
from app.service.ocr.async_ocr_task import AsyncPredictTask
from fastapi.responses import JSONResponse
from route_utils import get_redis
from aioredis import Redis
import uuid

from app.service.prediction_service import PredictionService
from app.models.task import Task

router = APIRouter()


# @router.post("/cv-ocr", summary="controller 辨識")  # responses={},
# async def cv_upload(request: Request, image_class: str = Form(...), files: List[UploadFile] = File(...), redis: Redis = Depends(get_redis)):
#     '''
#     call cv_controller api
#     '''
#     async_worker = AsyncPredictTask(redis_pool=redis, request=request)
#     tasks = []
#     action = 'cv-ocr'
#     logger = request.state.logger
#     logger.info(
#         {action: {'upload_file_num': len(files), 'image_class': image_class}})
#     try:
#         for file in files:
#             try:
#                 task = await async_worker.process_image(file, action=action, input_params={'image_class': image_class})
#                 tasks.append(task)
#             except Exception as ex:
#                 logger.error({'error_msg': str(ex)})
#                 task_id = task.get('task_id', '')
#                 image_id = task.get('image_id', '')
#                 logger.error(
#                     {'task_id': task_id, 'image_id': image_id, 'error_msg': str(ex)})
#                 tasks.append({'task_id': task_id, 'status': 'ERROR',
#                              'url_result': f'/ocr/result/{task_id}'})
#         return JSONResponse(status_code=200, content=tasks)
#     except Exception as ex:
#         logger.error({'error_msg': str(ex)})
#         return JSONResponse(status_code=400, content=[])


@router.post("/cv-ocr", summary="controller 辨識")
async def cv_upload(
    request: Request,
    image_class: str = Form(...),
    files: List[UploadFile] = File(...),
    redis: Redis = Depends(get_redis)
):
    '''
    call cv_controller api
    '''
    logger = request.state.logger
    action = 'cv-ocr'
    logger.info(
        {action: {'upload_file_num': len(files), 'image_class': image_class}}
    )

    prediction_service = PredictionService(
        redis_pool=redis, logger=logger, request_id=request.state.request_id)
    tasks = []

    try:
        for file in files:
            task = Task(image_id=str(uuid.uuid4()), file_name=file.filename)
            try:
                # Use the prediction service to predict for the task
                updated_task = await prediction_service.predict_for_task(file, task, action, {'image_class': image_class})
                logger.info(
                    updated_task.to_dict()
                )
                tasks.append(updated_task.to_dict())

            except Exception as ex:
                task_id = task.task_id
                image_id = task.image_id
                logger.error(
                    {'task_id': task_id, 'image_id': image_id, 'error_msg': str(ex)})
                tasks.append({'task_id': task_id, 'status': 'ERROR',
                             'url_result': f'/ocr/result/{task_id}'})
        return JSONResponse(status_code=200, content=tasks)

    except Exception as ex:
        logger.error({'error_msg': str(ex)})
        return JSONResponse(status_code=400, content=[])
