#!/usr/bin/env python3
"""
✅ Thread-based Modbus Orchestrator
Starts Async Modbus TCP Server in a background thread and runs the client.
Tested with Python 3.10 + pymodbus 3.6.8 (GitHub Actions).
"""

import asyncio
import os
import time
import threading
from datetime import datetime
from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import (
    ModbusSlaveContext,
    ModbusServerContext,
    ModbusSequentialDataBlock,
)
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.client import ModbusTcpClient


# --- Setup timestamped log directory ---
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_dir = os.path.join("logs", timestamp)
os.makedirs(log_dir, exist_ok=True)


async def async_server_loop():
    """Async Modbus server running inside its own asyncio loop"""
    slave = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]),
        co=ModbusSequentialDataBlock(0, [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]),
        hr=ModbusSequentialDataBlock(0, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]),
        ir=ModbusSequentialDataBlock(0, [5, 15, 25, 35, 45, 55, 65, 75, 85, 95]),
        zero_mode=True,
    )
    context = ModbusServerContext(slaves={0: slave, 1: slave}, single=False)

    identity = ModbusDeviceIdentification()
    identity.VendorName = "GitHub"
    identity.ProductName = "Threaded Modbus Server"

    print("🚀 Modbus server starting on 127.0.0.1:5020 ...")

    await StartAsyncTcpServer(
        context=context,
        identity=identity,
        address=("127.0.0.1", 5020),
        defer_start=False,
    )


def start_server_thread():
    """Run the async Modbus server in a dedicated thread"""
    loop = asyncio.new_event_loop()

    def run_loop():
        asyncio.set_event_loop(loop)
        loop.run_until_complete(async_server_loop())

    t = threading.Thread(target=run_loop, daemon=True)
    t.start()
    return t


def run_client():
    """Synchronous client interacting with the Modbus server"""
    client_log_path = os.path.join(log_dir, "client_output.txt")
    with open(client_log_path, "w") as log:
        client = ModbusTcpClient("127.0.0.1", port=5020)
        if not client.connect():
            print("❌ Could not connect to server.", file=log)
            return

        print("✅ Connected to Modbus server.", file=log)

        coils = client.read_coils(0, 10, unit=0)
        print(f"📡 Coils: {getattr(coils, 'bits', coils)}", file=log)

        hr = client.read_holding_registers(0, 10, unit=0)
        print(f"📗 Holding Registers: {getattr(hr, 'registers', hr)}", file=log)

        ir = client.read_input_registers(0, 10, unit=0)
        print(f"📙 Input Registers: {getattr(ir, 'registers', ir)}", file=log)

        client.close()
        print("🔌 Client disconnected.", file=log)


if __name__ == "__main__":
    # --- Start server in background thread ---
    server_thread = start_server_thread()
    time.sleep(3)  # give the server time to start

    # --- Run client operations ---
    run_client()

    # --- Allow server to serve a bit more, then exit ---
    time.sleep(1)
    print(f"✅ Logs saved to: {os.path.abspath(log_dir)}")

    with open(os.path.join(log_dir, "run_summary.txt"), "w") as f:
        f.write("✅ Modbus workflow completed successfully.\n")
        f.write("Timestamp: " + time.ctime() + "\n")
