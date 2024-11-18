import json
import random
import time
import paho.mqtt.client as mqtt
from kafka import KafkaProducer

# Simulate MQTT
def simulate_mqtt_data():
    mqtt_broker = "mqtt.eclipse.org"
    mqtt_port = 1883
    mqtt_topic = "real-time-data"
    
    client = mqtt.Client()
    client.connect(mqtt_broker, mqtt_port, 60)
    
    while True:
        data = {
            "sensor_id": random.randint(1, 10),
            "value": random.uniform(20.0, 100.0),
            "timestamp": time.time()
        }
        client.publish(mqtt_topic, json.dumps(data))
        print(f"Simulated MQTT data: {data}")
        time.sleep(1)

# Simulate Kafka
def simulate_kafka_data():
    kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    
    while True:
        data = {
            "sensor_id": random.randint(1, 10),
            "value": random.uniform(20.0, 100.0),
            "timestamp": time.time()
        }
        kafka_producer.send("real-time-data", value=data)
        print(f"Simulated Kafka data: {data}")
        time.sleep(1)

if __name__ == "__main__":
    simulate_mqtt_data()
    # Alternatively, use simulate_kafka_data() for Kafka simulation
