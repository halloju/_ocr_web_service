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
        self.gp_ocr = 'ocr/gp_ocr'
        self.template_ocr = 'ocr/template_ocr'
        self.business_unit = "C170"
        self.request_id = get_request_id()
        
    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def predict(self, image_id, image_complexity, model_name, template_id):
        try:
            encoded_data = celery.backend.get(image_id)
            # Call MLass using /template_ocr
            if template_id != "":
                input_data = {
                    "business_unit": self.business_unit,
                    "request_id": self.request_id,
                    "inputs": {
                        "image": encoded_data.decode("utf-8"),
                        "template_id": template_id,
                        "model_name": model_name
                    }
                }
                data_pred = call_mlaas_function(input_data, self.template_ocr)
            else:
                # Call MLass using /gp_ocr
                input_data = {
                    "business_unit": self.business_unit,
                    "request_id": get_request_id(),
                    "inputs": {
                        "image": encoded_data.decode("utf-8"),
                        "image_complexity": image_complexity,
                        "model_name": model_name
                    }
                }
                data_pred = call_mlaas_function(input_data, self.gp_ocr)
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
def predict_image(self, image_id, image_complexity, model_name, template_id):
    try:
        response = self.predict(image_id, image_complexity, model_name, template_id)
        if response['outputs']['status_msg'] == 'OK':
            data_pred = str(response['outputs']['ocr_results'])
        else:
            data_pred = str(response['outputs']['status_msg'])

        # Get the file name from Redis using the image ID as the key
        file_name = celery.backend.get(image_id + '_file_name').decode("utf-8")

        return {'status': 'SUCCESS', 'result': data_pred, 'file_name': file_name}

    except Exception as ex:
        logging.error(ex)
