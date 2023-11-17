import logging
import uuid

from app.service.image_storage import ImageStorage

from app.service.prediction_strategy import NonControllerOcrPredictionStrategy, PredictionAPI
from app.service.prediction_service import NonControllerOcrPredictionService
from route_utils import get_redis
from utils.logger import Logger
from route_utils import get_current_user
from app.models.user import User

from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from pydantic.typing import List
from aioredis import Redis


router = APIRouter(dependencies=[Depends(get_current_user)])
logger = Logger('sync_ocr')


async def get_ocr_prediction_service(
    logger: Logger,
    request_id: str,
    redis: Redis
) -> NonControllerOcrPredictionService:
    image_storage = ImageStorage(conn=redis)
    gp_ocr_strategy = NonControllerOcrPredictionStrategy(logger=logger)
    prediction_api = PredictionAPI(strategy=gp_ocr_strategy, logger=logger)
    return NonControllerOcrPredictionService(image_storage, prediction_api, redis, logger, request_id)


@router.post("/remittance", summary="匯款單辨識")
async def remittance(
    files: List[UploadFile] = File(...),
    redis: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user),
):
    '''
    Call remittance api
    '''
    rid = str(uuid.uuid4())
    logger.logger.extra['request_id'] = rid
    logger.logger.extra['user_id'] = current_user.user_id
    prediction_service = await get_ocr_prediction_service(logger, rid, redis)

    tasks = []
    action = 'REMIT/predict'
    input_params = {}
    try:
        for file in files:
            try:
                updated_task = await prediction_service.predict_for_task(file, action, input_params)
                tasks.append(updated_task.to_dict_no_dumps())
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
    redis: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user)
):
    rid = str(uuid.uuid4())
    logger.logger.extra['request_id'] = rid
    logger.logger.extra['user_id'] = current_user.user_id
    prediction_service = await get_ocr_prediction_service(logger, rid, redis)
    
    tasks = []
    action = 'CHECK/front_out_predict'
    input_params = {}
    try:
        for file in files:
            try:
                updated_task = await prediction_service.predict_for_task(file, action, input_params)
                tasks.append(updated_task.to_dict_no_dumps())
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
    redis: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user)
):
    rid = str(uuid.uuid4())
    logger.logger.extra['request_id'] = rid
    logger.logger.extra['user_id'] = current_user.user_id
    prediction_service = await get_ocr_prediction_service(logger, rid, redis)
    
    tasks = []
    action = 'CHECK/back_predict'
    input_params = {}
    try:
        for file in files:
            try:
                updated_task = await prediction_service.predict_for_task(file, action, input_params)
                tasks.append(updated_task.to_dict_no_dumps())
            except Exception as ex:
                logger.error({'error_msg': str(ex), 'action': action})
                tasks.append({'status': 'ERROR', 'error_msg': str(ex)})
        return JSONResponse(status_code=200, content=tasks)
    except Exception as ex:
        logger.error({'error_msg': str(ex), 'action': action})
        return JSONResponse(status_code=400, content=[])
