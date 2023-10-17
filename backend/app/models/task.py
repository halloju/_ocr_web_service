from datetime import datetime


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
            'url_result': f'/ocr/result/{self.task_id}'
        }

    def mark_as_processing(self, predict_class, image_cv_id):
        self.predict_class = predict_class
        self.status = 'PROCESSING'
        self.image_cv_id = image_cv_id
        self.task_id = str(self.image_cv_id).replace('/', '-')

    def mark_as_failed(self, predict_class, image_cv_id, err_code, err_msg):
        self.predict_class = predict_class
        self.status = 'FAIL'
        self.image_cv_id = image_cv_id
        self.err_msg = err_msg  # Further refine error handling if needed
        self.err_code = err_code
        self.task_id = str(self.image_cv_id).replace('/', '-')
