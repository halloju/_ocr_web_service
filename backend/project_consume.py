import redis
from app.kafka_server.result_consumer import ResultConsumer
import os
import sys


def run_consumer(project_name: str, redis_server, kafka_config):
    if project_name == 'cv_controller':
        kafka_config['group.id'] = "if_gp_ocr_cv_controller_callback_02"

        def msg_func(ocr_results) -> list:
            new_results = []
            for ocr_result in ocr_results:
                x_min, x_max, y_min, y_max = (
                    ocr_result['x_min'], ocr_result['x_max'], ocr_result['y_min'], ocr_result['y_max'])
                new_result = {key: value for key, value in ocr_result.items(
                ) if key not in ['text', 'x_min', 'x_max', 'y_min', 'y_max', 'etl_dt']}
                new_result['text'] = ocr_result['label']
                new_result['points'] = [[x_min, y_min], [
                    x_max, y_min], [x_max, y_max], [x_min, y_max]]  # 順時針
                new_results.append(new_result)
            return new_results
        try:
            consumer = ResultConsumer(
                kafka_config, ['if_gp_ocr.cv_controller_callback'], redis_server, msg_func)
            consumer.dequeue()
        except Exception as e:
            print(f'consumer failed to start, error: {e}')
    elif project_name == 'gp_controller':
        kafka_config['group.id'] = "if_gp_ocr_gp_controller_callback_02"

        def msg_func(ocr_results) -> list:
            """ format is the same """
            return ocr_results
        try:
            consumer = ResultConsumer(
                kafka_config, ['if_gp_ocr.gp_controller_callback'], redis_server, msg_func)
            consumer.dequeue()
        except Exception as e:
            print(f'consumer failed to start, error: {e}')


if __name__ == "__main__":
    from urllib import parse
    project_name = sys.argv[1]
    redis_url = os.environ.get("LOCAL_REDIS_URL", "redis://localhost:6379")
    parse.uses_netloc.append('redis')
    url = parse.urlparse(redis_url)
    redis_server = redis.Redis(
        host=url.hostname, port=url.port, db=0, password=url.password, decode_responses=True)
    kafka_config = {
        'sasl.username': os.environ.get('KAFKA_ID'),
        'sasl.password': os.environ.get('KAFKA_PASSWORD'),
        'bootstrap.servers': os.environ.get('KAFKA_HOST'),
        'auto.offset.reset': 'earliest',
        'max.poll.interval.ms': 3600000,
        # 'security.protocol': 'SASL_PLAINTEXT',
        # 'sasl.mechanism': 'SCRAM-SHA-512'
    }
    run_consumer(project_name, redis_server, kafka_config)
