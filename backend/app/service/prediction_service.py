import uuid
from typing import Any
import base64

from route_utils import get_redis_taskname
from app.models.task import Task
from app.exceptions import MlaasRequestError
from app.exceptions import TaskProcessingException
from app.exceptions import PredictionAPIException
from app.exceptions import GeneralException
from app.constants import remittance_points


async def encode_file(file):
    binary_data = await file.read()
    return base64.b64encode(binary_data).decode("utf-8")
        

class IPredictionService:
    async def predict_for_task(self, file, action, input_params) -> Any:
        raise NotImplementedError(
            "This method should be implemented by subclasses")


class ControllerOcrPredictionService(IPredictionService):
    def __init__(self, prediction_api, conn, logger, request_id):
        # self.image_storage = image_storage
        self.prediction_api = prediction_api
        self.conn = conn
        self.logger = logger
        self.request_id = request_id

    async def predict_for_task(self, file, action, input_params, special_rid: str=None):
        ## Encode file
        encoded_data = await encode_file(file)
        if special_rid:
            rid = special_rid
        else:
            rid = str(uuid.uuid4())
        try:
            # Call prediction API
            data_pred = await self.prediction_api.call_prediction_api(encoded_data, input_params, rid, action)

            predict_class = data_pred.get('predict_class', '')
            image_cv_ids = data_pred.get('image_cv_id')
            # controller predict API returns a single image_cv_id
            if isinstance(image_cv_ids, str):
                image_cv_ids = [image_cv_ids]
            
            tasks = []
            # Create task for each image_cv_id from the prediction result
            for idx, image_cv_id in enumerate(image_cv_ids):
                task = Task(file_name=file.filename, series_num=idx, image_cv_id=image_cv_id, predict_class=predict_class)
                task.mark_as_processing(image_cv_id, predict_class)
                tasks.append(task)

                # Store task in Redis
                await self._store_task_in_redis(task)


            return tasks

        except MlaasRequestError as exc:
            self.logger.error({
                'predict_service': {
                    'mlaas_rid': rid,
                    'backend_rid': self.request_id,
                    'error_msg': str(exc.message),
                    'action': action,
                    'input_params': input_params,
                    'status_code': exc.mlaas_code
                }
            })
            raise PredictionAPIException(task, exc)

        except Exception as exc:
            self.logger.error({
                'predict_service': {
                    'mlaas_rid': rid,
                    'backend_rid': self.request_id,
                    'error_msg': str(exc),
                    'action': action,
                    'input_params': input_params,
                    'status_code': '5001'
                }
            })
            raise GeneralException(task, exc)

    async def _store_task_in_redis(self, task: Task):
        task_dict = task.to_dict()
        task_key = get_redis_taskname(task.task_id)
        
        # Start a pipeline
        pipe = self.conn.pipeline()
        
        # Queue up all the HSET operations in the pipeline
        for key, value in task_dict.items():
            pipe.hset(task_key, key, value)
        
        # Set the TTL for the entire hash key in the pipeline
        pipe.expire(task_key, 3600)  # 3600 seconds equals 1 hour
        
        # Execute all commands in the pipeline
        await pipe.execute()


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

    async def predict_for_task(self, file, action, input_params, special_rid: str=None):
        # Store image data
        task, encoded_data = await Task.create_and_store_image(file, self.image_storage)
        if task.status == 'FAIL':
            raise TaskProcessingException(task)
        rid = str(uuid.uuid4())
        try:
            # Call prediction API
            response = await self.prediction_api.call_prediction_api(encoded_data, input_params, rid, action)

            data_pred = self._get_predict_data(response, action)
            # Process the prediction result
            task.mark_as_success(image_cv_id=rid, result=data_pred)

            return task

        except MlaasRequestError as exc:
            task.mark_as_failed('', '', exc.mlaas_code, exc.message)
            self.logger.error({
                'non_controller_predict_service': {
                    'mlaas_rid': rid,
                    'backend_rid': self.request_id,
                    'error_msg': str(exc.message),
                    'action': action,
                    'input_params': input_params,
                    'status_code': exc.mlaas_code
                }
            })
            raise PredictionAPIException(task, exc)

        except Exception as exc:
            self.logger.error({
                'non_controller_predict_service': {
                    'mlaas_rid': rid,
                    'backend_rid': self.request_id,
                    'error_msg': str(exc),
                    'action': action,
                    'input_params': input_params,
                    'status_code': '5001'
                }
            })
            task.mark_as_failed('', '', '5001', str(exc))
            raise GeneralException(task, exc)
