import subprocess
import time
import os

# Optional: create a logs directory
os.makedirs("logs", exist_ok=True)

print("🚀 Starting Modbus automation workflow")

# Step 1: Start Modbus server
print("Starting Modbus server...")
server_process = subprocess.Popen(["python", "modbus_server.py"])

# Step 2: Give the server a few seconds to start
time.sleep(5)

# Step 3: Run Modbus client
print("Running Modbus client...")
client_result = subprocess.run(["python", "modbus_client_read_coils.py"], capture_output=True, text=True)

# Save client output to a log file
with open("logs/client_output.txt", "w") as f:
    f.write(client_result.stdout)
    f.write(client_result.stderr)

# Step 4: Stop the server
print("Stopping Modbus server...")
if server_process.poll() is None:
    server_process.terminate()
    try:
        server_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        print("Server did not stop gracefully — killing it...")
        server_process.kill()

# Step 5: Write summary log
with open("logs/run_summary.txt", "w") as f:
    f.write("✅ Modbus workflow completed at: " + time.ctime() + "\n")

print("✅ Modbus operation completed successfully.")
