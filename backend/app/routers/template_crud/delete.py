from app.exceptions import CustomException
from app.schema.common import Response
from fastapi import APIRouter
from fastapi import Depends

from app.schema.template_crud.delete import DeleteTemplateRequest
from app.forms.template_crud.delete import DeleteTemplateForm
from route_utils import get_user_id, call_mlaas_function, get_request_id
from app.exceptions import MlaasRequestError
from app import response_table

router = APIRouter()


@router.delete("/delete_template/{template_id}")
async def delete_template(template_id: str):
    '''
    將 Feature DB 中的 template 資訊刪除
    '''

    input_data = {
        "business_unit": "C170",
        "request_id": get_request_id(),
        "inputs": {'template_id': template_id}
    }
    outputs = call_mlaas_function(input_data, 'template_crud/delete_template')
    status_code = outputs['outputs']['status_code']
    if status_code == '0000':
        return Response(status_code=200)
    elif status_code == '5407':
        raise MlaasRequestError(**response_table.status_templateexisterror)
    else:
        raise MlaasRequestError(status_code, outputs['outputs']['status_msg'])
