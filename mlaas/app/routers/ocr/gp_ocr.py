from app.database import get_db
from app.exceptions import CustomException
# from app.schema.common import Response
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.schema.ocr.gp_ocr import GpocrRequest
from app.forms.ocr.gp_ocr import GpocrForm
from app.services.ocr.gp_ocr import gp_ocr as service_gp_ocr
from app.schema.ocr.gp_ocr import GpocrResponse


from app.router_schema import mlaas_item_generator
from fastapi.encoders import jsonable_encoder
from app.route_utils import get_output_template
from copy import deepcopy
import uuid
import time

from app.api_config import http_responses


Input, Output = mlaas_item_generator('Gpocr', GpocrRequest, GpocrResponse)


router = APIRouter()


@router.post("/gp_ocr", response_model=Output, responses=http_responses)  # responses={},
async def gp_ocr(request: Input, db: Session = Depends(get_db)):
    '''
    將 image 影像上傳至 MinIO, 並進行全文辨識，將辨識結果存入 db
    '''
    start_time = time.time()
    req_data = jsonable_encoder(request)
    trace_id = str(uuid.uuid4())
    output_template = get_output_template()
    output = deepcopy(output_template)
    output.update(
        business_unit=req_data['business_unit'],
        request_id=req_data['request_id'],
        trace_id=trace_id,
        request_time=start_time
    )
    status_dict = {
        '0001': 'code error',
        '5401': 'unique violation',
        '5402': 'image type error'
    }
    if req_data['request_id'] in status_dict:
        end_time = time.time()
        duration_time = round((end_time - start_time), 4)
        result = {
            'status_code': req_data['request_id'],
            'status_msg': status_dict[req_data['request_id']]
        }
        output.update(response_time=end_time, duration_time=duration_time, outputs=result)
        return Output(**output)
    
    data = GpocrRequest(**req_data['inputs'])
    form = GpocrForm(data)
    await form.load_data()
    if await form.is_valid():
        ocr_image_info = GpocrRequest(
            image=form.image)
        image_cv_id, ocr_results = service_gp_ocr(ocr_image_info=ocr_image_info, db=db)

        end_time = time.time()
        duration_time = round((end_time - start_time), 4)
        result = {
            'image_cv_id': image_cv_id,
            'data_results': ocr_results,
            'status_code': '0000',
            'status_msg': 'OK'
        }
        output.update(response_time=end_time, duration_time=duration_time, outputs=result)
        return Output(**output)
    raise CustomException(status_code=401, message=form.errors)
