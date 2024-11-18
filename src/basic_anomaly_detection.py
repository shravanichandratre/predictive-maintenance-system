import pandas as pd
from influxdb_client import InfluxDBClient

# Constants
INFLUXDB_TOKEN = "jOIjovuaOTfd5pRIJXFYdIcWmKH4XscEIm6lzoLdrboXRFwRAbHIGnq8BB9CjKcZU4Mnyy2kg0Dh1urf91ooxA=="
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_ORG = "org1"
INFLUXDB_BUCKET = "maintenance_data"

# Initialize client
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
query_api = client.query_api()

# Query all data
query = f'from(bucket:"{INFLUXDB_BUCKET}") |> range(start: -30d)'
tables = query_api.query(query, org=INFLUXDB_ORG)

# Convert to DataFrame
data_list = []
for table in tables:
    for record in table.records:
        data_list.append(record.values)
df = pd.DataFrame(data_list)

# Close client
client.close()

# Print columns and sample data
print("Columns in DataFrame:", df.columns)
print("Sample data:\n", df.head())

# Check for missing values and descriptive stats
print("Missing values:\n", df.isnull().sum())
print("\nData summary:\n", df.describe())

# Ensure '_field' and '_value' are present in the DataFrame
if '_field' not in df.columns or '_value' not in df.columns:
    print("Error: '_field' or '_value' column not found in data.")
else:
    # Filter the rows where the _field column is 'sensor_9'
    sensor_9_data = df[df['_field'] == 'sensor_9']

    if sensor_9_data.empty:
        print("No data found for sensor_9.")
    else:
        # Calculate the threshold for anomaly detection
        sensor_threshold = sensor_9_data['_value'].mean() + 2 * sensor_9_data['_value'].std()

        # Detect anomalies where _value exceeds the threshold
        anomalies = sensor_9_data[sensor_9_data['_value'] > sensor_threshold]

        # Print threshold and anomalies
        print("Threshold for sensor_9:", sensor_threshold)
        print(f"Anomalies detected for sensor_9: {len(anomalies)}")
        if not anomalies.empty:
            print(anomalies[['result', '_time', '_value']])  # Print specific columns for clarity
        else:
            print("No anomalies detected.")

import matplotlib.pyplot as plt

sensor_9_data['_value'].hist(bins=50)
plt.axvline(x=sensor_threshold, color='r', linestyle='--', label='Threshold')
plt.legend()
plt.show()

