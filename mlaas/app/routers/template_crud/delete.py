from app.database import get_db
from app.exceptions import CustomException
from app.schema.common import Response
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.schema.template_crud.delete import DeleteTemplateRequest
from app.forms.template_crud.delete import DeleteTemplateForm
from app.services.template_crud import delete as service_delete
from app.schema.template_crud.delete import DeleteTemplateResponse

router = APIRouter()


@router.post("/delete_template", response_model=DeleteTemplateResponse)
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
        return DeleteTemplateResponse(
            status_code='0000',
            status_msg='OK'
        )
    raise CustomException(status_code=400, message=form.errors)
