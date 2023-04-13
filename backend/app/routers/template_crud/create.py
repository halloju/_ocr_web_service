import json

from app import response_table
from app.exceptions import CustomException, MlaasRequestError
from app.forms.template_crud.create import CreateTemplateForm
from app.schema.common import Response
from app.schema.template_crud.create import (CreateTemplateRequest,
                                             CreateTemplateResponse)
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from logger import Logger
from route_utils import call_mlaas_function, get_user_id, get_request_id

router = APIRouter()
logger = Logger('template_create')


@router.post("/create_template", response_model=CreateTemplateResponse)  # responses={},
async def create_template(request: CreateTemplateRequest):
    '''
    將 template 影像上傳至 MinIO, 並將其餘資訊存入 Feature DB
    '''
    log_main = {'user_id': uid, 'request_id': rid, 'action': action}
    form = CreateTemplateForm(request)
    await form.load_data()
    if await form.is_valid():
        uid = get_user_id()
        rid = get_request_id()
        action = 'template_crud/create_template'
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
        logger.info(log_main)
        outputs = call_mlaas_function(input_data, action, project='GP', logger=logger, timeout=60)
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
