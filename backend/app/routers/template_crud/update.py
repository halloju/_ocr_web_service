from app.exceptions import CustomException
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from app.schema.template_crud.update import UpdateTemplateRequest, UpdateTemplateResponse
from app.forms.template_crud.update import UpdateTemplateForm
from route_utils import async_call_mlaas_function
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
        try:
            outputs = await async_call_mlaas_function(input_data, 'template_crud/update_template', project='GP', logger=logger)
        except MlaasRequestError as e:
            raise e
        except Exception as e:
            logger.error({'error_msg': str(e)})
            raise CustomException(status_code=500, message=str(e))
        return UpdateTemplateResponse(template_id=outputs['template_id'])
    logger.error({'error_msg': {'form is not valid': {'errors': form.errors}}})
    raise CustomException(status_code=400, message=form.errors)
