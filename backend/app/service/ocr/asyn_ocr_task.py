"""
task asyn ocr (like cv controller)
"""
import base64
import json
import os
import uuid
from urllib import parse

import redis
from route_utils import call_mlaas_function, get_redis_filename, init_log


class AsynPredictTask(object):
    def __init__(self, logger):
        super().__init__()
        redis_url = os.environ.get("LOCAL_REDIS_URL", "redis://localhost:6379")
        parse.uses_netloc.append('redis')
        url = parse.urlparse(redis_url)
        self.conn = redis.Redis(host=url.hostname, port=url.port, db=0, password=url.password, decode_responses=True)
        self.business_unit = "C170"
        self.project_names = {
            'cv-ocr': 'CV',
        }
        self.endpoints = {
            'cv-ocr': 'ocr/upload',
        }
        self.logger = logger

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def predict(self, image_id, action, input_params):
        uid, rid, log_main = init_log('asynOcr', self.logger)
        try:
            encoded_data = self.conn.get(image_id)
            input_data = {
                "business_unit": self.business_unit,
                "request_id": rid,
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
                            "callback_url": f"{os.environ.get(f'GP_MLAAS_URL')}\callback/controller_callback/v1",
                            "callback_body": "{\"business_unit\": \"B31\", \"request_id\": \"test\", \"inputs\": {\"ocr_results\": \"${ocr_results}\"}}",
                            "callback_headers": json.dumps({"x-client-id": os.environ.get(f'GP_MLAAS_XClient')})
                        }
                    ],
                    **input_params  # "image_class": "PASSBOOK_COVER"
                }
            } 
            data_pred = call_mlaas_function(
                input_data,
                action=self.endpoints[action],
                project=self.project_names[action],
                logger=self.logger,
                timeout=60
            )

            self.logger.debug({**log_main, 'predict': {'image_id': image_id, 'response_index ': list(data_pred.keys())}})
            # Return the prediction result
            return data_pred
        except Exception as e:
            self.logger.error({**log_main, 'predict': {'error_msg': str(e), 'image_id': image_id, 'action': action, 'input_params': input_params}})
            raise e


    def predict_image(self, image_id, action, input_params):
        try:
            response = self.predict(image_id, action=action, input_params=input_params)
            status_code = response['outputs']['status_code']
            status = 'PROCESSING' if status_code == '0000' else 'FAIL'
            # Get the file name from Redis using the image ID as the key
            file_name = self.conn.get(get_redis_filename(image_id))
            if status == 'PROCESSING':
                image_cv_id = response['outputs']['image_cv_id']
                predict_class = response['outputs']['predict_class']
                return {'status': status, 'predict_class': predict_class, 'file_name': file_name, 'image_cv_id': image_cv_id}
        except Exception as e:
            self.logger.error({'predict_image': {'error_msg': str(e), 'image_id': image_id, 'action': action}})
        return {'status': 'FAIL', 'err_msg': str(response['outputs']['status_msg']), 'image_cv_id': ''}

    def process_image(self, request, file, action: str, input_params: dict):
        image_id = str(uuid.uuid4())
        # Read and encode the file data as base64
        image_data = file.file.read()
        encoded_data = base64.b64encode(image_data).decode("utf-8")

        # Store the encoded image data in Redis using the image ID as the key
        self.conn.set(image_id, encoded_data, ex=86400)
        # Store the file name in Redis using the image ID as the key
        self.conn.set(get_redis_filename(image_id), file.filename, ex=86400)
        # start task prediction
        upload_result = self.predict_image(image_id, action=action, input_params=input_params)
        task_id = str(upload_result["image_cv_id"])
        self.conn.set(task_id, json.dumps({'task_id': task_id, 'status': upload_result["status"], 'url_result': f'/ocr/result/{upload_result["image_cv_id"]}', 'image_id': image_id, 'result': '', 'file_name': upload_result["file_name"]}))
        return {'task_id': task_id, 'status': upload_result["status"], 'url_result': f'/ocr/result/{upload_result["image_cv_id"]}', 'image_id': image_id}