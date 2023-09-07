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

from app.router_schema import mlaas_item_generator
from fastapi.encoders import jsonable_encoder
from app.route_utils import get_output_template
from app.api_config import http_responses
from copy import deepcopy
import uuid
import time

router = APIRouter()


Input, Output = mlaas_item_generator(
    'DeleteTemplate', DeleteTemplateRequest, DeleteTemplateResponse)


@router.post("/delete_template", response_model=Output, responses=http_responses)
async def delete_template(request: Input, db: Session = Depends(get_db)):
    '''
    將 Feature DB 中的 template 資訊刪除
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
        return Output(**output)

    data = DeleteTemplateRequest(**req_data['inputs'])
    form = DeleteTemplateForm(data)
    await form.load_data()
    if await form.is_valid():
        template = DeleteTemplateRequest(
            template_id=form.template_id
        )
        service_delete.delete_template(template=template, db=db)
        end_time = time.time()
        duration_time = round((end_time - start_time), 4)
        result = {
            'status_code': '0000',
            'status_msg': 'OK'
        }
        output.update(response_time=end_time,
                      duration_time=duration_time, outputs=result)
        return Output(**output)
    raise CustomException(status_code=401, message=form.errors)
