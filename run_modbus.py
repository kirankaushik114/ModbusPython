import subprocess
import time
import os

# === Ensure logs folder exists ===
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

print("🚀 Starting Modbus automation workflow")

# --- 1️⃣ Start Modbus server and log output ---
print("Starting Modbus server...")
server_log_path = os.path.join(log_dir, "server_output.txt")
server_log = open(server_log_path, "w")

server_process = subprocess.Popen(
    ["python", "modbus_server.py"],
    stdout=server_log,
    stderr=subprocess.STDOUT
)

# Wait for server to start
time.sleep(5)

# --- 2️⃣ Run Modbus client and capture output ---
print("Running Modbus client...")
client_log_path = os.path.join(log_dir, "client_output.txt")
with open(client_log_path, "w") as client_log:
    subprocess.run(["python", "modbus_client_read_coils.py"],
                   stdout=client_log,
                   stderr=subprocess.STDOUT)

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

# --- 4️⃣ Write summary log ---
summary_log_path = os.path.join(log_dir, "run_summary.txt")
with open(summary_log_path, "w") as f:
    f.write("✅ Modbus workflow completed successfully.\n")
    f.write("Timestamp: " + time.ctime() + "\n")

print(f"✅ Logs created at: {os.path.abspath(log_dir)}")
