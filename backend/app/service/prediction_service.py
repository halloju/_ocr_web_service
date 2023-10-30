import base64
import json
import os
import uuid
from typing import Tuple, Dict, Any

from route_utils import get_redis_taskname
from app.exceptions import MlaasRequestError


class IPredictionService:
    async def predict_for_task(self, file, task, action, input_params) -> Any:
        raise NotImplementedError(
            "This method should be implemented by subclasses")


class CVOcrPredictionService(IPredictionService):
    def __init__(self, image_storage, prediction_api, conn, logger, request_id):
        self.image_storage = image_storage
        self.prediction_api = prediction_api
        self.conn = conn
        self.logger = logger
        self.request_id = request_id

    async def predict_for_task(self, file, task, action, input_params):
        # Store image data
        image_id, encoded_data = await self.image_storage.store_image_data(file)
        try:
            self.logger.error('call prediction api')
            # Call prediction API
            data_pred = await self.prediction_api.call_prediction_api(encoded_data, input_params, self.request_id)

            # Process the prediction result
            task.mark_as_processing(
                data_pred['predict_class'], data_pred['image_cv_id'])
            self.logger.info(task.to_dict())

            # Store task in Redis
            await self.conn.set(get_redis_taskname(task.task_id), json.dumps(task.to_dict()))

            return task
        except MlaasRequestError as e:
            task.mark_as_failed('', '', e.mlaas_code, e.message)
        except Exception as exc:
            self.logger.error({
                'predict': {
                    'error_msg': str(exc),
                    'image_id': image_id,
                    'action': action,
                    'input_params': input_params
                }
            })
            task.mark_as_failed('', '', '5001', 'unknown error')
            await self.conn.set(get_redis_taskname(task.task_id), json.dumps(task.to_dict()))
            return task


# class PredictionService:
#     def __init__(self, redis_pool, logger, request_id):
#         self.image_storage = ImageStorage(redis_pool)
#         self.prediction_api = PredictionAPI(logger)
#         self.conn = redis_pool
#         self.logger = logger
#         self.rid = request_id

#     async def predict_for_task(self, file, task, action, input_params):
#         image_id, encoded_data = await self.image_storage.store_image_data(file)
#         try:
#             data_pred = await self.prediction_api.call_prediction_api(encoded_data, action, input_params, self.rid)
#             task.mark_as_processing(
#                 data_pred['predict_class'], data_pred['image_cv_id'])
#             self.logger.info(task.to_dict())

#         except MlaasRequestError as e:
#             task.mark_as_failed('', '', e.mlaas_code, e.message)
#         except Exception as e:
#             self.logger.error({
#                 'predict': {
#                     'error_msg': str(e),
#                     'image_id': image_id,
#                     'action': action,
#                     'input_params': input_params
#                 }
#             })
#             task.mark_as_failed('', '', '5001', 'unknown error')

#         # Store task in Redis
#         await self.conn.set(get_redis_taskname(task.task_id), json.dumps(task.to_dict()))

#         return task
