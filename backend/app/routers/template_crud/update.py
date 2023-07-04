from app.exceptions import CustomException
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from app.schema.template_crud.update import UpdateTemplateRequest, UpdateTemplateResponse
from app.forms.template_crud.update import UpdateTemplateForm
from route_utils import call_mlaas_function
from app.exceptions import MlaasRequestError
from app import response_table
from starlette.requests import Request

router = APIRouter()

@router.post("/update_template", response_model=UpdateTemplateResponse)
async def update_template(data: UpdateTemplateRequest, request: Request):
    '''
    將 Feature DB 中的 template 資訊更新
    '''
    user_id = request.state.user_id
    rid = request.state.request_id
    logger = request.state.logger
    form = UpdateTemplateForm(data)
    await form.load_data()
    if await form.is_valid():
        
        inputs = {
            'user_id': user_id,
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
            logger.error({'error_msg': response_table.status_templateexisterror})
            raise MlaasRequestError(**response_table.status_templateexisterror)
        else:
            logger.error({'error_msg': outputs['outputs']})
            raise MlaasRequestError(status_code, outputs['outputs']['status_msg'])
    logger.error({'error_msg': {'form is not valid': {'errors': form.errors}}})
    raise CustomException(status_code=400, message=form.errors)
