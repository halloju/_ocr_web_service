from app.database import get_db
from app.exceptions import CustomException
from app.schema.common import Response
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.schema.template_crud.update import UpdateTemplateRequest, UpdateTemplateResponse
from app.forms.template_crud.update import UpdateTemplateForm
from app.services.template_crud import update as service_update


router = APIRouter()


@router.post("/update_template", response_model=UpdateTemplateResponse)
async def update_template(request: UpdateTemplateRequest, db: Session = Depends(get_db)):
    '''
    將 Feature DB 中的 template 資訊更新
    '''
    form = UpdateTemplateForm(request)
    await form.load_data()
    if await form.is_valid():
        template = UpdateTemplateRequest(
            user_id=form.user_id,
            template_id=form.template_id,
            points_list=form.points_list,
            template_name=form.template_name
            )
        new_template_id = service_update.update_template(template=template, db=db)
        return UpdateTemplateResponse(
            template_id=new_template_id,
            status_code='0000',
            status_msg='OK')
    raise CustomException(status_code=400, message=form.errors)
