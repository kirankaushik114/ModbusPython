#!/usr/bin/env python3
"""
🧪 Baseline test: create a log file so GitHub Actions uploads it as an artifact.
Once this works, we'll re-enable Modbus logic.
"""

import os
import time
from datetime import datetime

# --- Make sure a logs directory exists ---
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_dir = os.path.join("logs", timestamp)
os.makedirs(log_dir, exist_ok=True)

# --- Create a simple test file ---
file_path = os.path.join(log_dir, "test_log.txt")

with open(file_path, "w") as f:
    f.write("✅ Hello from GitHub Actions!\n")
    f.write("Timestamp: " + time.ctime() + "\n")
    f.write("Working directory: " + os.getcwd() + "\n")

print(f"✅ Created {file_path}")
print("✅ Listing directory contents:\n")
for root, dirs, files in os.walk(".", topdown=True):
    for name in files:
        print(os.path.join(root, name))

print("✅ Script completed successfully.")
