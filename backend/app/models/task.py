from datetime import datetime
import uuid
import json
from typing import List, Tuple


class Task:
    def __init__(self, file_name: str, series_num: int, image_cv_id: str, predict_class='', status='INITIAL', err_msg=''):
        self.file_name = file_name
        self.series_num = series_num
        self.image_cv_id = image_cv_id
        self.predict_class = predict_class
        self.status = status
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.err_msg = err_msg
        self.err_code = ''
        # Convert 2022/10/11.../uuid to 2022-10-11...-uuid
        self.task_id = str(self.image_cv_id).replace('/', '-')
        self.ocr_results = {}
        self.image_redis_key = f'{self.task_id}-image'

    def to_dict(self):
        """
        Convert the Task object to a dictionary. Useful for returning as a response or storing in databases.
        """
        return {
            'file_name': self.file_name,
            'series_num': self.series_num,
            'predict_class': self.predict_class,
            'status': self.status,
            'image_cv_id': self.image_cv_id,
            'start_time': self.start_time,
            'status_msg': self.err_msg,
            'task_id': self.task_id,
            'url_result': f'/ocr/result/{self.task_id}',
            'ocr_results': json.dumps(self.ocr_results),
            'image_redis_key': self.image_redis_key
        }
    
    def to_dict_no_dumps(self):
        """
        Convert the Task object to a dictionary. Useful for returning as a response or storing in databases.
        """
        return {
            'file_name': self.file_name,
            'series_num': self.series_num,
            'predict_class': self.predict_class,
            'status': self.status,
            'image_cv_id': self.image_cv_id,
            'start_time': self.start_time,
            'status_msg': self.err_msg,
            'task_id': self.task_id,
            'url_result': f'/ocr/result/{self.task_id}',
            'ocr_results': self.ocr_results,
            'image_redis_key': self.image_redis_key
        }

    def mark_as_processing(self, image_cv_id, predict_class: str = ''):
        self.status = 'PROCESSING'
        self.image_cv_id = image_cv_id
        self.task_id = str(self.image_cv_id).replace('/', '-')
        self.predict_class = predict_class

    def mark_as_failed(self, image_cv_id, err_code, err_msg, predict_class: str = ''):
        self.status = 'FAIL'
        self.image_cv_id = image_cv_id
        self.err_msg = err_msg  # Further refine error handling if needed
        self.err_code = err_code
        self.task_id = str(self.image_cv_id).replace('/', '-')
        self.predict_class = predict_class

    def mark_as_success(self, image_cv_id, result: List):
        self.status = 'SUCCESS'
        self.image_cv_id = image_cv_id
        self.task_id = str(self.image_cv_id).replace('/', '-')
        self.ocr_results['data_results'] = result
