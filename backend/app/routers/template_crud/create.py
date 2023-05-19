from app import response_table
from app.exceptions import CustomException, MlaasRequestError
from app.forms.template_crud.create import CreateTemplateForm
from app.schema.template_crud.create import (CreateTemplateRequest,
                                             CreateTemplateResponse)
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from logger import Logger
from route_utils import call_mlaas_function, init_log, verify_token

router = APIRouter()
logger = Logger(__name__)


@router.post("/create_template", response_model=CreateTemplateResponse, dependencies=[Depends(verify_token)])  # responses={},
async def create_template(request: CreateTemplateRequest):
    '''
    將前端標注的點位和上傳的圖片傳至 mlaas 對應的 api
    '''
    form = CreateTemplateForm(request)
    uid, rid, log_main = init_log('template_create', logger)
    await form.load_data()
    if await form.is_valid():
        inputs = {
            'user_id': uid,
            'image': form.image,
            'points_list': form.points_list,
            'template_name': form.template_name
        }
        input_data = {
            "business_unit": "C170",
            "request_id": rid,
            "inputs": jsonable_encoder(inputs)
        }

        outputs = call_mlaas_function(input_data, 'template_crud/create_template', project='GP', logger=logger, timeout=60)
        status_code = outputs['outputs']['status_code']
        if status_code == '0000':
            return CreateTemplateResponse(
                template_id=outputs['outputs']['template_id'],
                status_code='0000',
                status_msg='OK'
            )
        elif status_code == '5401':
            logger.error({**log_main, 'error_msg': response_table.status_uniqueviolation})
            raise MlaasRequestError(**response_table.status_uniqueviolation)
        elif status_code == '5402':
            logger.error({**log_main, 'error_msg': response_table.status_image_type_error})
            raise MlaasRequestError(**response_table.status_image_type_error)
        else:
            logger.error({**log_main, 'error_msg': outputs['outputs']})
            raise MlaasRequestError(status_code, outputs['outputs']['status_msg'])
    logger.error({**log_main, 'error_msg': {'form is not valid': {'errors': form.errors}}})
    raise CustomException(status_code=400, message=form.errors)
