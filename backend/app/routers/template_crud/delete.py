from app.exceptions import MlaasRequestError, CustomException
from app.schema.common import Response
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from route_utils import async_call_mlaas_function
from route_utils import get_current_user, get_request_id
from utils.logger import Logger
from app.models.user import User


router = APIRouter(dependencies=[Depends(get_current_user)])
logger = Logger('delete_template')


@router.delete("/delete_template/{template_id}")
async def delete_template(template_id: str, current_user: User = Depends(get_current_user)):
    '''
    刪除給定的 template_id 在 mlaas Feature DB 中的 template 資訊
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
        await async_call_mlaas_function(input_data, 'template_crud/delete_template', project='GP', logger=logger)
    except MlaasRequestError as e:
        raise e
    except Exception as e:
        logger.error({'error_msg': str(e)})
        raise CustomException(status_code=500, message=str(e))
    return Response(status_code=200)
