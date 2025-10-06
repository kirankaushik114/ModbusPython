import subprocess
import time
import os

# Create logs directory
os.makedirs("logs", exist_ok=True)

print("🚀 Starting Modbus automation workflow")

# --- 1️⃣ Start Modbus server and log output ---
print("Starting Modbus server...")
server_log = open("logs/server_output.txt", "w")
server_process = subprocess.Popen(
    ["python", "modbus_server.py"],
    stdout=server_log,
    stderr=subprocess.STDOUT
)

# Give the server a few seconds to start
time.sleep(5)

# --- 2️⃣ Run Modbus client and capture logs ---
print("Running Modbus client...")
client_log = open("logs/client_output.txt", "w")
client_result = subprocess.run(
    ["python", "modbus_client_read_coils.py"],
    stdout=client_log,
    stderr=subprocess.STDOUT
)
client_log.close()

# --- 3️⃣ Stop Modbus server ---
print("Stopping Modbus server...")
if server_process.poll() is None:
    server_process.terminate()
    try:
        server_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        print("Server did not stop gracefully, killing it...")
        server_process.kill()
server_log.close()

# --- 4️⃣ Write a summary log ---
with open("logs/run_summary.txt", "w") as f:
    f.write("✅ Modbus workflow completed successfully.\n")
    f.write("Timestamp: " + time.ctime() + "\n")

print("✅ Logs saved to ./logs/")
