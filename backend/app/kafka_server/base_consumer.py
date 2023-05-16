"""
Consumer Class
"""
import json
from confluent_kafka import Consumer
from logger import Logger

class BaseConsumer(object):
    """
    Base Class of Consumer
    """

    def __init__(self, kafka_configs: dict, topics: list):
        self.dequeue_status = True
        self.logger_tool = Logger(__name__)
        
        self.kafka_config = kafka_configs
        self.logger_tool.info(kafka_configs)
        self.consumer = Consumer(self.kafka_config)
        self.logger_tool.info(self.consumer.list_topics().topics)
        # self.logger_tool.info({'Available topics to consume: ', self.consumer.list_topics().topics})
        self.consumer.subscribe(topics)
        self.logger_tool.info({'msg', 'Kafka Consumer has been initiated...'})

    def consumer_process(self, msg):
        raise NotImplementedError

    def dequeue(self, timeout=1):
        try:
            while self.dequeue_status:
                msg = self.consumer.poll(timeout=timeout)
                if msg is not None:
                    # if message occured error
                    if msg.error():
                        self.logger_tool.error(msg.error().str())
                        self.logger_tool.error({
                            'consumer': {
                                'error_code': msg.error().code(),
                                'error_info': str(msg.error().str())
                            }
                        })
                        continue
                    else:
                        msg_decode = json.loads(msg.value().decode("utf-8"))
                        consume_status = self.consumer_process(msg_decode)
                        self.logger_tool.info(msg_decode)
                        # self.logger_tool.info({"consumer": {
                        #     "topic": msg.topic(),
                        #     "partition": msg.partition(),
                        #     "consume_status": consume_status,
                        #     "timestamp": {
                        #         "type": msg.timestamp()[0],
                        #         "value": msg.timestamp()[1]
                        #     }
                        # }})

        except Exception as e:
            self.logger_tool.error({"consumer": {"error_info": str(e)}})
            # raise KafkaToolsException
        finally:
            self.consumer.close()



if __name__ == "__main__":
    consumer = BaseConsumer()
    consumer.dequeue()
