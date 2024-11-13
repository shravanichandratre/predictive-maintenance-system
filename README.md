# MaintenAI

**MaintenAI** is an intelligent predictive maintenance system designed to monitor industrial equipment in real-time. By leveraging advanced machine learning models and IoT-based sensor data, it proactively predicts potential failures, thereby reducing downtime and improving the efficiency of industrial operations. The system uses **Random Forest** and **LSTM** models for anomaly detection and integrates technologies like **MQTT**, **Kafka**, and **InfluxDB** for seamless data flow and storage.

## Key Features

- **Real-Time Monitoring:** Continuously monitors sensor data from industrial equipment in real-time.
- **Predictive Analytics:** Uses machine learning models (Random Forest and LSTM) to predict potential failures before they occur.
- **Anomaly Detection:** Detects anomalies in the equipment's behavior to trigger alerts for maintenance.
- **Scalable Data Storage:** Utilizes **InfluxDB** for storing time-series sensor data, ensuring high scalability and reliability.
- **Stream Processing:** Implements **Kafka** for real-time stream processing and communication between components.
- **IoT Integration:** Uses **MQTT** for seamless data ingestion from IoT devices, ensuring fast and reliable data transmission.

## Technologies Used

- **Machine Learning:** Random Forest, LSTM (Long Short-Term Memory) models for anomaly detection.
- **Database:** InfluxDB for storing and querying time-series data.
- **Streaming:** Kafka for stream processing.
- **Real-Time Data Ingestion:** MQTT for IoT device communication.
- **Programming Languages:** Python
- **Data Processing:** Pandas, NumPy
- **Modeling:** Scikit-learn (Random Forest), TensorFlow/Keras (LSTM)
