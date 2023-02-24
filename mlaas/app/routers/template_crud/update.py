from app.database import get_db
from app.exceptions import CustomException
from app.schema.common import Response
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.schema.template_crud.update import UpdateTemplateRequest, UpdateTemplateResponse
from app.forms.template_crud.update import UpdateTemplateForm
from app.services.template_crud import update as service_update


from app.router_schema import mlaas_item_generator
from fastapi.encoders import jsonable_encoder
from app.route_utils import get_output_template
from copy import deepcopy
import uuid
import time

router = APIRouter()


Input, Output = mlaas_item_generator('UpdateTemplate', UpdateTemplateRequest, UpdateTemplateResponse)


@router.post("/update_template", response_model=Output)
async def update_template(request: Input, db: Session = Depends(get_db)):
    '''
    將 Feature DB 中的 template 資訊更新
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
    # data = full_data['inputs']
    data = UpdateTemplateRequest(**req_data['inputs'])
    form = UpdateTemplateForm(data)
    await form.load_data()
    if await form.is_valid():
        template = UpdateTemplateRequest(
            user_id=form.user_id,
            template_id=form.template_id,
            points_list=form.points_list,
            template_name=form.template_name
            )
        new_template_id = service_update.update_template(template=template, db=db)
        end_time = time.time()
        duration_time = round((end_time - start_time), 4)
        result = {
            'status_code': '0000',
            'status_msg': 'OK',
            'template_id': new_template_id
        }
        output.update(response_time=end_time, duration_time=duration_time, outputs=result)
        return Output(**output)
    raise CustomException(status_code=400, message=form.errors)
