from app.database import get_db
from app.exceptions import CustomException
from app.schema.common import Response
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.services.template_crud import read as service_read
from app.schema.template_crud.read import GetAvailableTemplatesResponse, GetAvailableTemplatesRequest
from app.schema.template_crud.read import GetTemplateDetailResponse, GetTemplateDetailRequest
from app.forms.template_crud.read import GetAvailableTemplatesForm, GetTemplateDetailForm


router = APIRouter()


@router.post("/get_available_templates", response_model=GetAvailableTemplatesResponse)
def get_available_templates(request: GetAvailableTemplatesRequest, db: Session = Depends(get_db)):
    '''
    取得該 user_id 可用的 template 清單
    '''
    form = GetTemplateDetailForm(request)
    await form.load_data()
    if await form.is_valid():
        template = GetTemplateDetailRequest(
            template_id=form.user_id
            )
        available_templates = service_read.get_available_templates(template, db)
        return GetAvailableTemplatesResponse(
            available_templates=available_templates
        )
    raise CustomException(status_code=400, message=form.errors)


@router.post("/get_template_detail", response_model=GetTemplateDetailResponse)
def get_template_detail(request: GetTemplateDetailRequest, db: Session = Depends(get_db)):
    '''
    取得該 template 的細節
    '''
    form = GetTemplateDetailForm(request)
    await form.load_data()
    if await form.is_valid():
        template = GetTemplateDetailRequest(
            template_id=form.template_id
            )
        image, template_detail = service_read.get_template_detail(template, db)
        return GetTemplateDetailResponse(
            image=image,
            template_name=template_detail['template_name'],
            bbox=template_detail['bbox']
        )
    raise CustomException(status_code=400, message=form.errors)
