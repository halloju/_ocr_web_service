
from app.exceptions import CustomException, MlaasRequestError
from app.forms.template_crud.create import CreateTemplateForm
from app.schema.template_crud.create import (CreateTemplateRequest,
                                             CreateTemplateResponse)
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from logger import Logger
from route_utils import async_call_mlaas_function
from starlette.requests import Request


router = APIRouter()
logger = Logger(__name__)


@router.post("/create_template", response_model=CreateTemplateResponse)  # responses={},
async def create_template(data: CreateTemplateRequest, request: Request):
    '''
    將前端標注的點位和上傳的圖片傳至 mlaas 對應的 api
    '''
    form = CreateTemplateForm(data)
    user_id = request.state.user_id
    rid = request.state.request_id
    logger = request.state.logger
    await form.load_data()
    if await form.is_valid():
        inputs = {
            'user_id': user_id,
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
            outputs = await async_call_mlaas_function(input_data, 'template_crud/create_template', project='GP', logger=logger, timeout=60)
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
