# import numpy as np
# import pandas as pd
# from influxdb_client import InfluxDBClient
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense
# from sklearn.ensemble import IsolationForest

# # Constants
# INFLUXDB_TOKEN = "jOIjovuaOTfd5pRIJXFYdIcWmKH4XscEIm6lzoLdrboXRFwRAbHIGnq8BB9CjKcZU4Mnyy2kg0Dh1urf91ooxA=="
# INFLUXDB_URL = "http://localhost:8086"
# INFLUXDB_ORG = "org1"
# INFLUXDB_BUCKET = "maintenance_data"

# # Initialize InfluxDB client
# client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)

# # Function to load data from InfluxDB with column filtering
# def load_data():
#     query_api = client.query_api()

#     # Define the Flux query to get relevant fields, filtering for only needed columns
#     query = f'''
#     from(bucket: "{INFLUXDB_BUCKET}")
#       |> range(start: -1y)  // Adjust time range if needed
#       |> filter(fn: (r) => r._measurement == "engine_data")
#       |> filter(fn: (r) => r._field =~ /sensor_\\d+|time_in_cycles|unit_number|op_setting_\\d+/)
#       |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
#     '''
    
#     result = query_api.query(query)
#     data = [record.values for table in result for record in table.records]
#     data_df = pd.DataFrame(data)

#     # Ensure necessary columns exist
#     expected_columns = ["unit_number", "time_in_cycles", "op_setting_1", "op_setting_2", "op_setting_3"] + \
#                        [f"sensor_{i}" for i in range(1, 22)]
#     data_df = data_df[expected_columns].dropna()

#     print("Data columns after filtering:", data_df.columns)
#     return data_df

# # Preprocess data for LSTM
# def preprocess_data(df, sequence_length=10):  # Adjust as needed
#     sequences = []
#     for unit in df["unit_number"].unique():
#         unit_data = df[df["unit_number"] == unit].drop("unit_number", axis=1).sort_values(by="time_in_cycles")
        
#         if len(unit_data) < sequence_length:
#             print(f"Skipping unit {unit} due to insufficient data (only {len(unit_data)} rows)")
#             continue
        
#         for i in range(len(unit_data) - sequence_length + 1):
#             sequences.append(unit_data.iloc[i : i + sequence_length].values)
    
#     sequences = np.array(sequences)
#     print(f"Preprocessed data shape: {sequences.shape}")
#     return sequences

# # Define a simple LSTM model
# def build_lstm_model(input_shape):
#     model = Sequential([
#         LSTM(50, input_shape=input_shape, return_sequences=True),
#         LSTM(50),
#         Dense(1)
#     ])
#     model.compile(optimizer="adam", loss="mse")
#     return model

# # Anomaly detection
# def detect_anomalies(data):
#     model = build_lstm_model((data.shape[1], data.shape[2]))
#     model.fit(data, data[:, -1, -1], epochs=5, batch_size=32)
#     predictions = model.predict(data)

#     # Compute residuals (errors between predictions and actual values)
#     residuals = np.abs(predictions.flatten() - data[:, -1, -1])

#     # Use Isolation Forest to detect anomalies in the residuals
#     isolation_forest = IsolationForest(contamination=0.1)
#     anomalies = isolation_forest.fit_predict(residuals.reshape(-1, 1))

#     return anomalies

# # Run anomaly detection
# if __name__ == "__main__":
#     print("Loading data...")
#     data_df = load_data()
    
#     print("Preprocessing data...")
#     data_sequences = preprocess_data(data_df)
#     print("Preprocessed data shape:", data_sequences.shape)  # Debug print

#     if data_sequences.ndim == 3:
#         print("Detecting anomalies...")
#         anomalies = detect_anomalies(data_sequences)
#         anomaly_indices = np.where(anomalies == -1)[0]
#         print(f"Anomaly detection complete. Anomalies detected at indices: {anomaly_indices}")
#     else:
#         print("Error: Preprocessed data does not have the expected 3D shape. Check data format and sequence length.")

# # Close client
# client.close()
