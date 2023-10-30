from confluent_kafka import Producer
import json
import time
import logging


def receipt(err, msg):
    if err is not None:
        print('Error: {}'.format(err))
    else:
        message = 'Produced message on topic {} with value of {}\n'.format(
            msg.topic(), msg.value().decode('utf-8'))
        logger.info(message)
        print(message)


logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='producer.log',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# gp
# 

# template
# 
p = Producer({
    'bootstrap.servers': 'localhost:9092',
    'sasl.username': 'admin',
    'sasl.password': '1313'})
print('Kafka Producer has been initiated...')
# gp
data = {'image_cv_id': '2023/10/30/07/56/53/87205f3a-5803-4a88-b808-ba8dcdc5319f', 'ocr_results': [{'points': [[205, 402], [433, 402], [433, 1310], [205, 1310]], 'text': '2023.01.16', 'det_prob': 0.9171, 'rec_prob': 0.457}, {'points': [[261, 548], [429, 548], [429, 1320], [261, 1320]], 'text': 'fake_model_name', 'det_prob': 0.7748, 'rec_prob': 0.2874}, {'points': [[256, 647], [743, 647], [743, 1157], [256, 1157]], 'text': 'medium', 'det_prob': 0.3431, 'rec_prob': 0.2719}], 'status_code': '0000', 'status_msg': 'OK'}
m = json.dumps(data)
p.poll(1)
p.produce('if_gp_ocr.gp_controller_callback',
            m.encode('utf-8'), callback=receipt)
p.flush()
# template
data = {'image_cv_id': '2023/10/30/07/58/927d1f0d-dc31-42c5-b44c-283d18e50271', 'ocr_results': [{'points': [[119, 1926], [139, 1926], [139, 2774], [119, 2774]], 'text': '2023.01.16', 'rec_prob': 0.2345, 'tag': 'example_0'}, {'points': [[46, 158], [126, 158], [126, 2738], [46, 2738]], 'text': 'template_alignment+cht_ppocr_v1', 'rec_prob': 0.6526, 'tag': 'example_1'}, {'points': [[59, 2829], [150, 2829], [150, 2829], [59, 2829]], 'text': '1352020231030155821', 'rec_prob': 0.1168, 'tag': 'example_2'}], 'status_code': '0000', 'status_msg': 'OK'}
m = json.dumps(data)
p.poll(1)
p.produce('if_gp_ocr.gp_controller_callback',
            m.encode('utf-8'), callback=receipt)
p.flush()
