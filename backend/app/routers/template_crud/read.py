from app import response_table
from app.exceptions import MlaasRequestError
from app.schema.template_crud.read import (GetAvailableTemplatesResponse,
                                           GetTemplateDetailResponse)
from fastapi import APIRouter
from route_utils import async_call_mlaas_function
from starlette.requests import Request

router = APIRouter()


@router.get("/get_available_templates", response_model=GetAvailableTemplatesResponse)
async def get_available_templates(request: Request):
    '''
    取得該 user_id 可用的 template 清單
    '''
    user_id = request.state.user_id
    rid = request.state.request_id
    logger = request.state.logger
    input_data = {
        "business_unit": "C170",
        "request_id": rid,
        "inputs": {'user_id': user_id}
    }
    outputs = await async_call_mlaas_function(input_data, 'template_crud/get_available_templates', project='GP', logger=logger)
    status_code = outputs['outputs']['status_code']
    if status_code == '0000':
        return GetAvailableTemplatesResponse(
            template_infos=outputs['outputs']['template_infos']
        )
    else:
        logger.error({'error_msg': outputs['outputs']})
        raise MlaasRequestError(status_code, outputs['outputs']['status_msg'])


@router.get("/get_template_detail/{template_id}", response_model=GetTemplateDetailResponse)
async def get_template_detail(template_id: str, request: Request):
    '''
    取得該 template 的細節
    '''
    rid = request.state.request_id
    logger = request.state.logger
    input_data = {
        "business_unit": "C170",
        "request_id": rid,
        "inputs": {'template_id': template_id}
    }
    outputs = await async_call_mlaas_function(input_data, 'template_crud/get_template_detail', project='GP', logger=logger)
    status_code = outputs['outputs']['status_code']
    if status_code == '0000':
        template_detail = outputs['outputs']['template_detail']
        return GetTemplateDetailResponse(
            image=template_detail['image'],
            is_no_ttl=template_detail['is_no_ttl'],
            template_name=template_detail['template_name'],
            points_list=template_detail['points_list'],
            creation_time=template_detail['creation_time'],
            expiration_time=template_detail['expiration_time']
        )
    elif status_code == '5407':
        logger.error({'error_msg': response_table.status_templateexisterror})
        raise MlaasRequestError(**response_table.status_templateexisterror)
    else:
        logger.error({'error_msg': outputs['outputs']})
        raise MlaasRequestError(status_code, outputs['outputs']['status_msg'])
