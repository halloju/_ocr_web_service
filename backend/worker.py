import os
import json
import time
import uuid
from celery import Task
from celery.exceptions import MaxRetriesExceededError
import requests
import logging

from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "amqp://rabbitmq")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

class PredictTask(Task):
    def __init__(self):
        super().__init__()
        self.url = os.environ.get("MLAAS_URL", "http://localhost:7777/ocr/gp_ocr")
        
    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def predict(self, image_id):
        try:
            encoded_data = celery.backend.get(image_id)
            # Process the image using the ML model
            data_pred = requests.post(self.url, data={
                "image": encoded_data,
                "image_complexity": "medium",
                "model_name": "dbnet_v0+cht_ppocr_v1"}).json()

            # Return the prediction result
            return {'status': 'SUCCESS', 'result': data_pred}
        except Exception as ex:
            logging.error(ex)
            raise ex
            # try:
            #     logging.error(ex)
            #     raise
            #     # Retry the task in 2 seconds if it fails
            #     self.retry(countdown=2)
            # except MaxRetriesExceededError as ex:
            #     # Return a failure result if the maximum number of retries is reached
            #     return {'status': 'FAIL', 'result': 'max retries achieved'}
    
@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True

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
def predict_image(self, image_id):
    try:
        # encoded_data = celery.backend.get(image_id)
        # logging.info(f"Predicting image {image_id}...")
        response = self.predict(image_id)
        logging.info(f"Prediction result: {response}")
        data_pred = response.json()
        return {'status': 'SUCCESS', 'result': data_pred}
    except Exception as ex:
        logging.error(ex)
        raise ex
        # try:
        #     self.retry(countdown=2)
        # except MaxRetriesExceededError as ex:
        #     return {'status': 'FAIL', 'result': 'max retried achieved'}