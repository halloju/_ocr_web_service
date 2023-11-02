import base64
import json
import os
import uuid
from typing import Tuple, Dict, Any

from route_utils import get_redis_taskname
from app.models.task import Task
from app.exceptions import MlaasRequestError

import traceback


class IPredictionService:
    async def predict_for_task(self, file, action, input_params) -> Any:
        raise NotImplementedError(
            "This method should be implemented by subclasses")


class OcrPredictionService(IPredictionService):
    def __init__(self, image_storage, prediction_api, conn, logger, request_id):
        self.image_storage = image_storage
        self.prediction_api = prediction_api
        self.conn = conn
        self.logger = logger
        self.request_id = request_id

    async def predict_for_task(self, file, action, input_params):
        # Store image data
        task, encoded_data = await Task.create_and_store_image(file, self.image_storage)
        self.logger.error({'store image'})
        if task.status == 'FAIL':
            return task
        try:
            # Call prediction API
            data_pred = await self.prediction_api.call_prediction_api(encoded_data, input_params, self.request_id)
            
            predict_class = data_pred.get('predict_class', '')
            # Process the prediction result
            task.mark_as_processing(
                data_pred['image_cv_id'], predict_class = predict_class)

            # Store task in Redis
            task_dict = task.to_dict()
            for key, value in task_dict.items():
                await self.conn.hset(get_redis_taskname(task.task_id), key, value)

            return task
        
        except MlaasRequestError as exc:
            self.logger.error({
                'predict_service': {
                    'error_msg': str(exc),
                    'action': action,
                    'input_params': input_params
                }
            })
            task.mark_as_failed('', '', exc.mlaas_code, exc.message)
            
        except Exception as exc:
            # traceback.print_exc()
            self.logger.error({
                'predict_service': {
                    'error_msg': str(exc),
                    'action': action,
                    'input_params': input_params
                }
            })
            task.mark_as_failed('', '', '5001', 'unknown error')
            # Store task in Redis
            task_dict = task.to_dict()
            for key, value in task_dict.items():
                await self.conn.hset(get_redis_taskname(task.task_id), key, value)
            return task
