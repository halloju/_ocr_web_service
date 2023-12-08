from app.schema.feedback import FeedbackRequest, FeedbackResponse
from utils.logger import Logger
from route_utils import get_current_user, async_call_mlaas_function
from app.models.user import User

import uuid
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic.typing import List
from aioredis import Redis


router = APIRouter(dependencies=[Depends(get_current_user)])
logger = Logger('feedback')


@router.post("/feedback", summary="回饋")
async def feedback(
    inputs: FeedbackRequest,
    current_user: User = Depends(get_current_user),
):
    '''
    Call feedback api
    '''
    action = 'feedback'
    rid = str(uuid.uuid4())
    logger.logger.extra['request_id'] = rid
    logger.logger.extra['user_id'] = current_user.user_id
    
    try:
        response = async_call_mlaas_function(inputs, action, project='service')
        return JSONResponse(status_code=200, content=response.json())
    except Exception as ex:
        logger.error({'error_msg': str(ex), 'action': action})
        return JSONResponse(status_code=400, content=[])