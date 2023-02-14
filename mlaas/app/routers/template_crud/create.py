from app.database import get_db
from app.exceptions import CustomException
from app.schema.common import Response
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.schema.template_crud.create import CreateTemplateRequest
from app.forms.template_crud.create import CreateTemplateForm
from app.services.template_crud import create as service_create
from app.schema.template_crud.create import CreateTemplateResponse


router = APIRouter()


@router.post("/create_template", response_model=CreateTemplateResponse)  # responses={},
async def create_template(request: CreateTemplateRequest, db: Session = Depends(get_db)):
    '''
    將 template 影像上傳至 MinIO, 並將其餘資訊存入 Feature DB
    '''
    form = CreateTemplateForm(request)
    await form.load_data()
    if await form.is_valid():
        template = CreateTemplateRequest(
            user_id=form.user_id,
            image=form.image,
            bbox=form.bbox,
            template_name=form.template_name,
            is_public=form.is_public,
            is_no_ttl=form.is_no_ttl
            )
        template_id = service_create.create_template(template=template, db=db)
        return CreateTemplateResponse(
            template_id=template_id
        )
    raise CustomException(status_code=400, message=form.errors)
