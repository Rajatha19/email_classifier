"""Module 10: optional Kafka consumer forwarding CEAS-like email events to the API."""
import json
import os
from kafka import KafkaConsumer
import requests


def main() -> None:
    brokers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    topic = os.getenv("KAFKA_INPUT_TOPIC", "incoming-emails")
    api_url = os.getenv("INFERENCE_API_URL", "http://localhost:8044/mlops/stream/classify")
    consumer = KafkaConsumer(topic, bootstrap_servers=brokers, value_deserializer=lambda value: json.loads(value.decode("utf-8")), group_id="phishing-inference")
    for message in consumer:
        response = requests.post(api_url, json=message.value, timeout=15)
        response.raise_for_status()
        print(json.dumps(response.json()))


if __name__ == "__main__":
    main()
