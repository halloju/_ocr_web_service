from fastapi import APIRouter, File, Form, Request, UploadFile, Depends
from pydantic.typing import List
from app.service.ocr.async_ocr_task import AsyncPredictTask
from fastapi.responses import JSONResponse
from route_utils import get_redis
from aioredis import Redis

router = APIRouter()


@router.post("/cv-ocr", summary="controller 辨識")  # responses={},
async def cv_upload(request: Request, image_class: str = Form(...), files: List[UploadFile] = File(...), redis: Redis = Depends(get_redis)):
    '''
    call cv_controller api
    '''
    async_worker = AsyncPredictTask(redis_pool=redis, request=request)
    tasks = []
    action = 'cv-ocr'
    logger = request.state.logger
    logger.info(
        {action: {'upload_file_num': len(files), 'image_class': image_class}})
    try:
        for file in files:
            try:
                task = await async_worker.process_image(file, action=action, input_params={'image_class': image_class})
                tasks.append(task)
            except Exception as ex:
                logger.error({'error_msg': str(ex)})
                task_id = task.get('task_id', '')
                image_id = task.get('image_id', '')
                logger.error(
                    {'task_id': task_id, 'image_id': image_id, 'error_msg': str(ex)})
                tasks.append({'task_id': task_id, 'status': 'ERROR',
                             'url_result': f'/ocr/result/{task_id}'})
        return JSONResponse(status_code=200, content=tasks)
    except Exception as ex:
        logger.error({'error_msg': str(ex)})
        return JSONResponse(status_code=400, content=[])
