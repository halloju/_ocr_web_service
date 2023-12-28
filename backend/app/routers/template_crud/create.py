
from app.exceptions import CustomException, MlaasRequestError
from app.forms.template_crud.create import CreateTemplateForm
from app.schema.template_crud.create import (CreateTemplateRequest,
                                             CreateTemplateResponse)
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from route_utils import async_call_mlaas_function
from route_utils import get_current_user, get_request_id
from utils.logger import Logger
from app.models.user import User


router = APIRouter(dependencies=[Depends(get_current_user)])
logger = Logger('template_crud')


@router.post("/create_template", response_model=CreateTemplateResponse)
async def create_template(data: CreateTemplateRequest, current_user: User = Depends(get_current_user)):
    '''
    將前端標注的點位和上傳的圖片傳至 mlaas 對應的 api
    '''
    rid = get_request_id()
    logger.logger.extra['request_id'] = rid
    logger.logger.extra['user_id'] = current_user.user_id
    
    form = CreateTemplateForm(data)
    await form.load_data()
    if await form.is_valid():
        inputs = {
            'system_id': 'GPOCR_WEB',
            'business_category': [],
            'user_id': current_user.user_id,
            'image': form.image,
            'points_list': form.points_list,
            'template_name': form.template_name
        }
        input_data = {
            "business_unit": "C170",
            "request_id": rid,
            "inputs": jsonable_encoder(inputs)
        }
        try:
            outputs = await async_call_mlaas_function(input_data, 'template_crud/create_template', project='TEMPLATE', logger=logger, timeout=60)
        except MlaasRequestError as e:
            logger.info({'error_msg': e.message})
            raise e
        except Exception as e:
            logger.error({'error_msg': str(e)})
            raise CustomException(status_code=500, message=str(e))
        return CreateTemplateResponse(
            template_id=outputs['template_id'],
            status_code='0000',
            status_msg='OK'
        )

    logger.error({'error_msg': {'form is not valid': {'errors': form.errors}}})
    raise CustomException(status_code=400, message=form.errors)
