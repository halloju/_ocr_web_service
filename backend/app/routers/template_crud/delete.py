from app import response_table
from app.exceptions import MlaasRequestError
from app.schema.common import Response
from fastapi import APIRouter, Depends
from starlette.requests import Request
from logger import Logger
from route_utils import call_mlaas_function, init_log, verify_token

router = APIRouter()
# logger = Logger(__name__)

@router.delete("/delete_template/{template_id}")
async def delete_template(template_id: str, request: Request):
    '''
    刪除給定的 template_id 在 mlaas Feature DB 中的 template 資訊
    '''
    rid = request.state.request_id
    logger = request.state.logger
    input_data = {
        "business_unit": "C170",
        "request_id": rid,
        "inputs": {'template_id': template_id}
    }
    outputs = call_mlaas_function(input_data, 'template_crud/delete_template', project='GP', logger=logger)
    status_code = outputs['outputs']['status_code']
    if status_code == '0000':
        return Response(status_code=200)
    elif status_code == '5407':
        logger.error({'error_msg': response_table.status_templateexisterror})
        raise MlaasRequestError(**response_table.status_templateexisterror)
    else:
        logger.error({'error_msg': outputs['outputs']})
        raise MlaasRequestError(status_code, outputs['outputs']['status_msg'])
