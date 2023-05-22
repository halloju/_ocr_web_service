"""
OCR result Consumer Class
"""
import json
from app.kafka_server.base_consumer import BaseConsumer
from route_utils import get_redis_filename, get_redis_taskname

class ResultConsumer(BaseConsumer):
    """
    Base Class of Consumer
    """

    def __init__(self, kafka_configs: dict, topics: list, redis_server, msg_func):
        # redis_server = redis.Redis(host="redis", port=6379, decode_responses=True)
        self.redis_server = redis_server
        self.msg_func = msg_func
        super().__init__(kafka_configs, topics)

    def consumer_process(self, msg):
        # check id exist
        if ('ocr_results' not in msg):
            self.logger_tool.warning({'error_msg': 'ocr_results not exist in msg'})
            return False
        try:
            full_key = msg['ocr_results'][0]['image_cv_id']
            old_data = self.redis_server.get(full_key)
            if (not old_data):
                self.logger_tool.warning({'request_id': full_key, 'error_msg': 'not exist in redis'})
                return False
            else:
                old_data = json.loads(old_data)
                self.logger_tool.info(msg['ocr_results'])
                self.logger_tool.info(old_data)
                old_data['result'] = self.msg_func(msg['ocr_results'])
                old_data['status'] = 'SUCCESS'
                self.logger_tool.info({'request_id': full_key, 'msg': 'msg_func'})
                self.redis_server.set(full_key, json.dumps(old_data))  # replace
                self.logger_tool.info({'request_id': full_key, 'msg': 'upload to redis'})
            return True
        except Exception as e:
            self.logger_tool.error({'request_id': msg['request_id'], 'error_msg': str(e)})


if __name__ == "__main__":
    consumer = BaseConsumer()
    consumer.dequeue()
