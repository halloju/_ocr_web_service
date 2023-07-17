import json
import logging
import os
import uuid

from celery import Celery, Task
from celery.signals import after_setup_logger
from logger import config_logging
from route_utils import call_mlaas_function, get_redis_filename, get_redis_taskname

from app.constants import remittance_points
from app.exceptions import MlaasRequestError, CustomException
import mlaas_log_formatter

# 設定 celery
celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "amqp://rabbitmq")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

# 設定 logger
logger = logging.getLogger(__name__)
@after_setup_logger.connect
def config_loggers(logger, *args, **kwags):
    config_logging()

class PredictTask(Task):
    def __init__(self):
        super().__init__()
        self.business_unit = "C170"
        self.project_names = {
            'gp_ocr': 'GP',
            'template_ocr': 'GP',
            'check_front': 'CHECK',  # 支票正面
            'check_back': 'CHECK',  # 支票背面
            'remittance': 'REMIT'  # 匯款單
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
                "request_id": self.request.id,
                "inputs": {
                    "image": encoded_data.decode("utf-8"),
                    **input_params
                }
            }
        except Exception as e:
            logger.error({'predict': {'error_msg': str(e), 'image_id': image_id, 'action': action, 'input+params': input_params}})
            raise CustomException(400, 'Image not found in Redis')

        data_pred = call_mlaas_function(
            input_data,
            action=self.endpoints[action],
            project=self.project_names[action],
            logger=logger,
            timeout=60
        )
        logger.info({'predict': {'image_id': image_id, 'data_pred': list(data_pred.keys())}})
        # Return the prediction result
        return data_pred


@celery.task(name="upload_to_redis")
def upload_to_redis(image_data):
    image_id = str(uuid.uuid4())
    try:
        # Store image data in Redis with 1-day expiration
        celery.backend.set(image_id, image_data)
        celery.backend.expire(image_id, 86400)
        return {'status': 'SUCCESS', 'image_id': image_id, 'status_msg': ''}
    except Exception as e:
        logger.error({'upload_to_redis': {'error_msg': str(e), 'image_id': image_id}})
        return {'status': 'FAIL', 'status_msg': '5002'}

@celery.task(name="get_from_redis")
def get_from_redis(task_id):
    try:
        task_result = celery.backend.get(get_redis_taskname(task_id))
        if task_result is None:
            logger.error({'get_from_redis': f'task_result of id {task_id} is None'})
            return {'status': 'ERROR', 'status_msg': '5003'}
        task_result_dict = json.loads(task_result.decode('utf-8'))
        return task_result_dict["result"]
    except Exception as e:
        logger.error({'get_from_redis': {'error_msg': str(e), 'task_id': task_id}})
        return {'status': 'FAIL', 'status_msg': '5002'}

def get_predict_data(response, action):
    data_pred = response['data_results']
    if action in ['check_front', 'check_back']:
        data_pred['data_results'] = [{'tag': key, 'text': value} for key, value in data_pred.items() if key not in ['status_code', 'status_msg', 'err_detail']]
    elif action == 'remittance':
        data_pred['data_results'] = [{'tag': key, 'text': value, 'points': remittance_points[key]} for key, value in data_pred.items() if key not in ['status_code', 'status_msg', 'err_detail']]
    return data_pred

@celery.task(ignore_result=False, bind=True, base=PredictTask)
def predict_image(self, image_id, action, input_params):
    # Get the file name from Redis using the image ID as the key
    file_name = celery.backend.get(get_redis_filename(image_id)).decode("utf-8")
    try:
        response = self.predict(image_id, action=action, input_params=input_params)
        data_pred = get_predict_data(response, action)
        return {'status': 'SUCCESS', 'status_msg': '', 'result': data_pred, 'file_name': file_name}
    except MlaasRequestError as e:
        return {'status': 'FAIL', 'status_msg': e.mlaas_code, 'file_name': file_name}
    except Exception as e:
        logger.error({'predict_image': {'error_msg': str(e), 'image_id': image_id, 'action': action}})
        return {'status': 'FAIL', 'status_msg': '5001', 'file_name': file_name}
