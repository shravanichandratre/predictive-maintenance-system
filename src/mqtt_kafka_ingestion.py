import json
import time
import paho.mqtt.client as mqtt
from kafka import KafkaProducer
import random
import threading

# MQTT Configuration
MQTT_BROKER = "mqtt.eclipse.org"
MQTT_PORT = 1883
MQTT_TOPIC = "real-time-data"

# Kafka Configuration
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "real-time-data"

# MQTT Client Setup
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe(MQTT_TOPIC)

mqtt_client.on_connect = on_connect

def publish_mqtt_data():
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()

    while True:
        data = {
            "sensor_id": random.randint(1, 10),
            "value": random.uniform(20.0, 100.0),
            "timestamp": time.time()
        }
        mqtt_client.publish(MQTT_TOPIC, json.dumps(data))
        print(f"Published data: {data}")
        time.sleep(1)

# Kafka Producer Setup
kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def publish_kafka_data():
    while True:
        data = {
            "sensor_id": random.randint(1, 10),
            "value": random.uniform(20.0, 100.0),
            "timestamp": time.time()
        }
        kafka_producer.send(KAFKA_TOPIC, value=data)
        print(f"Published data to Kafka: {data}")
        time.sleep(1)

# Start both MQTT and Kafka producers in parallel
if __name__ == "__main__":
    mqtt_thread = threading.Thread(target=publish_mqtt_data)
    kafka_thread = threading.Thread(target=publish_kafka_data)
    
    mqtt_thread.start()
    kafka_thread.start()

    mqtt_thread.join()
    kafka_thread.join()
