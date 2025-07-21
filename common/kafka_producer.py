
import json
from kafka import KafkaProducer
from django.conf import settings

def get_kafka_producer():
    return KafkaProducer(bootstrap_servers=settings.KAFKA_BROKER_URLS,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def send_kafka_message(topic, message):
    producer = get_kafka_producer()
    producer.send(topic, message)
    producer.flush()
    print(f"Sent message to topic {topic}: {message}")
