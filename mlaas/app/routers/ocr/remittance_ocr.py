from fastapi import APIRouter
from fastapi import Depends

from app.schema.ocr.remittance_ocr import PredictInput
from app.schema.ocr.remittance_ocr import PredictOutput

from app.router_schema import mlaas_item_generator
from fastapi.encoders import jsonable_encoder
from app.route_utils import get_output_template
from copy import deepcopy
import uuid
import time

from app.api_config import http_responses


Input, Output = mlaas_item_generator('REMITTANCE', PredictInput, PredictOutput)


router = APIRouter()


@router.post("/predict", response_model=Output, responses=http_responses)  # responses={},
async def predict(request: Input):
    '''
    remittance mlaas api
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
        '5401': 'unique violation',
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
    
    data = PredictInput(**req_data['inputs'])

    end_time = time.time()
    duration_time = round((end_time - start_time), 4)
    result = {
        'remitno': 'I90002',
        'amount': '0000000000500',
        'receiveacc': '00015979150388',
        'remitterid': 'A123456789',
        'agentid': 'B123456789',
        'receivebank': '5210116',
        'remark': 'Y',
        'receiver_name': '王曉明',
        'remit_name': '黃大強',
        'agent_name': '陳玉珊',
        'status_code': '0000',
        'status_msg': 'OK'
    }
    output.update(response_time=end_time, duration_time=duration_time, outputs=result)
    return Output(**output)
