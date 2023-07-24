"""
OCR result Consumer Class
"""
import json
from app.kafka_server.base_consumer import BaseConsumer
from route_utils import get_redis_taskname

from datetime import datetime

class ResultConsumer(BaseConsumer):
    """
    Base Class of Consumer
    """

    def __init__(self, kafka_configs: dict, topics: list, redis_server, msg_func):
        # redis_server = redis.Redis(host="redis", port=6379, decode_responses=True)
        self.redis_server = redis_server
        self.msg_func = msg_func
        super().__init__(kafka_configs, topics, 'cv_consumer')

    def consumer_process(self, msg):
        # check id exist
        if ('ocr_results' not in msg):
            self.logger_tool.warning({'error_msg': 'ocr_results not exist in msg'})
            return False
        try:
            task_id = msg['image_cv_id'].replace('/', '-')
            full_key = get_redis_taskname(task_id)
            old_data = self.redis_server.get(full_key)
            if (not old_data):
                self.logger_tool.error({'predict_image': {'task_id': task_id, 'process_time': '', 'action': '', 'status': 'FAIL', 'status_msg': '5002', 'error_msg': 'not exist in redis'}})
                return False
            if msg['recognition_status'] == 'FAIL':
                old_data['status'] = 'FAIL'
            else:
                old_data = json.loads(old_data)
                old_data['result'] = self.msg_func(msg['ocr_results'])
                old_data['status'] = 'SUCCESS'
                start_time = datetime.strptime(old_data['start_time'], "%Y-%m-%d %H:%M:%S")
            self.redis_server.set(full_key, json.dumps(old_data))  # replace
            # self.logger_tool.info({'request_id': full_key, 'msg': 'upload to redis'})
            self.logger_tool.info({'predict_image': {'task_id': task_id, 'process_time': (datetime.now() - start_time).microseconds, 'action': 'cv-ocr', 'status': 'SUCCESS', 'status_msg': '', 'error_msg': ''}})
            return True
        except Exception as e:
            self.logger_tool.error({'request_id': msg['request_id'], 'error_msg': str(e)})
