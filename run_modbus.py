#!/usr/bin/env python3
"""
✅ FINAL WORKING VERSION
Runs Modbus TCP Server and Client (pymodbus 3.x compatible) inside GitHub Actions.
Server runs in background process; client connects and reads data; all logs are saved.
"""

import os
import time
import socket
import multiprocessing
from datetime import datetime
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
from pymodbus.client import ModbusTcpClient


# === Create timestamped log folder ===
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_dir = os.path.join("logs", timestamp)
os.makedirs(log_dir, exist_ok=True)


def run_server():
    """Blocking Modbus server running in its own process."""
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0] * 10),
        co=ModbusSequentialDataBlock(0, [1] * 10),
        hr=ModbusSequentialDataBlock(0, list(range(10, 110, 10))),
        ir=ModbusSequentialDataBlock(0, list(range(5, 105, 10))),
        zero_mode=True,
    )
    context = ModbusServerContext(slaves=store, single=True)
    print("🚀 Starting Modbus TCP server on 127.0.0.1:5020 ...", flush=True)
    StartTcpServer(context, address=("127.0.0.1", 5020))


def wait_for_port(host, port, timeout=10):
    """Wait until a TCP port starts accepting connections."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
    return False


def run_client():
    """Run Modbus client, connect to server, and log results."""
    client_log = os.path.join(log_dir, "client_output.txt")
    with open(client_log, "w") as log:
        client = ModbusTcpClient("127.0.0.1", port=5020)
        if not client.connect():
            print("❌ Could not connect to server.", file=l
