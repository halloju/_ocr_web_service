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

    def __init__(self, kafka_configs: dict, topics: list, redis_server, msg_func, result_title, project):
        self.redis_server = redis_server
        self.msg_func = msg_func
        self.result_title = result_title
        self.project = project
        super().__init__(kafka_configs, topics, project)

    def consumer_process(self, msg):
        # check id exist
        if (self.result_title not in msg):
            self.logger_tool.warning(
                {'error_msg': f'{self.result_title} not exist in msg'})
            return False
        try:
            task_id = msg['image_cv_id'].replace('/', '-')
            full_key = get_redis_taskname(task_id)
            start_time = self.redis_server.hget(full_key, 'start_time')

            if (not start_time):
                self.logger_tool.error({'predict_image': {'task_id': task_id, 'process_time': '', 'action': '',
                                       'status': 'FAIL', 'status_msg': '5002', 'error_msg': 'not exist in redis'}})
                return False

            if msg['recognition_status'] == 'FAIL':
                self.redis_server.hset(full_key, 'status', 'FAIL')
            else:
                result_data = {
                    'data_results': self.msg_func(msg[self.result_title]),
                    'image_id': msg['image_cv_id']
                }
                updates = {
                    'result': json.dumps(result_data),
                    'status': 'SUCCESS'
                }
                self.redis_server.hmset(full_key, updates)

                start_time = datetime.strptime(
                    start_time, "%Y-%m-%d %H:%M:%S")
            self.logger_tool.info({
                'request_id': full_key,
                'process_time': (datetime.now() - start_time).microseconds,
                'action': self.project}
            )
            return True
        except Exception as exc:
            self.logger_tool.error(
                {'request_id': full_key, 'error_msg': str(exc)})
