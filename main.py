import threading
import time
from mqtt_kafka_ingestion import publish_mqtt_data, publish_kafka_data
from kafka_consumer import consume_kafka_data

def start_data_ingestion():
    mqtt_thread = threading.Thread(target=publish_mqtt_data)
    kafka_thread = threading.Thread(target=publish_kafka_data)
    mqtt_thread.start()
    kafka_thread.start()
    return mqtt_thread, kafka_thread

def start_consumer():
    consumer_thread = threading.Thread(target=consume_kafka_data)
    consumer_thread.start()
    return consumer_thread

if __name__ == "__main__":
    print("Starting data ingestion and Kafka consumer...")
    ingestion_threads = start_data_ingestion()
    consumer_thread = start_consumer()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping application...")
        for thread in ingestion_threads:
            thread.join()
        consumer_thread.join()
