from fastapi import APIRouter, File, Form, Request, UploadFile
from pydantic.typing import List
from logger import Logger
from app.service.ocr.asyn_ocr_task import AsynPredictTask
from fastapi.responses import JSONResponse


router = APIRouter()
logger = Logger(__name__)
Asyn_worker = AsynPredictTask(logger)


@router.post("/cv-ocr", summary="controller 辨識")  # responses={},
async def cv_upload(request: Request, image_class: str = Form(...), files: List[UploadFile] = File(...)):
    '''
    call cv_controller api
    '''
    tasks = []
    action = 'cv-ocr'
    logger.info({action: {'upload_file_num': len(files), 'image_class': image_class}})
    try:
        for file in files:
            try:
                task = Asyn_worker.process_image(request, file, action=action, input_params={'image_class': image_class})
                tasks.append(task)
            except Exception as ex:
                task_id = task.get('task_id', '')
                image_id = task.get('image_id', '')
                logger.error({'task_id': task_id, 'image_id': image_id, 'error_msg': str(ex)})
                tasks.append({'task_id': task_id, 'status': 'ERROR', 'url_result': f'/ocr/result/{task_id}'})
        return JSONResponse(status_code=200, content=tasks)
    except Exception as ex:
        logger.error({'error_msg': str(ex)})
        return JSONResponse(status_code=400, content=[])
