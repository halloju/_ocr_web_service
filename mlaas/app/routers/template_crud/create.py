from app.database import get_db
from app.exceptions import CustomException
from app.schema.common import Response
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
import time

from app.schema.template_crud.create import CreateTemplateRequest
from app.forms.template_crud.create import CreateTemplateForm
from app.services.template_crud import create as service_create
from app.schema.template_crud.create import CreateTemplateResponse

from app.router_schema import mlaas_item_generator
from fastapi.encoders import jsonable_encoder
from app.route_utils import get_output_template
from app.api_config import http_responses
from copy import deepcopy
import uuid

router = APIRouter()


Input, Output = mlaas_item_generator('CreateTemplate', CreateTemplateRequest, CreateTemplateResponse)

@router.post("/create_template", response_model=Output, responses=http_responses)  # responses={},
async def create_template(request: Input, db: Session = Depends(get_db)):
    '''
    將 template 影像上傳至 MinIO, 並將其餘資訊存入 Feature DB
    '''
    start_time = time.time()
    req_data = jsonable_encoder(request)
    trace_id = str(uuid.uuid4())
    output_template = get_output_template()
    output = deepcopy(output_template)
    output.update(
        business_unit=req_data['business_unit'],
        request_id=req_data['request_id'],
        trace_id=trace_id,
        request_time=start_time
    )
    # status
    status_dict = {
        '0001': 'code error',
        '5401': 'unique violation',
        '5402': 'image type error'
    }
    if req_data['request_id'] in status_dict:
        end_time = time.time()
        duration_time = round((end_time - start_time), 4)
        result = {
            'status_code': req_data['request_id'],
            'status_msg': status_dict[req_data['request_id']]
        }
        output.update(response_time=end_time, duration_time=duration_time, outputs=result)
        return Output(**output)
    
    data = CreateTemplateRequest(**req_data['inputs'])
    form = CreateTemplateForm(data)
    await form.load_data()
    if await form.is_valid():
        template = CreateTemplateRequest(
            user_id=form.user_id,
            image=form.image,
            points_list=form.points_list,
            template_name=form.template_name,
            is_public=form.is_public,
            is_no_ttl=form.is_no_ttl
        )
        template_id = service_create.create_template(template=template, db=db)
        end_time = time.time()
        duration_time = round((end_time - start_time), 4)
        result = {
            'template_id': template_id,
            'status_code': '0000',
            'status_msg': 'OK'
        }
        output.update(response_time=end_time, duration_time=duration_time, outputs=result)
        return Output(**output)
    raise CustomException(status_code=401, message=form.errors)
