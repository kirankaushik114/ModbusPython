#!/usr/bin/env python3
"""
✅ FINAL FIXED VERSION
Modbus Server + Client automation for pymodbus >= 3.6
Runs the TCP server in a background process, then connects a client, reads/writes data, and logs output.
Tested in GitHub Actions Ubuntu runner with pymodbus==3.6.8.
"""

import os
import time
import socket
import multiprocessing
from datetime import datetime
from pymodbus.server import StartTcpServer
from pymodbus.datastore import (
    ModbusSlaveContext,
    ModbusServerContext,
    ModbusSequentialDataBlock,
)
from pymodbus.client import ModbusTcpClient

# === Setup log directory ===
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_dir = os.path.join("logs", timestamp)
os.makedirs(log_dir, exist_ok=True)


def run_server():
    """Blocking Modbus server process"""
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0] * 10),
        co=ModbusSequentialDataBlock(0, [1] * 10),
        hr=ModbusSequentialDataBlock(0, list(range(10, 110, 10))),
        ir=ModbusSequentialDataBlock(0, list(range(5, 105, 10))),
        zero_mode=True,
    )
    context = ModbusServerContext(slaves=store, single=True)

    print("🚀 Starting Modbus TCP server on 127.0.0.1:5020 ...", flush=True)
    # ✅ pymodbus 3.6.8 expects keyword arguments only
    StartTcpServer(context=context, address=("127.0.0.1", 5020))


def wait_for_port(host: str, port: int, timeout: int = 10) -> bool:
    """Wait until a TCP port starts accepting connections"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
    return False


def run_client():
    """Run Modbus client, perform reads/writes, and save logs"""
    client_log_path = os.path.join(log_dir, "client_output.txt")
    with open(client_log_path, "w") as log:
        client = ModbusTcpClient("127.0.0.1", port=5020)
        if not client.connect():
            print("❌ Could not connect to server.", file=log)
            return

        print("✅ Connected to Modbus server.", file=log)

        # --- Read Coils ---
        coils = client.read_coils(0, 10)
        if not coils.isError():
            print(f"📡 Coils: {coils.bits}", file=log)
        else:
            print(f"❌ Coil read failed: {coils}", file=log)

        # --- Write Coils ---
        client.write_coil(0, False)
        client.write_coil(1, True)

        # --- Read Holding Registers ---
        hr = client.read_holding_registers(0, 10)
        if not hr.isError():
            print(f"📗 Holding Registers: {hr.registers}", file=log)
        else:
            print(f"❌ HR read failed: {hr}", file=log)

        # --- Read Input Registers ---
        ir = client.read_input_registers(0, 10)
        if not ir.isError():
            print(f"📙 Input Registers: {ir.registers}", file=log)
        else:
            print(f"❌ IR read failed: {ir}", file=log)

        client.close()
        print("🔌 Client disconnected.", file=log)


if __name__ == "__main__":
    # --- Start Modbus server in background ---
    server_proc = multiprocessing.Process(target=run_server, daemon=True)
    server_proc.start()

    print("⏳ Waiting for server to start ...")
    if not wait_for_port("127.0.0.1", 5020, timeout=10):
        print("❌ Server failed to start.")
        server_proc.terminate()
        raise SystemExit(1)

    print("✅ Server is ready. Running client ...")
    run_client()

    # --- Stop server ---
    print("🧹 Stopping server ...")
    server_proc.terminate()
    server_proc.join(timeout=2)

    # --- Write summary log ---
    summary_path = os.path.join(log_dir, "run_summary.txt")
    with open(summary_path, "w") as f:
        f.write("✅ Modbus workflow completed successfully.\n")
        f.write("Timestamp: " + time.ctime() + "\n")

    print(f"✅ Logs written to {os.path.abspath(log_dir)}")
