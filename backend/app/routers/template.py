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

from app.schema.template import UpdateTemplateRequest
from app.forms.template.update import UpdateTemplateForm
from app.services.template import update as service_update

from app.schema.template import DeleteTemplateRequest
from app.forms.template.delete import DeleteTemplateForm
from app.services.template import delete as service_delete

router = APIRouter()


@router.post("/create")
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
            template_name=form.template_name)
        template_id = service_create.create_template(template=template, db=db)
        return CreateTemplateResponse(
            template_id=template_id
        )
        # return Response(data={"status": 200, "template_id": template_id})
    raise CustomException(status_code=400, message=form.errors)


@router.get("/get_available_templates/{user_id}")
def get_available_templates(user_id: str, db: Session = Depends(get_db)):
    '''
    取得該 user_id 可用的 template 清單
    '''
    available_templates = service_read.get_available_templates(db, user_id)
    return Response(data={"status": 200, "available_templates": available_templates})


@router.get("/get_template_detail/{template_id}")
def get_template_detail(template_id: str, db: Session = Depends(get_db)):
    '''
    取得該 template 的細節
    '''
    template_detail = service_read.get_template_detail(db, template_id)
    return Response(data={"status": 200, "template_detail": template_detail})


@router.post("/update")
async def update_template(request: UpdateTemplateRequest, db: Session = Depends(get_db)):
    '''
    將 Feature DB 中的 template 資訊更新
    '''
    form = UpdateTemplateForm(request)
    await form.load_data()
    if await form.is_valid():
        template = UpdateTemplateRequest(
            user_id=form.user_id,
            bbox=form.bbox
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
            user_id=form.user_id
            )
        template_id = delete_template.delete_template(template=template, db=db)
        return Response(data={"status": 200})
    raise CustomException(status_code=400, message=form.errors)
