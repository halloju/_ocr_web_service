"""
Consumer Class
"""
import json
from mlaas_tools2.config_info import ConfigPass
from mlaas_tools2.kafka_tools import ConsumerTool
from src.logger_tool import Logger
from src.utils import KafkaToolsException

def call_common_consumer(flow_config, consumer_config, **context):
    consumer_instance = CommonConsumer(flow_config, consumer_config, context)
    consumer_instance.run()

class BaseConsumer(object):
    """
    Base Class of Consumer
    """

    def __init__(self):
        self.project = "if_gp_ocr"
        self.topic = "if_gp_ocr.gp_callback"
        self.config = ConfigPass()
        self.dequeue_status = True
        self.kafka_info = self.config.get_conn('if_gp_ocr_kafka')
        self.kafka_config = {
            'sasl.username': self.kafka_info['login'],
            'sasl.password': self.kafka_info['password'],
            'bootstrap.servers': self.kafka_info['host'],
            'group.id': "if_gp_ocr_gp_callback_01",
            'auto.offset.reset': 'earliest',
            'max.poll.interval.ms': 3600000,
        }
        self.consumer = ConsumerTool(self.kafka_config)
        self.consumer.subscribe([self.topic])
        self.logger_tool = Logger()

    def dequeue(self, timeout=1):
        try:
            while self.dequeue_status:
                print(self.dequeue_status)
                msg = self.consumer.poll(timeout=timeout)
                if msg is not None:
                    # if message occured error
                    if msg.error():
                        self.logger_tool.error({
                            'consumer': {
                                'error_code': msg.error().code(),
                                'error_info': str(msg.error().str())
                            }
                        })
                        continue
                    else:
                        msg_decode = json.loads(msg.value().decode("utf-8"))
                        self.logger_tool.info(msg_decode)
                        self.logger_tool.info({"consumer": {
                            "topic": msg.topic(),
                            "partition": msg.partition(),
                            "timestamp": {
                                "type": msg.timestamp()[0],
                                "value": msg.timestamp()[1]
                            }
                        }})

        except Exception as e:
            self.logger_tool.error({"consumer": {"error_info": str(e)}})
            raise KafkaToolsException


if __name__ == "__main__":
    consumer = BaseConsumer()
    consumer.dequeue()
