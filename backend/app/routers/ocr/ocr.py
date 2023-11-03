import base64
import uuid

from app.service.image_storage import ImageStorage

from app.service.prediction_strategy import NonControllerOcrPredictionStrategy, PredictionAPI
from app.service.prediction_service import NonControllerOcrPredictionService
from route_utils import get_redis
from logging import Logger
from route_utils import get_redis_filename

from fastapi import APIRouter, File, Request, UploadFile, Depends
from fastapi.responses import JSONResponse
from pydantic.typing import List
from worker import predict_image
from datetime import datetime
from aioredis import Redis


router = APIRouter()


def get_logger() -> Logger:
    return Logger('sync_ocr')

async def get_ocr_prediction_service(
    redis: Redis = Depends(get_redis),
    logger=Depends(get_logger)
) -> NonControllerOcrPredictionService:
    image_storage = ImageStorage(conn=redis)
    gp_ocr_strategy = NonControllerOcrPredictionStrategy(logger=logger)
    prediction_api = PredictionAPI(strategy=gp_ocr_strategy, logger=logger)
    request_id = str(uuid.uuid4())
    return NonControllerOcrPredictionService(image_storage, prediction_api, redis, logger, request_id)


@router.post("/remittance", summary="匯款單辨識")
async def remittance(
    files: List[UploadFile] = File(...),
    prediction_service: NonControllerOcrPredictionService = Depends(
        get_ocr_prediction_service),
    logger=Depends(get_logger)
):
    '''
    Call remittance api
    '''
    tasks = []
    action = 'ocr/predict'
    input_params = {}
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


@router.post("/check_front", summary="支票正面辨識")
async def check_front(
    files: List[UploadFile] = File(...),
    prediction_service: NonControllerOcrPredictionService = Depends(
        get_ocr_prediction_service),
    logger=Depends(get_logger)
):
    tasks = []
    action = 'ocr/front_out_predict'
    input_params = {}
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


@router.post("/check_back", summary="支票背面辨識")
async def check_back(
    files: List[UploadFile] = File(...),
    prediction_service: NonControllerOcrPredictionService = Depends(
        get_ocr_prediction_service),
    logger=Depends(get_logger)
):
    tasks = []
    action = 'ocr/back_predict'
    input_params = {}
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
