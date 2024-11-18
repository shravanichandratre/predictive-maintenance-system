from influxdb_client import InfluxDBClient
from datetime import datetime

# Constants
INFLUXDB_TOKEN = "jOIjovuaOTfd5pRIJXFYdIcWmKH4XscEIm6lzoLdrboXRFwRAbHIGnq8BB9CjKcZU4Mnyy2kg0Dh1urf91ooxA=="
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_ORG = "org1"
INFLUXDB_BUCKET = "maintenance_data"

# Initialize client
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)

# Define start and stop time to delete all data
start_time = "1970-01-01T00:00:00Z"  # UNIX epoch start time
stop_time = datetime.utcnow().isoformat() + "Z"  # Current time

# Delete data
delete_api = client.delete_api()
delete_api.delete(start_time, stop_time, '_measurement="engine_data"', bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG)

# Close client
client.close()
print("Previous data deleted successfully.")
