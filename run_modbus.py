#!/usr/bin/env python3
"""
✅ Async orchestrator that runs both Modbus server and client in one event loop.
Compatible with pymodbus 3.6.8 and Python 3.10+
"""

import asyncio
import os
import time
from datetime import datetime
from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import (
    ModbusSlaveContext,
    ModbusServerContext,
    ModbusSequentialDataBlock,
)
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.client import ModbusTcpClient


# === Create timestamped logs folder ===
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
log_dir = os.path.join("logs", timestamp)
os.makedirs(log_dir, exist_ok=True)


async def start_modbus_server():
    """Start async Modbus TCP server in background"""
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
    identity.ProductName = "Async Modbus Server"

    print("🚀 Starting Async Modbus TCP Server on 127.0.0.1:5020 ...")
    await StartAsyncTcpServer(context=context, identity=identity, address=("127.0.0.1", 5020))


async def run_modbus_client():
    """Run Modbus client tasks"""
    await asyncio.sleep(2)  # wait for server startup
    log_path = os.path.join(log_dir, "client_output.txt")

    with open(log_path, "w") as log:
        client = ModbusTcpClient("127.0.0.1", port=5020)
        if client.connect():
            print("✅ Connected to Modbus server.", file=log)
            coils = client.read_coils(0, 10, unit=0)
            print(f"📖 Coils: {coils.bits[:10]}", file=log)
            client.write_coil(0, False, unit=0)
            client.write_coil(1, True, unit=0)
            hr = client.read_holding_registers(0, 10, unit=0)
            print(f"📗 Holding Registers: {hr.registers[:10]}", file=log)
            ir = client.read_input_registers(0, 10, unit=0)
            print(f"📙 Input Registers: {ir.registers[:10]}", file=log)
            client.close()
            print("🔌 Client disconnected.", file=log)
        else:
            print("❌ Could not connect to server.", file=log)

    print("✅ Client run complete.")


async def main():
    server_task = asyncio.create_task(start_modbus_server())
    client_task = asyncio.create_task(run_modbus_client())

    await asyncio.wait([client_task], return_when=asyncio.ALL_COMPLETED)
    print("🧹 Shutting down Modbus server...")
    server_task.cancel()
    with open(os.path.join(log_dir, "run_summary.txt"), "w") as f:
        f.write("✅ Modbus workflow completed successfully.\n")
        f.write("Timestamp: " + time.ctime() + "\n")


if __name__ == "__main__":
    asyncio.run(main())
