import json
from model_processing import detect_anomalies

# Sample test data for anomaly detection
test_data = [
    {"sensor_id": 1, "value": 90.0, "timestamp": 1632979200.0},  # Potential anomaly
    {"sensor_id": 2, "value": 45.0, "timestamp": 1632979260.0},  # Normal data
    {"sensor_id": 3, "value": 100.5, "timestamp": 1632979320.0}, # Potential anomaly
]

def test_anomalies():
    print("Testing anomaly detection with sample data...")
    for data in test_data:
        print(f"Testing data: {json.dumps(data)}")
        detect_anomalies(data)

if __name__ == "__main__":
    test_anomalies()
