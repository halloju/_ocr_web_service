from app.exceptions import MlaasRequestError, CustomException
from app.schema.common import Response
from fastapi import APIRouter
from starlette.requests import Request
from route_utils import async_call_mlaas_function

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
    try:
        await async_call_mlaas_function(input_data, 'template_crud/delete_template', project='GP', logger=logger)
    except MlaasRequestError as e:
        raise e
    except Exception as e:
        logger.error({'error_msg': str(e)})
        raise CustomException(status_code=500, message=str(e))
    return Response(status_code=200)
