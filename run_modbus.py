#!/usr/bin/env python3
"""
✅ Reliable Modbus Orchestrator
Starts an async Modbus TCP server and runs a synchronous client against it.
Tested with Python 3.10 + pymodbus 3.6.8 in GitHub Actions.
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


# --- Create timestamped log folder ---
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_dir = os.path.join("logs", timestamp)
os.makedirs(log_dir, exist_ok=True)


async def run_server(stop_event: asyncio.Event):
    """Run Modbus server until stop_event is set."""
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
    identity.ProductName = "Async Modbus TCP Server"

    print("🚀 Starting Async Modbus TCP Server on 127.0.0.1:5020 ...")

    server_task = asyncio.create_task(
        StartAsyncTcpServer(context=context, identity=identity, address=("127.0.0.1", 5020))
    )

    # Wait until asked to stop
    await stop_event.wait()
    print("🧹 Stopping server ...")
    await ServerAsyncStop()
    server_task.cancel()


async def run_client():
    """Run client after confirming server is live."""
    await asyncio.sleep(3)  # wait a bit longer for server startup
    log_path = os.path.join(log_dir, "client_output.txt")

    with open(log_path, "w") as log:
        client = ModbusTcpClient("127.0.0.1", port=5020)
        if not client.connect():
            print("❌ Could not connect to server.", file=log)
            return

        print("✅ Connected to Modbus server.", file=log)

        coils = client.read_coils(0, 10, unit=0)
        if not coils.isError():
            print(f"📡 Coils: {coils.bits[:10]}", file=log)
        else:
            print(f"❌ Coil read failed: {coils}", file=log)

        client.write_coil(0, False, unit=0)
        client.write_coil(1, True, unit=0)

        hr = client.read_holding_registers(0, 10, unit=0)
        if not hr.isError():
            print(f"📗 Holding Registers: {hr.registers[:10]}", file=log)
        else:
            print(f"❌ HR read failed: {hr}", file=log)

        ir = client.read_input_registers(0, 10, unit=0)
        if not ir.isError():
            print(f"📙 Input Registers: {ir.registers[:10]}", file=log)
        else:
            print(f"❌ IR read failed: {ir}", file=log)

        client.close()
        print("🔌 Client disconnected.", file=log)


async def main():
    stop_event = asyncio.Event()
    server = asyncio.create_task(run_server(stop_event))
    await run_client()
    stop_event.set()
    await asyncio.sleep(1)  # allow server to shut down cleanly

    # Summary file
    with open(os.path.join(log_dir, "run_summary.txt"), "w") as f:
        f.write("✅ Modbus workflow completed successfully.\n")
        f.write("Timestamp: " + time.ctime() + "\n")

    print(f"✅ Logs written to: {os.path.abspath(log_dir)}")


if __name__ == "__main__":
    asyncio.run(main())
