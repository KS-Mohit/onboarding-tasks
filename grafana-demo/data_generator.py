import influxdb_client
import psutil
import time
import os
from influxdb_client.client.write_api import SYNCHRONOUS

# --- InfluxDB Connection Details ---
# IMPORTANT: PASTE THE API TOKEN YOU SAVED IN THIS VARIABLE
token = "2-lyXa4NoBgkL-pPm8liR-esOQPI70TVQrXtC3q5C8rn7PqhSJy7v600T4Hcd6gO8Swhq8upBmlGBY2MpkJn-g=="
org = "my-org"
bucket = "metrics"
url = "http://localhost:8086"

# --- Script Starts Here ---
print("Connecting to InfluxDB...")
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)
print("Connection successful. Starting data generation...")
print("Press Ctrl+C to stop the script.")

try:
    while True:
        # --- Get System Metrics ---
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        
        # Get disk usage for the root directory ('/')
        # On Windows you might need to change this to 'C:\\'
        disk_path = '/' if os.name != 'nt' else 'C:\\'
        disk_percent = psutil.disk_usage(disk_path).percent
        
        # Get network I/O counters
        net_io = psutil.net_io_counters()
        network_bytes_sent = net_io.bytes_sent
        network_bytes_recv = net_io.bytes_recv

        # Create the data point in the format InfluxDB understands
        point = (
            influxdb_client.Point("system_metrics")
            .tag("host", "local_machine")
            .field("cpu_load_percent", cpu_percent)
            .field("memory_percent", memory_percent)
            .field("disk_percent", disk_percent)
            .field("network_bytes_sent", network_bytes_sent)
            .field("network_bytes_recv", network_bytes_recv)
        )
        
        # Write the data point to the InfluxDB bucket
        write_api.write(bucket=bucket, org=org, record=point)
        
        print(f"Data written: CPU {cpu_percent}%, Memory {memory_percent}%, Disk {disk_percent}%")
        
        # Wait for 5 seconds before sending the next data point
        time.sleep(5)

except KeyboardInterrupt:
    print("\nScript stopped by user.")
finally:
    print("Closing InfluxDB client.")
    client.close()