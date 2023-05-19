from app.exceptions import CustomException
from app.schema.common import Response
from fastapi import APIRouter
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from logger import Logger

from app.schema.template_crud.update import UpdateTemplateRequest, UpdateTemplateResponse
from app.forms.template_crud.update import UpdateTemplateForm
from route_utils import call_mlaas_function, init_log, verify_token
from app.exceptions import MlaasRequestError
from app import response_table


router = APIRouter()
logger = Logger(__name__)

@router.post("/update_template", response_model=UpdateTemplateResponse, dependencies=[Depends(verify_token)])
async def update_template(request: UpdateTemplateRequest):
    '''
    將 Feature DB 中的 template 資訊更新
    '''
    form = UpdateTemplateForm(request)
    uid, rid, log_main = init_log('template_upload', logger)
    await form.load_data()
    if await form.is_valid():
        
        inputs = {
            'user_id': uid,
            'template_id': form.template_id,
            'points_list': form.points_list,
            'template_name': form.template_name,
        }
        input_data = {
            "business_unit": "C170",
            "request_id": rid,
            "inputs": jsonable_encoder(inputs)
        }
        outputs = call_mlaas_function(input_data, 'template_crud/update_template', project='GP', logger=logger)
        status_code = outputs['outputs']['status_code']
        if status_code == '0000':
            new_template_id = outputs['outputs']['template_id']
            return UpdateTemplateResponse(template_id=new_template_id)
        elif status_code == '5407':
            logger.error({**log_main, 'error_msg': response_table.status_templateexisterror})
            raise MlaasRequestError(**response_table.status_templateexisterror)
        else:
            logger.error({**log_main, 'error_msg': outputs['outputs']})
            raise MlaasRequestError(status_code, outputs['outputs']['status_msg'])
    logger.error({**log_main, 'error_msg': {'form is not valid': {'errors': form.errors}}})
    raise CustomException(status_code=400, message=form.errors)
