from logging import Logger
from fastapi import APIRouter, File, Form, Request, UploadFile, Depends
from pydantic.typing import List
from fastapi.responses import JSONResponse
from route_utils import get_redis
from aioredis import Redis
import uuid

from app.service.prediction_strategy import CVOcrPredictionStrategy, PredictionAPI
from app.service.prediction_service import CVOcrPredictionService
from app.service.image_storage import ImageStorage
from app.models.task import Task


router = APIRouter()



def get_logger() -> Logger:
    return Logger('async_ocr')


async def get_cv_ocr_prediction_service(
    redis: Redis = Depends(get_redis),
    logger=Depends(get_logger)
) -> CVOcrPredictionStrategy:
    image_storage = ImageStorage(conn=redis)
    cv_ocr_strategy = CVOcrPredictionStrategy(logger=logger)
    prediction_api = PredictionAPI(strategy=cv_ocr_strategy, logger=logger)
    request_id = "some_unique_request_id"
    return CVOcrPredictionService(image_storage, prediction_api, redis, logger, request_id)



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


# @router.post("/cv-ocr", summary="controller 辨識")
# async def cv_upload(
#     image_class: str = Form(...),
#     files: List[UploadFile] = File(...),
#     request_handler: RequestHandler = Depends(),
#     redis: Redis = Depends(get_redis)
# ):
#     '''
#     Call cv_controller api
#     '''
#     logger = request_handler.prediction_service.logger
#     logger.info({'cv-ocr': {'upload_file_num': len(files), 'image_class': image_class}})

#     tasks = await request_handler.handle_cv_ocr(image_class, files)
#     return JSONResponse(status_code=200, content=tasks)


@router.post("/cv-ocr", summary="controller 辨識")
async def cv_upload(
    request: Request,
    image_class: str = Form(...),
    files: List[UploadFile] = File(...),
    prediction_service: CVOcrPredictionService = Depends(
        get_cv_ocr_prediction_service),
    logger=Depends(get_logger)
):
    '''
    Call cv_controller api
    '''
    logger.error(
        {'cv-ocr': {'upload_file_num': len(files), 'image_class': image_class}})
    tasks = []
    action = 'cv-ocr'
    input_params = {'image_class': image_class}

    try:
        for file in files:
            try:
                task = Task(image_id=str(uuid.uuid4()),
                            file_name=file.filename)
                updated_task = await prediction_service.predict_for_task(file, task, action, input_params)
                tasks.append(updated_task.to_dict())
            except Exception as ex:
                logger.error({'error_msg': str(ex), 'action': action})
                task_id = task.task_id if task else ''
                image_id = task.image_id if task else ''
                logger.error(
                    {'task_id': task_id, 'image_id': image_id, 'error_msg': str(ex)})
                tasks.append({'task_id': task_id, 'status': 'ERROR',
                             'url_result': f'/ocr/result/{task_id}'})
        return JSONResponse(status_code=200, content=tasks)
    except Exception as ex:
        logger.error({'error_msg': str(ex), 'action': action})
        return JSONResponse(status_code=400, content=[])


@router.post("/gp_ocr", summary="全文辨識")
async def process(request: Request, image_complexity: str = Form(...), filters: List[str] = Form(...), files: List[UploadFile] = File(...), redis: Redis = Depends(get_redis)):
    tasks = []
    action = 'gp-ocr'
    logger = request.state.logger
    logger.info({action: {'upload_file_num': len(
        files), 'image_complexity': image_complexity, 'filters': filters}})
    prediction_service = PredictionService(
        redis_pool=redis, logger=logger, request_id=request.state.request_id)
    try:
        for file in files:
            try:
                task = await prediction_service.predict_for_task(request, file, action=action, input_params={'image_complexity': image_complexity, 'filters': filters})
                tasks.append(task.to_dict())
            except Exception as ex:
                task_id = task.task_id
                image_id = task.image_id
                logger.error(
                    {'task_id': task_id, 'image_id': image_id, 'error_msg': str(ex)})
                tasks.append({'task_id': task_id, 'status': 'FAIL',
                             'url_result': f'/ocr/result/{task_id}'})
        return JSONResponse(status_code=202, content=tasks)
    except Exception as ex:
        logger.error({'error_msg': str(ex)})
        return JSONResponse(status_code=400, content=[])
