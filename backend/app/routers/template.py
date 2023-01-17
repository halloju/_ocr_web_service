from app.database import get_db
from app.exceptions import CustomException
from app.schema.common import Response
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.schema.template import CreateTemplateRequest
from app.forms.template.create import CreateTemplateForm
from app.services.template import create as service_create
from app.schema.template import CreateTemplateResponse

from app.services.template import read as service_read
from app.schema.template import GetAvailableTemplatesResponse
from app.schema.template import GetTemplateDetailResponse

from app.schema.template import UpdateTemplateRequest
from app.forms.template.update import UpdateTemplateForm
from app.services.template import update as service_update

from app.schema.template import DeleteTemplateRequest
from app.forms.template.delete import DeleteTemplateForm
from app.services.template import delete as service_delete

router = APIRouter()


@router.post("/create", response_model=CreateTemplateResponse)  # responses={},
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
            is_no_ttl=form.is_no_ttl,
            bbox=form.bbox,
            template_name=form.template_name,
            is_public=form.is_public
            )
        template_id = service_create.create_template(template=template, db=db)
        return CreateTemplateResponse(
            template_id=template_id
        )
    raise CustomException(status_code=400, message=form.errors)


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


@router.post("/update")
async def update_template(request: UpdateTemplateRequest, db: Session = Depends(get_db)):
    '''
    將 Feature DB 中的 template 資訊更新
    '''
    form = UpdateTemplateForm(request)
    await form.load_data()
    if await form.is_valid():
        template = UpdateTemplateRequest(
            template_id=form.template_id,
            bbox=form.bbox,
            template_name=form.template_name
            )
        template_id = service_update.update_template(template=template, db=db)
        return Response(data={"status": 200})
    raise CustomException(status_code=400, message=form.errors)


@router.post("/delete")
async def delete_template(request: DeleteTemplateRequest, db: Session = Depends(get_db)):
    '''
    將 Feature DB 中的 template 資訊刪除
    '''
    form = DeleteTemplateForm(request)
    await form.load_data()
    if await form.is_valid():
        template = DeleteTemplateRequest(
            template_id=form.template_id
            )
        template_id = service_delete.delete_template(template=template, db=db)
        return Response(data={"status": 200})
    raise CustomException(status_code=400, message=form.errors)
