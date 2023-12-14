import uuid
from typing import Any

from route_utils import get_redis_taskname
from app.models.task import Task
from app.exceptions import MlaasRequestError
from app.constants import remittance_points

import traceback


class IPredictionService:
    async def predict_for_task(self, file, action, input_params) -> Any:
        raise NotImplementedError(
            "This method should be implemented by subclasses")


class ControllerOcrPredictionService(IPredictionService):
    def __init__(self, image_storage, prediction_api, conn, logger, request_id):
        self.image_storage = image_storage
        self.prediction_api = prediction_api
        self.conn = conn
        self.logger = logger
        self.request_id = request_id

    async def predict_for_task(self, file, action, input_params):
        # Store image data
        task, encoded_data = await Task.create_and_store_image(file, self.image_storage)
        if task.status == 'FAIL':
            return task
        try:
            # Call prediction API
            data_pred = await self.prediction_api.call_prediction_api(encoded_data, input_params, self.request_id, action)

            predict_class = data_pred.get('predict_class', '')
            # Process the prediction result
            task.mark_as_processing(
                data_pred['image_cv_id'], predict_class=predict_class)

            # Store task in Redis
            task_dict = task.to_dict()
            for key, value in task_dict.items():
                await self.conn.hset(get_redis_taskname(task.task_id), key, value)

            return task

        except MlaasRequestError as exc:
            self.logger.error({
                'predict_service': {
                    'error_msg': str(exc.message),
                    'action': action,
                    'input_params': input_params,
                    'status_code': exc.mlaas_code
                }
            })
            task.mark_as_failed('', '', exc.mlaas_code, exc.message)

        except Exception as exc:
            self.logger.error({
                'controller_predict_service': {
                    'error_msg': str(exc),
                    'action': action,
                    'input_params': input_params,
                    'status_code': '5001'
                }
            })
            task.mark_as_failed('', '', '5001', 'unknown error')
            # Store task in Redis
            task_dict = task.to_dict()
            for key, value in task_dict.items():
                await self.conn.hset(get_redis_taskname(task.task_id), key, value)
            return task


class NonControllerOcrPredictionService(IPredictionService):
    def __init__(self, image_storage, prediction_api, conn, logger, request_id):
        self.image_storage = image_storage
        self.prediction_api = prediction_api
        self.conn = conn
        self.logger = logger
        self.request_id = request_id

    def _get_predict_data(self, data_pred, action):
        # Mapping action to their respective processing functions
        action_processing = {
            'CHECK/front_out_predict': self._process_front_out_predict,
            'CHECK/back_predict': self._process_back_predict,
            'REMIT/predict': self._process_ocr_predict,  # remittance
        }

        process_function = action_processing.get(action)
        if process_function:
            return process_function(data_pred)
        else:
            self.logger.error({
                'non_controller_predict_service': {
                    'error_msg': 'Unknown action',
                    'action': action}
                }
            )
            # Handle unknown action
            return data_pred

    def _process_front_out_predict(self, data_pred):
        return self._format_prediction_data(data_pred, exclude_keys=['status_code', 'status_msg', 'err_detail'])

    def _process_back_predict(self, data_pred):
        return self._format_prediction_data(data_pred, exclude_keys=['status_code', 'status_msg', 'err_detail'])

    def _process_ocr_predict(self, data_pred):
        exclude_keys = ['status_code', 'status_msg', 'err_detail']
        return [{'tag': key, 'text': value, 'points': remittance_points[key]}
                for key, value in data_pred.items() if key not in exclude_keys]

    def _format_prediction_data(self, data_pred, exclude_keys):
        return [{'tag': key, 'text': value} for key, value in data_pred.items() if key not in exclude_keys]

    async def predict_for_task(self, file, action, input_params):
        # Store image data
        task, encoded_data = await Task.create_and_store_image(file, self.image_storage)
        if task.status == 'FAIL':
            return task
        try:
            # Call prediction API
            response = await self.prediction_api.call_prediction_api(encoded_data, input_params, self.request_id, action)

            data_pred = self._get_predict_data(response, action)
            # Process the prediction result
            task.mark_as_success(image_cv_id=str(
                uuid.uuid4()), result=data_pred)

            return task

        except MlaasRequestError as exc:
            self.logger.error({
                'non_controller_predict_service': {
                    'error_msg': str(exc),
                    'action': action,
                    'input_params': input_params
                }
            })
            task.mark_as_failed('', '', exc.mlaas_code, exc.message)
            self.logger.error({
                'non_controller_predict_service': {
                    'error_msg': str(exc.message),
                    'action': action,
                    'input_params': input_params,
                    'status_code': exc.mlaas_code
                }
            })

        except Exception as exc:
            self.logger.error({
                'non_controller_predict_service': {
                    'error_msg': str(exc),
                    'action': action,
                    'input_params': input_params,
                    'status_code': '5001'
                }
            })
            task.mark_as_failed('', '', '5001', 'unknown error')
            return task
