from app.schema.feedback import BatchFeedbackRequest, FeedbackResponse
from utils.logger import Logger
from route_utils import get_current_user, async_call_mlaas_function
from app.models.user import User

import uuid
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic.typing import List
from aioredis import Redis
import asyncio


router = APIRouter(dependencies=[Depends(get_current_user)])
logger = Logger('feedback')


# Modify your endpoint to accept a list of FeedbackRequest
@router.post("/batch-feedback", summary="批次回饋")
async def batch_feedback(
    feedback_requests: BatchFeedbackRequest,
    current_user: User = Depends(get_current_user),
):
    '''
    Call feedback api for a batch of feedback requests
    '''
    action = 'feedback'
    rid = str(uuid.uuid4())
    logger.logger.extra['request_id'] = rid
    logger.logger.extra['user_id'] = current_user.user_id

    try:
        tasks = []
        batch_size = 10  # Set your batch size

        for i in range(0, len(feedback_requests), batch_size):
            batch = feedback_requests[i:i + batch_size]
            batch_tasks = [async_call_mlaas_function(feedback, action, project='service') for feedback in batch]
            results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            # Process results and handle any exceptions
            for result in results:
                if isinstance(result, Exception):
                    logger.error({'error_msg': str(result), 'action': action})
                else:
                    tasks.append(result.json())

        return JSONResponse(status_code=200, content=tasks)

    except Exception as ex:
        logger.error({'error_msg': str(ex), 'action': action})
        return JSONResponse(status_code=400, content=[])
