import pandas as pd
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Constants
INFLUXDB_TOKEN = "jOIjovuaOTfd5pRIJXFYdIcWmKH4XscEIm6lzoLdrboXRFwRAbHIGnq8BB9CjKcZU4Mnyy2kg0Dh1urf91ooxA=="
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_ORG = "org1"
INFLUXDB_BUCKET = "maintenance_data"
FILE_PATH = "data/train_FD001.txt"  # Change file path to train_FD001.txt
MIN_CYCLES = 5  # Minimum number of cycles required for each unit

# Load and preprocess dataset
def load_and_filter_data(file_path, min_cycles=MIN_CYCLES):
    print(f"Loading data from {file_path}...")
    column_names = ["unit_number", "time_in_cycles", "op_setting_1", "op_setting_2", "op_setting_3"] + \
                   [f"sensor_{i}" for i in range(1, 22)]
    data = pd.read_csv(file_path, sep=" ", header=None, names=column_names, index_col=False)
    
    # Drop any extra columns created due to spacing in the file
    data = data.loc[:, ~data.columns.duplicated()]
    print(f"Data loaded with {data.shape[0]} records and {data.shape[1]} columns.")
    
    # Filter units with fewer than `min_cycles` cycles
    unit_counts = data['unit_number'].value_counts()
    valid_units = unit_counts[unit_counts >= min_cycles].index
    data = data[data['unit_number'].isin(valid_units)]
    
    # Log dropped units for debugging
    dropped_units = unit_counts[unit_counts < min_cycles]
    if not dropped_units.empty:
        print(f"Dropping units with insufficient data:\n{dropped_units}")
    
    print(f"Data after filtering has {data.shape[0]} records.")
    return data

# Initialize InfluxDB client
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Function to write data to InfluxDB
def ingest_data(data):
    points = []
    print("Beginning data ingestion...")
    for _, row in data.iterrows():
        point = (
            Point("engine_data")
            .tag("unit_number", int(row["unit_number"]))
            .field("time_in_cycles", row["time_in_cycles"])
            .field("op_setting_1", row["op_setting_1"])
            .field("op_setting_2", row["op_setting_2"])
            .field("op_setting_3", row["op_setting_3"])
        )
        
        # Add sensor readings as fields
        for sensor in range(1, 22):
            point = point.field(f"sensor_{sensor}", row[f"sensor_{sensor}"])
        
        points.append(point)
        
        # Log the ingestion of the point
        print(f"Ingesting point: unit_number={row['unit_number']}, time_in_cycles={row['time_in_cycles']}")
        
        # Write in batches to InfluxDB for efficiency
        if len(points) == 1000:
            print(f"Writing batch of {len(points)} points to InfluxDB...")
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=points)
            points = []  # Reset points after batch write

    # Write any remaining points
    if points:
        print(f"Writing final batch of {len(points)} points to InfluxDB...")
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=points)

# Run ingestion
if __name__ == "__main__":
    print("Loading and filtering data...")
    data = load_and_filter_data(FILE_PATH)
    print(f"Data loaded with {data.shape[0]} records after filtering.")
    
    print("Starting data ingestion...")
    ingest_data(data)
    print("Data ingestion complete.")
    
    # Close client after ingestion
    client.close()
    print("InfluxDB client connection closed.")
