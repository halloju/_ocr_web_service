from confluent_kafka import Consumer
import redis

class ResultConsumer(object):
    def __init__(self) -> None:
        consumer_config = {
            'bootstrap.servers':'localhost:9092',
            'group.id':'python-consumer',
            
        }
        consumer_server = Consumer({,,'auto.offset.reset':'earliest'})
        print('Kafka Consumer has been initiated...')
        redis_server = redis.Redis(host='localhost', port=6379, decode_responses=True)
        # r.set('name', 'runoob')  # 设置 name 对应的值


        print('Available topics to consume: ', consumer_server.list_topics().topics)
        consumer_server.subscribe(['if_gp_ocr.gp_callback'])
    def consume
    while True:
        msg=c.poll(1.0) #timeout
        if msg is None:
            continue
        \
        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue
        data=msg.value().decode('utf-8')
        print(data)
    c.close()