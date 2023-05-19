import base64
import uuid

from celery.result import AsyncResult
from fastapi import APIRouter, File, Form, Request, UploadFile, Depends
from fastapi.responses import JSONResponse
from logger import Logger
from pydantic.typing import List
from worker import predict_image
from route_utils import verify_token


router = APIRouter()
logger = Logger(__name__)

async def process_image(request: Request, file: UploadFile, action: str, input_params: dict):
    image_id = str(uuid.uuid4())
    task_id = ''

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
    task_id = predict_image.delay(image_id, action=action, input_params=input_params)
    return {'task_id': str(task_id), 'status': 'PROCESSING', 'url_result': f'/ocr/result/{task_id}', 'image_id': image_id}

@router.post("/gp_ocr", summary="全文辨識", dependencies=[Depends(verify_token)])
async def process(request: Request, image_complexity: str = Form(...), model_name: str = Form(...), files: List[UploadFile] = File(...)):
    tasks = []
    action = 'gp_ocr'
    logger.info({action: {'upload_file_num': len(files), 'image_complexity': image_complexity, 'model_name': model_name}})
    try:
        for file in files:
            try:
                task = await process_image(request, file, action=action, input_params={'image_complexity': image_complexity, 'model_name': model_name})
                tasks.append(task)
            except Exception as ex:
                task_id = task.get('task_id', '')
                image_id = task.get('image_id', '')
                logger.error({'task_id': task_id, 'image_id': image_id, 'error_msg': str(ex)})
                tasks.append({'task_id': task_id, 'status': 'ERROR', 'url_result': f'/ocr/result/{task_id}'})
        return JSONResponse(status_code=202, content=tasks)
    except Exception as ex:
        logger.error({'error_msg': str(ex)})
        return JSONResponse(status_code=400, content=[])

@router.post("/template_ocr", summary="模板辨識", dependencies=[Depends(verify_token)])
async def process(request: Request, model_name: str = Form(...), template_id: str = Form(...), files: List[UploadFile] = File(...)):
    tasks = []
    action = 'template_ocr'
    logger.info({action: {'upload_file_num': len(files), 'template_id': template_id, 'model_name': model_name}})
    try:
        for file in files:
            try:
                task = await process_image(request, file, action=action, input_params={'model_name': model_name, 'template_id': template_id})
                tasks.append(task)
            except Exception as ex:
                task_id = task.get('task_id', '')
                image_id = task.get('image_id', '')
                logger.error({'task_id': task_id, 'image_id': image_id, 'error_msg': str(ex)})
                tasks.append({'task_id': str(task_id), 'status': 'ERROR', 'url_result': f'/ocr/result/{task_id}'})
        return JSONResponse(status_code=202, content=tasks)
    except Exception as ex:
        logger.error({'error_msg': str(ex)})
        return JSONResponse(status_code=400, content=[])

@router.post("/remittance", summary="匯款單辨識", dependencies=[Depends(verify_token)])
async def process(request: Request, files: List[UploadFile] = File(...)):
    tasks = []
    action = 'remittance'
    logger.info({action: {'upload_file_num': len(files)}})
    try:
        for file in files:
            try:
                task = await process_image(request, file, action=action, input_params={})
                tasks.append(task)
            except Exception as ex:
                task_id = task.get('task_id', '')
                image_id = task.get('image_id', '')
                logger.error({'task_id': task_id, 'image_id': image_id, 'error_msg': str(ex)})
                tasks.append({'task_id': str(task_id), 'status': 'ERROR', 'url_result': f'/ocr/result/{task_id}'})
        return JSONResponse(status_code=202, content=tasks)
    except Exception as ex:
        logger.error({'error_msg': str(ex)})
        return JSONResponse(status_code=400, content=[])

@router.post("/check_front", summary="支票正面辨識", dependencies=[Depends(verify_token)])
async def process(request: Request, files: List[UploadFile] = File(...)):
    tasks = []
    action = 'check_front'
    logger.info({action: {'upload_file_num': len(files)}})
    try:
        for file in files:
            try:
                task = await process_image(request, file, action=action, input_params={})
                tasks.append(task)
            except Exception as ex:
                task_id = task.get('task_id', '')
                image_id = task.get('image_id', '')
                logger.error({'task_id': task_id, 'image_id': image_id, 'error_msg': str(ex)})
                tasks.append({'task_id': str(task_id), 'status': 'ERROR', 'url_result': f'/ocr/result/{task_id}'})
        return JSONResponse(status_code=202, content=tasks)
    except Exception as ex:
        logger.error({'error_msg': str(ex)})
        return JSONResponse(status_code=400, content=[])

@router.post("/check_back", summary="支票背面辨識", dependencies=[Depends(verify_token)])
async def process(request: Request, files: List[UploadFile] = File(...)):
    tasks = []
    action = 'check_back'
    logger.info({action: {'upload_file_num': len(files)}})
    try:
        for file in files:
            try:
                task = await process_image(request, file, action=action, input_params={})
                tasks.append(task)
            except Exception as ex:
                task_id = task.get('task_id', '')
                image_id = task.get('image_id', '')
                logger.error({'task_id': task_id, 'image_id': image_id, 'error_msg': str(ex)})
                tasks.append({'task_id': str(task_id), 'status': 'ERROR', 'url_result': f'/ocr/result/{task_id}'})
        return JSONResponse(status_code=202, content=tasks)
    except Exception as ex:
        logger.error({'error_msg': str(ex)})
        return JSONResponse(status_code=400, content=[])