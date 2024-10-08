from typing import Type

from fastapi import APIRouter, File, Form, UploadFile, Depends
from pydantic.typing import List
from fastapi.responses import JSONResponse
from aioredis import Redis
import uuid
import asyncio
import os

from app.service.prediction_strategy import CVOcrPredictionStrategy, GPOcrPredictionStrategy, TemplateOcrPredictionStrategy, PredictionAPI
from app.service.prediction_service import ControllerOcrPredictionService
from app.service.image_storage import ImageStorage
from app.exceptions import TaskProcessingException
from app.exceptions import PredictionAPIException
from app.exceptions import GeneralException
from route_utils import get_current_user
from app.models.user import User
from utils.logger import Logger
from route_utils import get_redis


router = APIRouter(dependencies=[Depends(get_current_user)])
logger = Logger('async_ocr')
batch_size = os.environ.get("batch_size", 5)

async def get_cv_ocr_prediction_service(
    logger: Logger,
    request_id: str,
    redis: Redis
) -> ControllerOcrPredictionService:
    image_storage = ImageStorage(conn=redis)
    cv_ocr_strategy = CVOcrPredictionStrategy(logger=logger)
    prediction_api = PredictionAPI(strategy=cv_ocr_strategy, logger=logger)
    return ControllerOcrPredictionService(image_storage, prediction_api, redis, logger, request_id)


async def get_gp_ocr_prediction_service(
    logger: Logger,
    request_id: str,
    redis: Redis
) -> ControllerOcrPredictionService:
    image_storage = ImageStorage(conn=redis)
    gp_ocr_strategy = GPOcrPredictionStrategy(logger=logger)
    prediction_api = PredictionAPI(strategy=gp_ocr_strategy, logger=logger)
    return ControllerOcrPredictionService(image_storage, prediction_api, redis, logger, request_id)


async def get_template_ocr_prediction_service(
    logger: Logger,
    request_id: str,
    redis: Redis
) -> ControllerOcrPredictionService:
    image_storage = ImageStorage(conn=redis)
    gp_ocr_strategy = TemplateOcrPredictionStrategy(logger=logger)
    prediction_api = PredictionAPI(strategy=gp_ocr_strategy, logger=logger)
    return ControllerOcrPredictionService(image_storage, prediction_api, redis, logger, request_id)


def process_results(results, image_class):
    response_content = []
    for result in results:
        if isinstance(result, Exception):
            logger.error({image_class: str(result)})
            response_content.append({"error": str(result)})
        else:
            response_content.extend([task.to_dict() for task in result])  # Flatten list of tasks
    return response_content


@router.post("/cv-ocr", summary="cv controller 辨識")
async def cv_upload(
    image_class: str = Form(...),
    files: List[UploadFile] = File(...),
    redis: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user)
):
    '''
    Call cv_controller api
    '''
    rid = str(uuid.uuid4())
    logger.logger.extra['request_id'] = rid
    logger.logger.extra['user_id'] = current_user.user_id
    prediction_service = await get_cv_ocr_prediction_service(logger, rid, redis)

    tasks = []
    action = 'ocr/upload'
    input_params = {'image_class': image_class}

    try:
        for i in range(0, len(files), batch_size):
            batch = files[i:i + batch_size]
            batch_tasks = [prediction_service.predict_for_task(file, action, input_params) for file in batch]
            results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            tasks.extend(process_results(results,  image_class))

        return JSONResponse(status_code=200, content=tasks)
    except Exception as ex:
        logger.error({'error_msg': str(ex), 'action': action, 'request_id': rid})
        return JSONResponse(status_code=400, content=[])


@router.post("/gp_ocr", summary="gp controller 辨識")
async def gp_upload(
    filters: List[str] = Form(...),
    files: List[UploadFile] = File(...),
    redis: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user),
):
    '''
    call gpocr
    '''
    rid = str(uuid.uuid4())
    logger.logger.extra['request_id'] = rid
    logger.logger.extra['user_id'] = current_user.user_id
    prediction_service = await get_gp_ocr_prediction_service(logger, rid, redis)

    tasks = []
    action = 'ocr/gp_ocr'
    input_params = {'filters': filters}

    try:
        for i in range(0, len(files), batch_size):
            batch = files[i:i + batch_size]
            batch_tasks = [prediction_service.predict_for_task(file, action, input_params) for file in batch]
            results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            tasks.extend(process_results(results, 'gp_ocr'))

        return JSONResponse(status_code=200, content=tasks)
    except Exception as ex:
        logger.error({'error_msg': str(ex), 'action': action, 'request_id': rid})
        return JSONResponse(status_code=400, content=[])


@router.post("/template_ocr", summary="controller 辨識")
async def template_upload(
    template_id: str = Form(...),
    files: List[UploadFile] = File(...),
    redis: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user),
):
    '''
    Call template_ocr api
    '''
    rid = str(uuid.uuid4())
    logger.logger.extra['request_id'] = rid
    logger.logger.extra['user_id'] = current_user.user_id
    prediction_service = await get_template_ocr_prediction_service(logger, rid, redis)

    tasks = []
    action = 'ocr/template_ocr'
    input_params = {'template_id': template_id}
    
    try:
        for i in range(0, len(files), batch_size):
            batch = files[i:i + batch_size]
            batch_tasks = [prediction_service.predict_for_task(file, action, input_params) for file in batch]
            results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            tasks.extend(process_results(results, 'template_ocr'))

        return JSONResponse(status_code=200, content=tasks)
    except Exception as ex:
        logger.error({'error_msg': str(ex), 'action': action})
        return JSONResponse(status_code=400, content=[])
