from app.database import get_db
from app.exceptions import CustomException
from app.schema.common import Response
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi import Depends
from sqlalchemy.orm import Session

from app.schema.template_crud.create import CreateTemplateRequest
from app.forms.template_crud.create import CreateTemplateForm
from app.schema.template_crud.create import CreateTemplateResponse
from route_utils import get_user_id, call_mlaas_function, get_request_id
from app.exceptions import MlaasRequestError
from app import response_table
import json

router = APIRouter()


@router.post("/create_template", response_model=CreateTemplateResponse)  # responses={},
async def create_template(request: CreateTemplateRequest, db: Session = Depends(get_db)):
    '''
    將 template 影像上傳至 MinIO, 並將其餘資訊存入 Feature DB
    '''
    form = CreateTemplateForm(request)
    await form.load_data()
    if await form.is_valid():
        inputs = {
            'user_id': get_user_id(),
            'image': form.image,
            'points_list': form.points_list,
            'template_name': form.template_name,
            'is_public': False,
            'is_no_ttl': False
        }
        input_data = {
            "business_unit": "C170",
            "request_id": "111",
            "inputs": jsonable_encoder(inputs)
        }
        outputs = call_mlaas_function(input_data, 'template_crud/create_template')
        status_code = outputs['outputs']['status_code']
        if status_code == '0000':
            print(outputs['outputs']['template_id'])
            return CreateTemplateResponse(
                template_id=outputs['outputs']['template_id'],
                status_code='0000',
                status_msg='OK'
            )
        elif status_code == '5401':
            raise MlaasRequestError(**response_table.status_uniqueviolation)
        elif status_code == '5402':
            raise MlaasRequestError(**response_table.status_image_type_error)
        else:
            raise MlaasRequestError(status_code, outputs['outputs']['status_msg'])
    raise CustomException(status_code=400, message=form.errors)
