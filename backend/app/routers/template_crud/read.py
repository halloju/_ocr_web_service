from app.database import get_db
from app.exceptions import CustomException
from app.schema.common import Response
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.services.template_crud import read as service_read
from app.schema.template_crud.read import GetAvailableTemplatesResponse
from app.schema.template_crud.read import GetTemplateDetailResponse


router = APIRouter()


@router.get("/get_available_templates/{user_id}", response_model=GetAvailableTemplatesResponse)
def get_available_templates(user_id: str, is_public: bool, db: Session = Depends(get_db)):
    '''
    取得該 user_id 可用的 template 清單
    '''
    available_templates = service_read.get_available_templates(db, user_id, is_public)
    return GetAvailableTemplatesResponse(
        available_templates=available_templates
    )


@router.get("/get_template_detail/{template_id}", response_model=GetTemplateDetailResponse)
def get_template_detail(template_id: str, db: Session = Depends(get_db)):
    '''
    取得該 template 的細節
    '''
    image, template_detail = service_read.get_template_detail(db, template_id)
    return GetTemplateDetailResponse(
        image=image,
        template_name=template_detail['template_name'],
        bbox=template_detail['bbox']
    )
