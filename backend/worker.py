import logging
import os
import json
import requests
import uuid
from celery import Celery
from celery import Task

from route_utils import get_request_id, call_mlaas_function

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "amqp://rabbitmq")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

class PredictTask(Task):
    def __init__(self):
        super().__init__()
        self.business_unit = "C170"
        self.request_id = get_request_id()
        self.project_names = {
            'gp_ocr': 'GP',
            'template_ocr': 'GP',
            'check_front': 'CHECK',  # 支票正面
            'check_back': 'CHECK',  # 支票背面
            'remittance': 'REMIT' # 匯款單
        }
        self.endpoints = {
            'gp_ocr': 'ocr/gp_ocr',
            'template_ocr': 'ocr/template_ocr',
            'check_front': 'ocr/front_out_predict',  # 支票正面
            'check_back': 'ocr/back_predict',  # 支票背面
            'remittance': 'ocr/predict' # 匯款單
            
        }
        
    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def predict(self, image_id, action, input_params):
        try:
            encoded_data = celery.backend.get(image_id)
            input_data = {
                "business_unit": self.business_unit,
                "request_id": self.request_id,
                "inputs": {
                    "image": encoded_data.decode("utf-8"),
                    **input_params
                }
            }
            data_pred = call_mlaas_function(input_data, action=self.endpoints[action], project= self.project_names[action], timeout=60)
            if action in ['check_front', 'check_back', 'remittance']:
                if data_pred['outputs']['status_code'] == '0000':
                    data_pred['outputs']['data_results'] = [{'tag': key, 'text': value} for key, value in data_pred['outputs'].items() if key not in ['status_code', 'status_msg', 'err_detail']]
            # Return the prediction result
            return data_pred
        except Exception as ex:
            logging.error(ex)
            raise ex

@celery.task(name="upload_to_redis")
def upload_to_redis(image_data):
    try:
        image_id = str(uuid.uuid4())
        # Store image data in Redis with 1-day expiration
        celery.backend.set(image_id, image_data)
        celery.backend.expire(image_id, 86400)
        return {'status': 'SUCCESS', 'image_id': image_id}
    except:
        return {'status': 'FAIL'}

@celery.task(name="get_from_redis")
def get_from_redis(task_id):
    try:
        full_key = f'celery-task-meta-{task_id}'
        task_result = celery.backend.get(full_key)
        if task_result is None:
            return {'status': 'ERROR'}
        task_result_dict = json.loads(task_result.decode('utf-8'))
        return task_result_dict["result"]
    except:
        return {'status': 'FAIL'}

@celery.task(ignore_result=False, bind=True, base=PredictTask)
def predict_image(self, image_id, action, input_params):
    try:
        response = self.predict(image_id, action=action, input_params=input_params)
        status_code = response['outputs']['status_code']
        data_pred = str(response['outputs']['data_results']) if status_code == '0000' else str(response['outputs']['status_str'])
        status = 'SUCCESS' if status_code == '0000' else 'FAIL'

        # Get the file name from Redis using the image ID as the key
        file_name = celery.backend.get(image_id + '_file_name').decode("utf-8")

        return {'status': status, 'result': data_pred, 'file_name': file_name}

    except Exception as ex:
        logging.error(ex)
