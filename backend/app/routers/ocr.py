from app.database import get_db
from app.exceptions import CustomException
from app.schema.common import Response
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.schema.ocr import CreateGPOCRRequest
from app.forms.ocr import CreateGPOCRForm
from app.services.ocr import gpocr
from app.schema.ocr import CreateGPOCRResponse

router = APIRouter()


@router.post("/gpocr", response_model=CreateGPOCRResponse)  # responses={},
async def gp_ocr(request: CreateGPOCRRequest, db: Session = Depends(get_db)):
    '''
    將 image 影像上傳至 MinIO, 並進行全文辨識，將辨識結果存入 db
    '''
    form = CreateGPOCRForm(request)
    await form.load_data()
    if await form.is_valid():
        ocr_image_info = CreateGPOCRRequest(
            image=form.image)
        image_cv_id, ocr_results = gpocr(ocr_image_info=ocr_image_info, db=db)
        return CreateGPOCRResponse(
            image_cv_id=image_cv_id,
            ocr_results=ocr_results
        )
    raise CustomException(status_code=400, message=form.errors)
