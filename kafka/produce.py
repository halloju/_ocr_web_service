from confluent_kafka import Producer
import json
import time
import logging

def receipt(err, msg):
    if err is not None:
        print('Error: {}'.format(err))
    else:
        message = 'Produced message on topic {} with value of {}\n'.format(msg.topic(), msg.value().decode('utf-8'))
        logger.info(message)
        print(message)

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='producer.log',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


p = Producer({
    'bootstrap.servers': 'localhost:9092',
    'sasl.username': 'admin',
    'sasl.password': '1313'})
print('Kafka Producer has been initiated...')

for i in range(10):
    data = {
        'request_id': 'c703d6e3-4e9a-4657-9cd4-640990c95d5b',
        "ocr_results": [
        {
            "image_cv_id": "test_ws_encrypt",
            "ocr_type": "WITHHOLDING_STATEMENT",
            "tag": "id",
            "model": "attention",
            "label": "F1234567",
            "prob": [
            0.9586760401725769,
            0.9515883326530457,
            0.9507707953453064,
            0.9577591419219971,
            0.952286422252655,
            0.9467113018035889,
            0.9480671286582947
            ],
            "x_min": 89,
            "y_min": 226,
            "x_max": 213,
            "y_max": 253,
            "etl_dt": "2022-04-06 18:11:52"
        }
        ]
    }
    m = json.dumps(data)
    p.poll(1)
    p.produce('if_gp_ocr.gp_callback', m.encode('utf-8'),callback=receipt)
    p.flush()
    time.sleep(2)
