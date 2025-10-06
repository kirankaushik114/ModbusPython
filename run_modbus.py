#!/usr/bin/env python3
"""
✅ Full Modbus Orchestrator with Async Server + Client + Logging
Works inside GitHub Actions using pymodbus 3.6.8
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
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_dir = os.path.join("logs", timestamp)
os.makedirs(log_dir, exist_ok=True)


async def start_modbus_server():
    """Start async Modbus server"""
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

    print("🚀 Starting Async Modbus TCP Server on 127.0.0.1:5020 ...")

    await StartAsyncTcpServer(
        context=context,
        identity=identity,
        address=("127.0.0.1", 5020),
        defer_start=False,
    )


async def run_modbus_client():
    """Connect to local server, read/write data, and save logs"""
    await asyncio.sleep(2)  # wait for server to start

    client_log_path = os.path.join(log_dir, "client_output.txt")
    with open(client_log_path, "w") as log:
        client = ModbusTcpClient("127.0.0.1", port=5020)
        if client.connect():
            print("✅ Connected to Modbus server.", file=log)

            # --- Read Coils ---
            coils = client.read_coils(0, 10, unit=0)
            if not coils.isError():
                print(f"📡 Coils: {coils.bits[:10]}", file=log)
            else:
                print(f"❌ Coil read failed: {coils}", file=log)

            # --- Write Coils ---
            client.write_coil(0, False, unit=0)
            client.write_coil(1, True, unit=0)

            # --- Read Holding Registers ---
            hr = client.read_holding_registers(0, 10, unit=0)
            if not hr.isError():
                print(f"📗 Holding Registers: {hr.registers[:10]}", file=log)
            else:
                print(f"❌ HR read failed: {hr}", file=log)

            # --- Read Input Registers ---
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
    server_task = asyncio.create_task(start_modbus_server())
    await run_modbus_client()
    server_task.cancel()

    # Write summary log
    summary_path = os.path.join(log_dir, "run_summary.txt")
    with open(summary_path, "w") as f:
        f.write("✅ Modbus workflow completed successfully.\n")
        f.write("Timestamp: " + time.ctime() + "\n")

    print(f"✅ Logs written to: {os.path.abspath(log_dir)}")


if __name__ == "__main__":
    asyncio.run(main())
