from app.database import get_db
from app.exceptions import CustomException
from app.schema.common import Response
from fastapi import APIRouter
from fastapi import Depends
import time

from app.schema.user.user import AuthUsereRequest
from app.schema.user.user import AuthUserResponse

from app.router_schema import mlaas_item_generator
from fastapi.encoders import jsonable_encoder
from app.route_utils import get_output_template
from app.api_config import http_responses
from copy import deepcopy
import uuid

router = APIRouter()


Input, Output = mlaas_item_generator(
    'AuthUser', AuthUsereRequest, AuthUserResponse)


# responses={},
@router.post("/authenticate_user", response_model=Output, responses=http_responses)
async def create_template(request: Input):
    '''
    驗證使用者權限
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
    result = {
        'is_authenticated': False,
        'status_code': '0000',
        'status_msg': 'OK'
    }
    end_time = time.time()
    duration_time = round((end_time - start_time), 4)
    output.update(response_time=end_time, duration_time=duration_time, outputs=result)
    return Output(**output)
