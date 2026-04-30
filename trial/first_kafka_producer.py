from confluent_kafka import Producer 


my_producer = Producer({
    'bootstrap.servers': 'localhost:9094'
})

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
        print("all done")

my_producer.produce('test_topic', value='Hello World'.encode('utf-8'), callback=delivery_report)
my_producer.flush()