from app.exceptions import MlaasRequestError, CustomException
from app.schema.template_crud.read import (GetAvailableTemplatesResponse,
                                           GetTemplateDetailResponse)
from fastapi import APIRouter, Depends
from route_utils import async_call_mlaas_function
from route_utils import get_current_user, get_request_id
from utils.logger import Logger
from app.models.user import User
from starlette.requests import Request


router = APIRouter(dependencies=[Depends(get_current_user)])
logger = Logger('read_template')


@router.get("/get_available_templates", response_model=GetAvailableTemplatesResponse)
async def get_available_templates(current_user: User = Depends(get_current_user)):
    '''
    取得該 user_id 可用的 template 清單
    '''
    rid = get_request_id()
    input_data = {
        "business_unit": "C170",
        "request_id": rid,
        "inputs": {'user_id': current_user.user_id}
    }
    try:
        outputs = await async_call_mlaas_function(input_data, 'template_crud/get_available_templates', project='GP', logger=logger)
    except MlaasRequestError as e:
        raise e
    except Exception as e:
        logger.error({'error_msg': str(e)})
        raise CustomException(status_code=500, message=str(e))
    return GetAvailableTemplatesResponse(
        template_infos=outputs['template_infos']
    )


@router.get("/get_template_detail/{template_id}", response_model=GetTemplateDetailResponse)
async def get_template_detail(template_id: str, current_user: User = Depends(get_current_user)):
    '''
    取得該 template 的細節
    '''
    rid = get_request_id()
    logger.logger.extra['request_id'] = rid
    logger.logger.extra['user_id'] = current_user.user_id
    
    input_data = {
        "business_unit": "C170",
        "request_id": rid,
        "inputs": {'template_id': template_id}
    }
    try:
        outputs = await async_call_mlaas_function(input_data, 'template_crud/get_template_detail', project='GP', logger=logger)
        template_detail = outputs['template_detail']
    except MlaasRequestError as e:
        raise e
    except Exception as e:
        logger.error({'error_msg': str(e)})
        raise CustomException(status_code=500, message=str(e))
    return GetTemplateDetailResponse(
        image=template_detail['image'],
        is_no_ttl=template_detail['is_no_ttl'],
        template_name=template_detail['template_name'],
        points_list=template_detail['points_list'],
        creation_time=template_detail['creation_time'],
        expiration_time=template_detail['expiration_time']
    )
