from app.database import get_db
from app.exceptions import CustomException
from app.schema.common import Response
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

# from app.services.template_crud import read as service_read
from app.schema.template_crud.read import GetAvailableTemplatesResponse
from app.schema.template_crud.read import GetTemplateDetailResponse
from app.route_utils import get_user_id, call_mlaas_function, get_request_id
from app.exceptions import MlaasRequestError
from app import response_table

router = APIRouter()


@router.get("/get_available_templates/{user_id}", response_model=GetAvailableTemplatesResponse)
def get_available_templates(user_id: str, db: Session = Depends(get_db)):
    '''
    取得該 user_id 可用的 template 清單
    '''
    input_data = {
        "business_unit": "C170",
        "request_id": get_request_id(),
        "inputs": {'user_id': user_id}
    }
    outputs = call_mlaas_function(input_data, 'get_available_templates')
    status_code = outputs['outputs']['status_code']
    if status_code == '0000':
        return GetAvailableTemplatesResponse(
            template_infos=outputs['outputs']['template_infos']
        )
    else:
        raise MlaasRequestError(**response_table.status_mlaaserror)


@router.get("/get_template_detail/{template_id}", response_model=GetTemplateDetailResponse)
def get_template_detail(template_id: str, db: Session = Depends(get_db)):
    '''
    取得該 template 的細節
    '''
    input_data = {
        "business_unit": "C170",
        "request_id": get_request_id(),
        "inputs": {'template_id': template_id}
    }
    outputs = call_mlaas_function(input_data, 'get_template_detail')
    status_code = outputs['outputs']['status_code']
    if status_code == '0000':
        template_detail = outputs['outputs']['template_detail']
        return GetTemplateDetailResponse(
            image=template_detail['image'],
            template_name=template_detail['template_name'],
            points_list=template_detail['points_list'],
            updated_at=template_detail['updated_at']
        )
    elif status_code == '5407':
        raise MlaasRequestError(**response_table.status_templateexisterror)
    else:
        raise MlaasRequestError(**response_table.status_mlaaserror)
