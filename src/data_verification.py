import random
from influxdb_client import InfluxDBClient

# Constants
INFLUXDB_TOKEN = "jOIjovuaOTfd5pRIJXFYdIcWmKH4XscEIm6lzoLdrboXRFwRAbHIGnq8BB9CjKcZU4Mnyy2kg0Dh1urf91ooxA=="
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_ORG = "org1"
INFLUXDB_BUCKET = "maintenance_data"

# Initialize client
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
query_api = client.query_api()

# Query to fetch a broader dataset to ensure randomness
query = f'from(bucket:"{INFLUXDB_BUCKET}") |> range(start: -30d) |> limit(n: 1000)'
tables = query_api.query(query, org=INFLUXDB_ORG)

# Collect all records in a list
all_records = []
for table in tables:
    for record in table.records:
        all_records.append(record.values)

# Convert the list of records into a DataFrame-like structure for easier inspection
import pandas as pd

# Convert records to DataFrame
df = pd.DataFrame(all_records)

# Check the DataFrame structure
print("\nData Structure:")
print("Shape of DataFrame:", df.shape)
print("Columns:", df.columns.tolist())
print("Data types of columns:\n", df.dtypes)

# Print a sample of the first few rows to verify the data
print("\nSample of the first few records:")
print(df.head())

# Select 10 random records from the fetched data
sample_records = random.sample(all_records, 10)

# Print 10 randomly selected records
print("\nRandomly selected records:")
for record in sample_records:
    print(record)

# Close client
client.close()
