import pickle
import tensorflow as tf
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Load Random Forest Model
def load_random_forest_model():
    with open("models/random_forest_model.pkl", "rb") as file:
        rf_model = pickle.load(file)
    return rf_model

# Load LSTM Model
def load_lstm_model():
    return tf.keras.models.load_model("models/lstm_model.h5")

# Function to detect anomalies
def detect_anomalies(data):
    rf_model = load_random_forest_model()
    lstm_model = load_lstm_model()

    # Random Forest Anomaly Detection
    rf_prediction = rf_model.predict([[data['sensor_id'], data['value']]])
    print(f"Random Forest prediction: {rf_prediction}")

    # LSTM Anomaly Detection (mocked as we assume sequential data)
    # Note: In a real implementation, you should provide a sequence of data to the LSTM model
    lstm_input = np.array([data['value']]).reshape((1, 1, 1))  # LSTM expects 3D input
    lstm_prediction = lstm_model.predict(lstm_input)
    print(f"LSTM prediction: {lstm_prediction}")

    if rf_prediction == 1 or lstm_prediction > 0.5:
        print("Anomaly detected!")
    else:
        print("Data is normal.")
