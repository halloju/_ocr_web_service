from datetime import datetime
import uuid
import json
from typing import List


class Task:
    def __init__(self, image_id, file_name, predict_class='', status='INITIAL', image_cv_id='', err_msg=''):
        self.image_id = image_id
        self.file_name = file_name
        self.predict_class = predict_class
        self.status = status
        self.image_cv_id = image_cv_id
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.err_msg = err_msg
        self.err_code = ''
        # Convert 2022/10/11.../uuid to 2022-10-11...-uuid
        self.task_id = str(self.image_cv_id).replace('/', '-')
        self.ocr_results = {}

    @staticmethod
    async def create_and_store_image(file, image_storage):
        image_id = str(uuid.uuid4())
        task = Task(image_id=image_id, file_name=file.filename)
        _, encoded_data = await image_storage.store_image_data(file, image_id)
        if encoded_data is None:
            task.mark_as_failed('', '', '5002', 'Image storage failed')
        return task, encoded_data

    def to_dict(self):
        """
        Convert the Task object to a dictionary. Useful for returning as a response or storing in databases.
        """
        return {
            'image_id': self.image_id,
            'file_name': self.file_name,
            'predict_class': self.predict_class,
            'status': self.status,
            'image_cv_id': self.image_cv_id,
            'start_time': self.start_time,
            'err_msg': self.err_msg,
            'task_id': self.task_id,
            'url_result': f'/ocr/result/{self.task_id}',
            'ocr_results': json.dumps(self.ocr_results)
        }
    
    def to_dict_no_dumps(self):
        """
        Convert the Task object to a dictionary. Useful for returning as a response or storing in databases.
        """
        return {
            'image_id': self.image_id,
            'file_name': self.file_name,
            'predict_class': self.predict_class,
            'status': self.status,
            'image_cv_id': self.image_cv_id,
            'start_time': self.start_time,
            'err_msg': self.err_msg,
            'task_id': self.task_id,
            'url_result': f'/ocr/result/{self.task_id}',
            'ocr_results': self.ocr_results
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
