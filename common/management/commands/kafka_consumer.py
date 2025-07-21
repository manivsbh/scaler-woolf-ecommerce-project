
import json
from django.core.management.base import BaseCommand
from kafka import KafkaConsumer
from django.conf import settings

class Command(BaseCommand):
    help = 'Starts a Kafka consumer to listen for messages'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Kafka consumer...'))
        consumer = KafkaConsumer(
            'user_registered', 'cart_item_added', 'order_created', 'payment_processed',
            bootstrap_servers=settings.KAFKA_BROKER_URLS,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        for message in consumer:
            self.stdout.write(self.style.SUCCESS(f"Received message from topic '{message.topic}': {message.value}"))
