import redis
from app.kafka_server.result_consumer import ResultConsumer
import os
import sys
from urllib import parse
from utils.logger import Logger

logger_tool = Logger('consumer_main')


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
        topics = ['if_gp_ocr.cv_controller_callback']
        key_name = 'ocr_results'
    elif project_name == 'gp_controller':
        kafka_config['group.id'] = "if_gp_ocr_gp_callback_02"

        def msg_func(ocr_results) -> list:
            """ format is the same """
            for ocr_result in ocr_results:
                ocr_result['points'] = ocr_result['points_list']
                del ocr_result['points_list']
            return ocr_results
        topics = ['if_gp_ocr.gp_callback']
        key_name = 'data_results'
    try:
        consumer = ResultConsumer(
            kafka_config,
            topics,
            redis_server,
            msg_func,
            key_name,
            project_name
        )
        consumer.dequeue()
    except Exception as e:
        logger_tool.error(
            {'error_msg': f'consumer failed to start, error: {e}', 'project': project_name})


def validate_redis_url(redis_url):
    parse.uses_netloc.append('redis')
    parsed_url = parse.urlparse(redis_url)
    if parsed_url.scheme != 'redis':
        raise ValueError("Invalid URL scheme for Redis URL")
    if not parsed_url.hostname or not parsed_url.port:
        raise ValueError("Invalid Redis URL")
    return parsed_url


if __name__ == "__main__":
    project_name = sys.argv[1]
    allowed_project_names = ['cv_controller', 'gp_controller']
    if project_name not in allowed_project_names:
        logger_tool.error("Not allowed consumer type")
        exit()
    redis_url = os.environ.get("LOCAL_REDIS_URL", "redis://localhost:6379")
    try:
        validated_url = validate_redis_url(redis_url)
        # Proceed with using validated_url to establish Redis connection
    except ValueError as e:
        # Handle invalid URL appropriately
        logger_tool.error(f"Error: {e}")
        exit()
    redis_server = redis.Redis(
        host=validated_url.hostname, port=validated_url.port, db=0, password=validated_url.password, decode_responses=True)
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
