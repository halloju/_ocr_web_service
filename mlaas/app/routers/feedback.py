from app.database import get_db
from app.exceptions import CustomException
from app.schema.common import Response
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
import time

from app.schema.feedback import FeedbackRequest, FeedbackResponse

from app.router_schema import mlaas_item_generator
from fastapi.encoders import jsonable_encoder
from app.route_utils import get_output_template
from app.api_config import http_responses
from copy import deepcopy
import uuid

router = APIRouter()


Input, Output = mlaas_item_generator(
    'Feedback', FeedbackRequest, FeedbackResponse)


# responses={},
@router.post("/feedback", response_model=Output, responses=http_responses)
async def create_template(request: Input):
    '''
    傳送 feedback
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
        '0002': 'DB error'
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

    raise CustomException(status_code=401, message=form.errors)