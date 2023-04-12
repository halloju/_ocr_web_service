from app.exceptions import CustomException
from app.schema.common import Response
from fastapi import APIRouter
from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from app.schema.template_crud.update import UpdateTemplateRequest, UpdateTemplateResponse
from app.forms.template_crud.update import UpdateTemplateForm
from route_utils import get_user_id, call_mlaas_function, get_request_id
from app.exceptions import MlaasRequestError
from app import response_table
# from app.services.template_crud import update as service_update


router = APIRouter()


@router.post("/update_template", response_model=UpdateTemplateResponse)
async def update_template(request: UpdateTemplateRequest):
    '''
    將 Feature DB 中的 template 資訊更新
    '''
    form = UpdateTemplateForm(request)
    await form.load_data()
    if await form.is_valid():
        inputs = {
            'user_id': get_user_id(),
            'template_id': form.template_id,
            'points_list': form.points_list,
            'template_name': form.template_name,
        }
        input_data = {
            "business_unit": "C170",
            "request_id": get_request_id(),
            "inputs": jsonable_encoder(inputs)
        }
        outputs = call_mlaas_function(input_data, 'template_crud/update_template', project='GP')
        status_code = outputs['outputs']['status_code']
        if status_code == '0000':
            print(outputs['outputs'])
            new_template_id = outputs['outputs']['template_id']
            return UpdateTemplateResponse(template_id=new_template_id)
        elif status_code == '5407':
            raise MlaasRequestError(**response_table.status_templateexisterror)
        else:
            raise MlaasRequestError(status_code, outputs['outputs']['status_msg']) 
    raise CustomException(status_code=400, message=form.errors)
