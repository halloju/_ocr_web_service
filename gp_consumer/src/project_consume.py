import os
from urllib import parse

from app.kafka_server.result_consumer import ResultConsumer
from utils.logger import Logger

import redis

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
            {"consumer":
                {'error_msg': f'consumer failed to start, error: {e}',
                    'project': project_name}
             }
        )


def validate_redis_url(redis_url):
    parse.uses_netloc.append('redis')
    parsed_url = parse.urlparse(redis_url)
    if parsed_url.scheme != 'redis':
        raise ValueError("Invalid URL scheme for Redis URL")
    if not parsed_url.hostname or not parsed_url.port:
        raise ValueError("Invalid Redis URL")
    return parsed_url


def main_consumer(project_name):
    from urllib import parse
    if not project_name:
        logger_tool.error({"consumer": {"error_msg": "專案項目不可為空"}})
    if project_name not in ['cv_controller', 'gp_controller']:
        logger_tool.error(
            {"consumer": {"error_msg": f"專案項目錯誤: {project_name}"}})
        
    redis_server = None
    try:
        redis_url = os.getenv("LOCAL_REDIS_URL", "redis://localhost:6379")
        location = parse.urlparse(redis_url)
        parse.uses_netloc.append('redis')
        query = location.query
        if ('url' not in parse.parse_qs(query)):
            redis_server = redis.Redis(
                host=location.hostname, port=location.port, db=0, password=location.password, decode_responses=True)
    except Exception as e:
        logger_tool.error({"consumer": {"error_msg": f"redis error: {str(e)}"}})

    if redis_url:
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

