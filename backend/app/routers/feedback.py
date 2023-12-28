from app.schema.feedback import FeedbackRequest, FeedbackResponse
from utils.logger import Logger
from route_utils import get_current_user, async_call_mlaas_function
from app.models.user import User

import uuid
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic.typing import List
from aioredis import Redis
import asyncio
from typing import List
from fastapi import Request
import json


router = APIRouter(dependencies=[Depends(get_current_user)])
logger = Logger('feedback')


# Modify your endpoint to accept a list of FeedbackRequest
from fastapi import FastAPI, Depends
from typing import List
import asyncio
import uuid
from your_module import FeedbackRequest, User, get_current_user, async_call_mlaas_function, logger

app = FastAPI()

@app.post("/feedback", summary="Batch Feedback")
async def batch_feedback(
    feedback_requests: List[FeedbackRequest],
    current_user: User = Depends(get_current_user),
):
    action = 'feedback/feedback'
    rid = str(uuid.uuid4())
    logger.logger.extra['request_id'] = rid
    logger.logger.extra['user_id'] = current_user.user_id

    success_count, failure_count = 0, 0
    failure_details = []

    try:
        batch_size = 10  # Set your batch size

        for i in range(0, len(feedback_requests), batch_size):
            batch = feedback_requests[i:i + batch_size]
            batch_tasks = []

            for feedback in batch:
                # Convert feedback to dict and update the user_id
                feedback_data = feedback.dict(exclude_none=True)
                feedback_data['user_id'] = current_user.user_id
                feedback_data['system_id'] = 'GPOCR'
                feedback_data['business_category'] = ['GPOCR_WEB']
                payload = {
                    "business_unit": 'C170',
                    "request_id": rid,
                    "inputs": feedback_data
                }

                # Add the task to the batch
                task = async_call_mlaas_function(payload, action, project='service', logger=logger)
                batch_tasks.append(task)

            results = await asyncio.gather(*batch_tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, Exception):
                    failure_count += 1
                    failure_details.append(str(result))
                else:
                    success_count += 1
        if failure_details:
            logger.error({action: {'failure_details': failure_details, 'success_count': success_count, 'failure_count': failure_count}})
        if failure_count == len(feedback_requests):
            return {"status_code": '4000', "status_msg": 'All feedback requests failed', "err_details": failure_details}
        elif failure_count == 0:
            return {"status_code": '0000', "status_msg": f'Feedback success.'}
        else:
            return {"status_code": '4001', "status_msg": f'Feedback partially successful. Success: {success_count}, Failures: {failure_count}', "err_details": failure_details}

    except Exception as ex:
        logger.error({'error_msg': str(ex), 'action': action})
        return {"status_code": '5000', "status_msg": 'Internal Server Error', "err_detail": str(ex)}

