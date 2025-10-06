import subprocess
import time
import signal
import os

print("🚀 Starting Modbus automation workflow")

# Start Modbus server
print("Starting Modbus server...")
server_process = subprocess.Popen(["python", "modbus_server.py"])

# Give server a few seconds to initialize
time.sleep(5)
git add .
# Run Modbus client
print("Running Modbus client...")
subprocess.run(["python", "modbus_client_read_coils.py"])

# Stop the server
print("Stopping Modbus server...")
if server_process.poll() is None:
    server_process.terminate()
    try:
        server_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        print("Server didn’t stop gracefully, killing it...")
        server_process.kill()

print("✅ Modbus cycle completed successfully.")
