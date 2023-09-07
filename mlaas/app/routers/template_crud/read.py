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
from app.api_config import http_responses
from app.router_schema import mlaas_item_generator
from fastapi.encoders import jsonable_encoder
from app.route_utils import get_output_template
from copy import deepcopy
import uuid
import time

router = APIRouter()

available_Input, available_Output = mlaas_item_generator(
    'GetAvailableTemplates', GetAvailableTemplatesRequest, GetAvailableTemplatesResponse)

detail_Input, detail_Output = mlaas_item_generator(
    'GetTemplateDetail', GetTemplateDetailRequest, GetTemplateDetailResponse)


@router.post("/get_available_templates", response_model=available_Output, responses=http_responses)
async def get_available_templates(request: available_Input, db: Session = Depends(get_db)):
    '''
    取得該 user_id 可用的 template 清單
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
    status_dict = {
        '0001': 'code error',
    }
    if req_data['request_id'] in status_dict:
        end_time = time.time()
        duration_time = round((end_time - start_time), 4)
        result = {
            'status_code': req_data['request_id'],
            'status_msg': status_dict[req_data['request_id']]
        }
        output.update(response_time=end_time,
                      duration_time=duration_time, outputs=result)
        return available_Output(**output)

    data = GetAvailableTemplatesRequest(**req_data['inputs'])
    form = GetAvailableTemplatesForm(data)

    await form.load_data()
    if await form.is_valid():
        template = GetAvailableTemplatesRequest(
            user_id=form.user_id
        )
        available_templates = service_read.get_available_templates(
            template, db)
        end_time = time.time()
        duration_time = round((end_time - start_time), 4)
        result = {
            'status_code': '0000',
            'status_msg': 'OK',
            'template_infos': available_templates
        }
        output.update(response_time=end_time,
                      duration_time=duration_time, outputs=result)
        return available_Output(**output)
    raise CustomException(status_code=401, message=form.errors)


@router.post("/get_template_detail", response_model=detail_Output, responses=http_responses)
async def get_template_detail(request: detail_Input, db: Session = Depends(get_db)):
    '''
    取得該 template 的細節
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

    status_dict = {
        '0001': 'code error',
        '5407': 'template_id not exist'
    }
    if req_data['request_id'] in status_dict:
        end_time = time.time()
        duration_time = round((end_time - start_time), 4)
        result = {
            'status_code': req_data['request_id'],
            'status_msg': status_dict[req_data['request_id']]
        }
        output.update(response_time=end_time,
                      duration_time=duration_time, outputs=result)
        return detail_Output(**output)

    data = GetTemplateDetailRequest(**req_data['inputs'])
    form = GetTemplateDetailForm(data)
    await form.load_data()
    if await form.is_valid():
        template = GetTemplateDetailRequest(
            template_id=form.template_id
        )
        template_detail = service_read.get_template_detail(template, db)
        end_time = time.time()
        duration_time = round((end_time - start_time), 4)
        result = {
            'status_code': '0000',
            'status_msg': 'OK',
            'template_detail': template_detail
        }
        output.update(response_time=end_time,
                      duration_time=duration_time, outputs=result)
        return detail_Output(**output)
    raise CustomException(status_code=401, message=form.errors)
