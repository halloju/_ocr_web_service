import asyncio
from app.database import get_db
from app.exceptions import CustomException
from app.forms.ocr.gp_ocr import GpocrForm
from app.schema.ocr.gp_ocr import GpocrRequest, GpocrRequest2
from app.services.ocr.gp_ocr import gp_ocr as service_gp_ocr
from app.schema.ocr.gp_ocr import GpocrResponse
from fastapi import APIRouter, Request
from fastapi import Depends
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/gp_ocr_1", summary="單張圖片辨識功能")
async def gp_ocr_1(request: Request, gpocr_request: GpocrRequest, db: Session = Depends(get_db)):
    '''
    (1) 將 image 影像全部上傳至 Redis
    (2) 將第一張圖片打 MLaaS，僅回傳第一張結果
    (3) Redis 暫存預設一天
    '''
    # Save image to Redis
    for image_id, image_data in gpocr_request.image.items():
        # Set image data in Redis using the provided id as key
        await request.app.state.redis.set(image_id, image_data)
        # Set an expiration time of 1 day (86400 seconds) for the key
        await request.app.state.redis.expire(image_id, 86400)

    # 打 MLaaS
    form = GpocrForm(gpocr_request)
    await form.load_data()
    if await form.is_valid():
        ocr_image_info = list(form.imageDict.values())[0]
        image_cv_id, ocr_results = service_gp_ocr(ocr_image_info=ocr_image_info, db=db)
        return GpocrResponse(
            image_cv_id=image_cv_id,
            ocr_results=ocr_results
        )
    raise CustomException(status_code=400, message=form.errors)

@router.post("/gp_ocr_2", summary="全部圖片辨識功能")
async def gp_ocr_2(request: Request, gpocr_request: GpocrRequest2, db: Session = Depends(get_db)):
    '''
    (1) 從 Redis 將 image 拉下來，拉下來就會刪除該張緩存
    (2) 一張一張打到 MLaaS
    (3) 整理好 Response 回傳給前端
    '''
    ocr_results = {}
    # Process images and store OCR results
    coroutines = []
    for image_id in gpocr_request.image:
        coroutines.append(process_image(image_id, request, db, ocr_results))
    await asyncio.gather(*coroutines)
    return {"ocr_results": ocr_results}

async def process_image(image_id, request, db, ocr_results):
    ocr_image_info = await request.app.state.redis.get(image_id)
    if ocr_image_info:
        # Process image with backend service
        image_cv_id, ocr_result = service_gp_ocr(ocr_image_info=ocr_image_info, db=db)
        ocr_results[image_id] = {
            "image_cv_id": image_cv_id,
            "ocr_result": ocr_result
        }
        # Remove image from Redis
        await request.app.state.redis.delete(image_id)
