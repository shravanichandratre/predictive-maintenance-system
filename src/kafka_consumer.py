import json
from kafka import KafkaConsumer
from model_processing import detect_anomalies

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "real-time-data"

# Kafka Consumer Setup
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

def consume_kafka_data():
    print("Consuming data from Kafka...")
    for message in consumer:
        data = message.value
        print(f"Consumed data: {data}")
        detect_anomalies(data)

if __name__ == "__main__":
    consume_kafka_data()
