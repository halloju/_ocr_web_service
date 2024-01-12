from app.exceptions import CustomException
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from app.schema.template_crud.update import UpdateTemplateRequest, UpdateTemplateResponse
from app.forms.template_crud.update import UpdateTemplateForm
from route_utils import async_call_mlaas_function
from app.exceptions import MlaasRequestError
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from route_utils import get_current_user, get_request_id
from utils.logger import Logger
from app.models.user import User

router = APIRouter(dependencies=[Depends(get_current_user)])
logger = Logger('template_crud')


@router.post("/update_template", response_model=UpdateTemplateResponse)
async def update_template(data: UpdateTemplateRequest, current_user: User = Depends(get_current_user)):
    '''
    將 Feature DB 中的 template 資訊更新
    '''
    rid = get_request_id()
    logger.logger.extra['request_id'] = rid
    logger.logger.extra['user_id'] = current_user.user_id

    form = UpdateTemplateForm(data)
    await form.load_data()
    if await form.is_valid():

        inputs = {
            'system_id': 'GPOCR_WEB',
            'business_category': [],
            'user_id': current_user.user_id,
            'template_id': form.template_id,
            'points_list': form.points_list,
            'template_name': form.template_name,
        }
        input_data = {
            "business_unit": "C170",
            "request_id": rid,
            "inputs": jsonable_encoder(inputs)
        }
        try:
            outputs = await async_call_mlaas_function(input_data, 'template_crud/update_template', project='TEMPLATE', logger=logger, timeout=60)
        except MlaasRequestError as e:
            raise e
        except Exception as e:
            logger.error({'error_msg': str(e)})
            raise CustomException(status_code=500, message=str(e))
        return UpdateTemplateResponse(template_id=outputs['template_id'])
    logger.error({'error_msg': {'form is not valid': {'errors': form.errors}}})
    raise CustomException(status_code=400, message=form.errors)
