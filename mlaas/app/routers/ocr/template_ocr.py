from app.database import get_db
from app.exceptions import CustomException
# from app.schema.common import Response
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.schema.ocr.template_ocr import TemplateocrRequest
from app.forms.ocr.template_ocr import TemplateocrForm
from app.services.ocr.template_ocr import template_ocr as service_template_ocr
from app.schema.ocr.template_ocr import TemplateocrResponse


router = APIRouter()


@router.post("/template_ocr", response_model=TemplateocrResponse)
async def template_ocr(request: TemplateocrRequest, db: Session = Depends(get_db)):
    '''
    將 image 影像上傳至 MinIO, 並進行模板辨識，將辨識結果存入 db
    '''
    form = TemplateocrForm(request)
    await form.load_data()
    if await form.is_valid():
        template_ocr_info = TemplateocrRequest(
            image=form.image, 
            template_id=form.template_id,
            model_name=form.model_name)
        image_cv_id, ocr_results = service_template_ocr(template_ocr_info=template_ocr_info, db=db)
        return TemplateocrResponse(
            image_cv_id=image_cv_id,
            ocr_results=ocr_results
        )
    raise CustomException(status_code=400, message=form.errors)
