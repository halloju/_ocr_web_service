from logging import Logger
from fastapi import APIRouter, File, Form, Request, UploadFile, Depends
from pydantic.typing import List
from fastapi.responses import JSONResponse
from route_utils import get_redis
from aioredis import Redis
import uuid

from app.service.prediction_strategy import CVOcrPredictionStrategy, GPOcrPredictionStrategy, PredictionAPI
from app.service.prediction_service import OcrPredictionService
from app.service.image_storage import ImageStorage


router = APIRouter()


def get_logger() -> Logger:
    return Logger('async_ocr')


async def get_cv_ocr_prediction_service(
    redis: Redis = Depends(get_redis),
    logger=Depends(get_logger)
) -> OcrPredictionService:
    image_storage = ImageStorage(conn=redis)
    cv_ocr_strategy = CVOcrPredictionStrategy(logger=logger)
    prediction_api = PredictionAPI(strategy=cv_ocr_strategy, logger=logger)
    request_id = "some_unique_request_id"
    return OcrPredictionService(image_storage, prediction_api, redis, logger, request_id)


async def get_gp_ocr_prediction_service(
    redis: Redis = Depends(get_redis),
    logger=Depends(get_logger)
) -> OcrPredictionService:
    image_storage = ImageStorage(conn=redis)
    gp_ocr_strategy = GPOcrPredictionStrategy(logger=logger)
    prediction_api = PredictionAPI(strategy=gp_ocr_strategy, logger=logger)
    request_id = "some_unique_request_id"
    return OcrPredictionService(image_storage, prediction_api, redis, logger, request_id)


@router.post("/cv-ocr", summary="controller 辨識")
async def cv_upload(
    image_class: str = Form(...),
    files: List[UploadFile] = File(...),
    prediction_service: OcrPredictionService = Depends(
        get_cv_ocr_prediction_service),
    logger=Depends(get_logger)
):
    '''
    Call cv_controller api
    '''
    tasks = []
    action = 'cv-ocr'
    input_params = {'image_class': image_class}

    try:
        for file in files:
            try:
                # task = Task(image_id=str(uuid.uuid4()),
                #             file_name=file.filename)
                updated_task = await prediction_service.predict_for_task(file, action, input_params)
                tasks.append(updated_task.to_dict())
            except Exception as ex:
                logger.error({'error_msg': str(ex), 'action': action})
                tasks.append({'status': 'ERROR', 'error_msg': str(ex)})
        return JSONResponse(status_code=200, content=tasks)
    except Exception as ex:
        logger.error({'error_msg': str(ex), 'action': action})
        return JSONResponse(status_code=400, content=[])


@router.post("/gp_ocr", summary="controller 辨識")
async def gp_upload(
    image_complexity: str = Form(...), 
    filters: List[str] = Form(...), 
    files: List[UploadFile] = File(...),
    prediction_service: OcrPredictionService = Depends(
        get_gp_ocr_prediction_service),
    logger=Depends(get_logger)
):
    '''
    Call cv_controller api
    '''
    tasks = []
    action = 'gp_ocr'
    input_params = {'image_complexity': image_complexity, 'filters': filters}
    
    try:
        for file in files:
            try:

                updated_task = await prediction_service.predict_for_task(file, action, input_params)
                tasks.append(updated_task.to_dict())
            except Exception as ex:
                logger.error({'error_msg': str(ex), 'action': action})
                tasks.append({'status': 'ERROR', 'error_msg': str(ex)})
        return JSONResponse(status_code=200, content=tasks)
    except Exception as ex:
        logger.error({'error_msg': str(ex), 'action': action})
        return JSONResponse(status_code=400, content=[])

