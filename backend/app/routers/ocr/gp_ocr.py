import base64
import json
import uuid
from io import BytesIO
from app.database import get_db
from app.exceptions import CustomException
from fastapi import APIRouter, Body, Depends, File, Response, Request, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.services.ocr.gp_ocr import gp_ocr as service_gp_ocr
from pydantic.typing import List

router = APIRouter()

@router.post("/upload_images", summary="單張圖片辨識功能")
async def store_images(request: Request, files: List[UploadFile] = File(...)):
    '''
    將 image 影像全部上傳至 Redis
    '''
    image_ids = []
    for file in files:
        # Generate a unique image ID using the uuid module
        image_id = str(uuid.uuid4())

        # Read and encode the file data as base64
        image_data = await file.read()
        encoded_data = base64.b64encode(image_data).decode("utf-8")

        # Store the encoded image data in Redis using the image ID as the key
        await request.app.state.redis.set(image_id, encoded_data)
        # Set an expiration time of 1 day (86400 seconds) for the key
        await request.app.state.redis.expire(image_id, 86400)

        # Append the generated image ID to the list of image IDs
        image_ids.append(image_id)

    # Return the list of image IDs
    return image_ids

async def generate_image_stream(images):
    for image in images:
        yield image

@router.post("/get_images")
async def get_images(request: Request, image_ids: List[str]):
    # Get the Redis connection from the app state
    redis = request.app.state.redis
    pipeline = redis.pipeline()
    for image_id in image_ids:
        pipeline.get(image_id)
    results = await pipeline.execute()
    images_dict = {}
    for image_id, result in zip(image_ids, results):
        images_dict[image_id] = result

    return images_dict

# 這個好像會亂碼ＱＱ
@router.post("/get_images2")
async def get_images(request: Request, image_ids: List[str]):
    # Get the Redis connection from the app state
    redis = request.app.state.redis
    pipeline = redis.pipeline()
    for image_id in image_ids:
        pipeline.get(image_id)
    results = await pipeline.execute()
    images_dict = {}
    for image_id, result in zip(image_ids, results):
        images_dict[image_id] = result
    
    async def generate_image_stream():
        for image_id, image_data in images_dict.items():
            img_io = BytesIO(base64.b64decode(image_data))
            while chunk := img_io.read(1024):
                yield chunk
    
    return StreamingResponse(generate_image_stream(), media_type="multipart/x-mixed-replace; boundary=frame")