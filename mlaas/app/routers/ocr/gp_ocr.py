from app.database import get_db
from app.exceptions import CustomException
# from app.schema.common import Response
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.schema.ocr.gp_ocr import GpocrRequest
from app.forms.ocr.gp_ocr import GpocrForm
from app.services.ocr.gp_ocr import gp_ocr as service_gp_ocr
from app.schema.ocr.gp_ocr import GpocrResponse

router = APIRouter()


@router.post("/gp_ocr", response_model=GpocrResponse)  # responses={},
async def gp_ocr(request: GpocrRequest, db: Session = Depends(get_db)):
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
            ocr_results=ocr_results,
            status_code='0000',
            status_msg='OK'
        )
    raise CustomException(status_code=400, message=form.errors)
