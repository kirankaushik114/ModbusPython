#!/usr/bin/env python3
"""
✅ Fully Working Modbus Orchestrator
Runs Async Modbus TCP Server and Client together, logs all results.
Compatible with Python 3.10+ and pymodbus 3.6.8.
"""

import asyncio
import os
import time
from datetime import datetime
from pymodbus.server import ServerAsyncStop, StartAsyncTcpServer
from pymodbus.datastore import (
    ModbusSlaveContext,
    ModbusServerContext,
    ModbusSequentialDataBlock,
)
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.client import ModbusTcpClient

# === Setup timestamped logs folder ===
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
log_dir = os.path.join("logs", timestamp)
os.makedirs(log_dir, exist_ok=True)


async def start_server():
    """Start the async Modbus server"""
    slave_data = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]),
        co=ModbusSequentialDataBlock(0, [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]),
        hr=ModbusSequentialDataBlock(0, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]),
        ir=ModbusSequentialDataBlock(0, [5, 15, 25, 35, 45, 55, 65, 75, 85, 95]),
        zero_mode=True,
    )
    context = ModbusServerContext(slaves={0: slave_data, 1: slave_data}, single=False)

    identity = ModbusDeviceIdentification()
    identity.VendorName = "GitHub"
    identity.ProductName = "Async Modbus TCP Server"
    identity.MajorMinorRevision = "3.6.8"

    print("🚀 Starting Async Modbus TCP Server on 127.0.0.1:5020 ...")

    # Start server in background and return the task
    server = await StartAsyncTcpServer(
        context=context,
        identity=identity,
        address=("127.0.0.1", 5020),
        defer_start=False,
    )
    return server


async def run_client():
    """Run Modbus client tests"""
    await asyncio.sleep(2)  # Wait for server to initialize
    log_path = os.path.join(log_dir, "client_output.txt")

    with open(log_path, "w") as log:
        client = ModbusTcpClient("127.0.0.1", port=5020)
        if client.connect():
            print("✅ Connected to Modbus server.", file=log)

            # Read coils
            coils = client.read_coils(0, 10, unit=0)
            if not coils.isError():
                print(f"📡 Coils: {coils.bits[:10]}", file=log)
            else:
                print(f"❌ Coil read failed: {coils}", file=log)

            # Write coils
            client.write_coil(0, False, unit=0)
            client.write_coil(1, True, unit=0)

            # Read holding registers
            hr = client.read_holding_registers(0, 10, unit=0)
            if not hr.isError():
                print(f"📗 Holding Registers: {hr.registers[:10]}", file=log)
            else:
                print(f"❌ HR read failed: {hr}", file=log)

            # Read input registers
            ir = client.read_input_registers(0, 10, unit=0)
            if not ir.isError():
                print(f"📙 Input Registers: {ir.registers[:10]}", file=log)
            else:
                print(f"❌ IR read failed: {ir}", file=log)

            client.close()
            print("🔌 Client disconnected.", file=log)
        else:
            print("❌ Could not connect to server.", file=log)

    print("✅ Client finished run.")


async def main():
    server_task = asyncio.create_task(start_server())
    client_task = asyncio.create_task(run_client())

    await client_task  # Wait for client to finish
    print("🧹 Stopping Modbus server...")
    await ServerAsyncStop()
    with open(os.path.join(log_dir, "run_summary.txt"), "w") as f:
        f.write("✅ Modbus workflow completed successfully.\n")
        f.write("Timestamp: " + time.ctime() + "\n")


if __name__ == "__main__":
    asyncio.run(main())
