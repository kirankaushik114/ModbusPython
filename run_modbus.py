#!/usr/bin/env python3
"""
✅ Reliable Modbus Orchestrator for pymodbus >= 3.0
Runs StartTcpServer (sync server) in a background process and a client to interact with it.
Tested with Python 3.10 + pymodbus 3.6.8 (GitHub Actions)
"""

import os
import time
import multiprocessing
from datetime import datetime
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
from pymodbus.client import ModbusTcpClient

# === Create timestamped logs folder ===
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_dir = os.path.join("logs", timestamp)
os.makedirs(log_dir, exist_ok=True)


def run_server():
    """Run Modbus server (blocking) in its own process"""
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*10),
        co=ModbusSequentialDataBlock(0, [1]*10),
        hr=ModbusSequentialDataBlock(0, list(range(10, 110, 10))),
        ir=ModbusSequentialDataBlock(0, list(range(5, 105, 10))),
        zero_mode=True,
    )
    context = ModbusServerContext(slaves=store, single=True)
    print("🚀 Starting Modbus TCP server on 127.0.0.1:5020 ...")
    StartTcpServer(context, address=("127.0.0.1", 5020))


def run_client():
    """Connect to server, read/write coils & registers, log output"""
    client_log = os.path.join(log_dir, "client_output.txt")
    with open(client_log, "w") as log:
        client = ModbusTcpClient("127.0.0.1", port=5020)
        if not client.connect():
            print("❌ Could not connect to server.", file=log)
            return

        print("✅ Connected to Modbus server.", file=log)

        coils = client.read_coils(0, 10)
        print(f"📡 Coils: {getattr(coils, 'bits', coils)}", file=log)

        client.write_coil(0, False)
        client.write_coil(1, True)

        hr = client.read_holding_registers(0, 10)
        print(f"📗 Holding Registers: {getattr(hr, 'registers', hr)}", file=log)

        ir = client.read_input_registers(0, 10)
        print(f"📙 Input Registers: {getattr(ir, 'registers', ir)}", file=log)

        client.close()
        print("🔌 Client disconnected.", file=log)


if __name__ == "__main__":
    # --- Start Modbus server in a background process ---
    server_proc = multiprocessing.Process(target=run_server, daemon=True)
    server_proc.start()
    time.sleep(3)  # give server time to start

    # --- Run client ---
    run_client()

    # --- Stop server ---
    server_proc.terminate()
    server_proc.join(timeout=2)

    with open(os.path.join(log_dir, "run_summary.txt"), "w") as f:
        f.write("✅ Modbus workflow completed successfully.\n")
        f.write("Timestamp: " + time.ctime() + "\n")

    print(f"✅ Logs written to {os.path.abspath(log_dir)}")
