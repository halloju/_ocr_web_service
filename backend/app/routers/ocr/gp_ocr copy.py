import asyncio
import base64
import json
import sys
import uuid
import zlib
from app.database import get_db
from app.exceptions import CustomException
from app.schema.ocr.gp_ocr import GpocrUpload, GpocrPredict
from app.services.ocr.gp_ocr import gp_ocr as service_gp_ocr
from app.schema.ocr.gp_ocr import GpocrResponse
from celery.result import AsyncResult
from fastapi import APIRouter, Body, Depends, File, Request, HTTPException, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.orm import Session
from pydantic.typing import List
from worker import create_task, upload_to_redis, get_from_redis

router = APIRouter()

@router.post("/upload_image", summary="直接上傳圖片到 Redis")
async def upload_image(request: Request, files: List[UploadFile] = File(...), ):
    '''
    將圖片儲存在 Redis
    回傳 image_id
    '''
    image_ids = await asyncio.gather(*[upload_image_to_redis(request, image) for image in files])
    return image_ids

async def upload_image_to_redis(request, image):
    image_id = str(uuid.uuid4())
    await router.state.redis.set(image_id, await image.read())
    return image_id

@router.post('/upload_image_with_task', summary="上傳圖片(用task實作)")
async def upload_image_with_task(files: List[UploadFile] = File(...)):
    tasks = []
    # try:
    for file in files:
        d = {}
        try:
            # Read file data
            file_data = await file.read()
            file_data_base64 = base64.b64encode(file_data).decode('utf-8')
            # start task prediction
            task_id = upload_to_redis.delay(file_data_base64)
            d['task_id'] = str(task_id)
            d['status'] = 'PROCESSING'
            d['url_result'] = f'/api/result/{task_id}'
        except Exception as ex:
            d['task_id'] = str(task_id)
            d['status'] = 'ERROR'
            d['url_result'] = ''
        tasks.append(d)
    return JSONResponse(status_code=202, content=tasks)

@router.get('/upload_image/result/{task_id}', summary="依照任務查詢上傳圖片進度和圖片id")
async def upload_image_result(task_id: str):
    image_id = ''
    task_status = 'PROCESSING'
    task = AsyncResult(task_id)
    if task.state == 'FAILURE':
        task_status = 'ERROR'
    elif task.ready():
        result = get_from_redis.delay(task_id).get()
        task_status = result['status']
        image_id = result['image_id']
    return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': task_status, 'image_id': image_id})

@router.post("/gp_ocr", response_model=GpocrResponse)  # responses={},
async def gp_ocr(request: GpocrUpload, db: Session = Depends(get_db)):
    '''
    將 image 影像上傳至 MinIO, 並進行全文辨識，將辨識結果存入 db
    '''
    form = GpocrForm(request)
    await form.load_data()
    if await form.is_valid():
        ocr_image_info = GpocrRequest(
            image=form.image)
        image_cv_id, ocr_results = service_gp_ocr(ocr_image_info=ocr_image_info, db=db)
        return GpocrResponse(
            image_cv_id=image_cv_id,
            ocr_results=ocr_results
        )
    raise CustomException(status_code=400, message=form.errors)