import base64
import json
import os
import uuid

from route_utils import async_call_mlaas_function, get_redis_filename, get_redis_taskname
from app.exceptions import MlaasRequestError


class PredictionService:
    '''
    Storing the image data.
    Making a prediction using the stored data.
    Updating the task with the prediction results or errors.
    '''

    def __init__(self, redis_pool, logger, request_id):
        self.conn = redis_pool
        self.logger = logger
        self.rid = request_id
        self.business_unit = "C170"
        self.project_names = {
            'cv-ocr': 'CV',
        }
        self.endpoints = {
            'cv-ocr': 'ocr/upload',
        }

    async def _store_image_data(self, file):
        image_id = str(uuid.uuid4())
        image_data = file.file.read()
        encoded_data = base64.b64encode(image_data).decode("utf-8")

        # Store the encoded image data and filename in Redis
        await self.conn.set(image_id, encoded_data)
        await self.conn.set(get_redis_filename(image_id), file.filename)

        return image_id, encoded_data

    async def _call_prediction_api(self, encoded_data, action, input_params):
        input_data = self._get_req_info(encoded_data, input_params)
        return await async_call_mlaas_function(
            input_data,
            action=self.endpoints[action],
            project=self.project_names[action],
            logger=self.logger
        )

    def _get_req_info(self, encoded_data, input_params):
        return {
            "business_unit": self.business_unit,
            "request_id": self.rid,
            "inputs": {
                "system_id": "CH0052_OLIU",
                "business_category": [
                    "OPEN_ACCOUNT_BANK",
                    "UNSECURED_LOAN"
                ],
                "image": encoded_data,
                "action": "RECOGNITION",
                "source": "INTERNAL",
                "clearness_type": "MANUAL",
                "clearness_threshold": 2,
                "callback": [
                    {
                        "callback_url": f"{os.environ.get(f'GP_CALLBACK_MLAAS_URL')}/callback/controller_callback/v1",
                        "callback_body": "{\"business_unit\": \"B31\", \"request_id\": \"test\", \"inputs\": {\"image_cv_id\": \"${image_cv_id}\", \"recognition_status\": \"${recognition_status}\", \"ocr_results\": \"${ocr_results}\"}}",
                        "callback_headers": json.dumps({
                            "x-client-id": os.environ.get(f'MLAAS_XClient'),
                            "Authorization": os.environ.get(f'MLAAS_JWT')})
                    }
                ],
                **input_params  # "image_class": "PASSBOOK_COVER"
            }
        }

    async def predict_for_task(self, file, task, action, input_params):
        image_id, encoded_data = await self._store_image_data(file)
        try:
            data_pred = await self._call_prediction_api(encoded_data, action, input_params)
            task.mark_as_processing(
                data_pred['predict_class'], data_pred['image_cv_id'])
            self.logger.info(
              task.to_dict()
            )
              
        except MlaasRequestError as e:
            task.mark_as_failed('', '', e.mlaas_code, e.message)
        except Exception as e:
            self.logger.error({
                'predict': {
                    'error_msg': str(e),
                    'image_id': image_id,
                    'action': action,
                    'input_params': input_params
                }
            })
            task.mark_as_failed('', '', '5001', 'unknown error')

        # Store task in Redis
        await self.conn.set(get_redis_taskname(task.task_id), json.dumps(task.to_dict()))

        return task
