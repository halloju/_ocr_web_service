from fastapi import APIRouter, File, Form, Request, UploadFile
from pydantic.typing import List
from logger import Logger
from app.utils.ocr_utils import AsynPredictTask
from fastapi.responses import JSONResponse

import base64
import uuid

router = APIRouter()
logger = Logger(__name__)
Asyn_worker = AsynPredictTask(logger)

async def process_image(request: Request, file: UploadFile, action: str, input_params: dict):
    image_id = str(uuid.uuid4())

    # Read and encode the file data as base64
    image_data = await file.read()
    encoded_data = base64.b64encode(image_data).decode("utf-8")

    # Store the encoded image data in Redis using the image ID as the key
    await Asyn_worker.conn.set(image_id, encoded_data, ex=86400)

    # Store the file name in Redis using the image ID as the key
    await Asyn_worker.conn.set(image_id + '_file_name', file.filename, ex=86400)
    # start task prediction
    #  {'status': status, 'predict_class': predict_class, 'file_name': file_name, 'image_cv_id': image_cv_id}
    upload_result = await Asyn_worker.predict_image(image_id, action=action, input_params=input_params)
    return {'task_id': str(upload_result["image_cv_id"]), 'status': 'PROCESSING', 'url_result': f'/ocr/result/{upload_result["image_cv_id"]}', 'image_id': image_id}


@router.post("/cv_ocr", summary="controller 辨識")  # responses={},
async def cv_upload(request: Request, image_class: str, files: List[UploadFile] = File(...)):
    '''
    call cv_controller api
    '''
    tasks = []
    action = 'cv_ocr'
    logger.info({action: {'upload_file_num': len(files), 'image_class': image_class}})
    try:
        for file in files:
            try:
                task = await process_image(request, file, action=action, input_params={'image_class': image_class})
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

