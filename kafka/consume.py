from confluent_kafka import Consumer
################
c = Consumer({
    'bootstrap.servers': '127.0.0.1:9092',
    'group.id': 'python-consumer',
    'auto.offset.reset': 'earliest',
    'sasl.username': 'admin',
    'sasl.password': '1313'})
print('Kafka Consumer has been initiated...')


print('Available topics to consume: ', c.list_topics().topics)
c.subscribe(['if_gp_ocr.gp_callback'])

while True:
    msg = c.poll(1.0)  # timeout
    print(msg)
    if msg is None:
        continue
    if msg.error():
        print('Error: {}'.format(msg.error()))
        continue
    data = msg.value().decode('utf-8')
    print(data)
c.close()
