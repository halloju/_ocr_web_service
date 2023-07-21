"""
task asyn ocr (like cv controller)
"""
import base64
import json
import os
import uuid

from route_utils import async_call_mlaas_function, get_redis_filename, get_redis_taskname
from app.exceptions import MlaasRequestError
from datetime import datetime

class AsyncPredictTask(object):
    def __init__(self, redis_pool, request):
        super().__init__()
        self.conn = redis_pool
        self.business_unit = "C170"
        self.project_names = {
            'cv-ocr': 'CV',
        }
        self.endpoints = {
            'cv-ocr': 'ocr/upload',
        }
        self.logger = request.state.logger
        self.rid = request.state.request_id

    def _get_task_info(self, status, predict_class, file_name, image_cv_id, status_msg='', err_msg=''):
        return {
            'status': status,
            'status_msg': status_msg,
            'predict_class': predict_class,
            'file_name': file_name,
            'image_cv_id': image_cv_id,
            'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'err_msg': err_msg
        }

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

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

    async def predict(self, image_id, action, input_params):
        try:
            file_name = await self.conn.get(get_redis_filename(image_id))
            encoded_data = await self.conn.get(image_id)
            input_data = self._get_req_info(encoded_data, input_params)
            data_pred = await async_call_mlaas_function(
                input_data,
                action=self.endpoints[action],
                project=self.project_names[action],
                logger=self.logger
            )
            predict_class = data_pred['predict_class']
            self.logger.debug({'predict': {'image_id': image_id, 'response_index ': list(data_pred.keys())}})
            # Return the prediction result
            return self._get_task_info('PROCESSING', predict_class, file_name, data_pred['image_cv_id'])
        except MlaasRequestError as e:
            return self._get_task_info('FAIL', predict_class, file_name, data_pred['image_cv_id'], e.mlaas_code,  e.message)
        except Exception as e:
            self.logger.error({'predict': {'error_msg': str(e), 'image_id': image_id, 'action': action, 'input_params': input_params}})
            return self._get_task_info('FAIL', '', file_name, '', '5001', 'unknown error')

    async def process_image(self, file, action: str, input_params: dict):
        image_id = str(uuid.uuid4())
        # Read and encode the file data as base64
        image_data = file.file.read()
        encoded_data = base64.b64encode(image_data).decode("utf-8")

        # Store the encoded image data in Redis using the image ID as the key
        await self.conn.set(image_id, encoded_data)
        # Store the file name in Redis using the image ID as the key
        await self.conn.set(get_redis_filename(image_id), file.filename)
        # start task prediction
        upload_result = await self.predict(image_id, action=action, input_params=input_params)
        task_id = str(upload_result["image_cv_id"]).replace('/', '-')  # 2022/10/11.../uuid  -< 2022-10-11...-uuid
        task_info = {**upload_result, 'url_result': f'/ocr/result/{task_id}', 'image_id': image_id}
        self.logger.info(task_info)

        await self.conn.set(get_redis_taskname(task_id), json.dumps(task_info))
        return task_info
