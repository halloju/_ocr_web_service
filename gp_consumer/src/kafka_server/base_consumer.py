"""
Consumer Class
"""
import json

from confluent_kafka import Consumer
from utils.logger import Logger


class BaseConsumer(object):
    """
    Base Class of Consumer
    """

    def __init__(self, kafka_configs: dict, topics: list, kafka_name: str = 'consumer'):
        self.dequeue_status = True
        self.logger_tool = Logger(kafka_name)

        self.kafka_config = kafka_configs
        self.consumer = Consumer(self.kafka_config)
        self.consumer.subscribe(topics)
        self.logger_tool.info({'msg': 'Kafka Consumer has been initiated...'})

    def consumer_process(self, msg):
        raise NotImplementedError

    def dequeue(self, timeout=1):
        try:
            while self.dequeue_status:
                msg = self.consumer.poll(timeout=timeout)
                if not msg:
                    continue
                if msg.error():
                    self.logger_tool.error({
                        'dequeue': {
                            'error_code': msg.error().code(),
                            'error_msg': str(msg.error().str())
                        }
                    })
                    continue
                else:
                    msg_decode = json.loads(msg.value().decode("utf-8"))
                    consume_status = self.consumer_process(msg_decode)
                    self.logger_tool.info({
                        'dequeue': {
                            'consume_status': consume_status
                        }
                    })
        except Exception as exc:
            self.logger_tool.error({"dequeue": {"error_msg": str(exc)}})
        finally:
            self.consumer.close()
