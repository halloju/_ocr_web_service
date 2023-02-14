from app.database import get_db
from app.exceptions import CustomException
from app.schema.common import Response
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.schema.template_crud.delete import DeleteTemplateRequest
from app.forms.template_crud.delete import DeleteTemplateForm
from app.services.template_crud import delete as service_delete


router = APIRouter()


@router.post("/delete_template")
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
    raise CustomException(status_code=400, message=form.errors)
