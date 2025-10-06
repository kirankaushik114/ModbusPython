#!/usr/bin/env python3
"""
✅ Async Modbus TCP Server (for pymodbus >= 3.6)
Simulates 10 values per data type, supports Unit IDs 0 and 1
"""

import asyncio
import logging
from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import (
    ModbusSlaveContext,
    ModbusServerContext,
    ModbusSequentialDataBlock,
)
from pymodbus.device import ModbusDeviceIdentification

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()
log.setLevel(logging.DEBUG)


async def run_server():
    # --- Create datastore ---
    slave_data = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]),
        co=ModbusSequentialDataBlock(0, [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]),
        hr=ModbusSequentialDataBlock(0, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]),
        ir=ModbusSequentialDataBlock(0, [5, 15, 25, 35, 45, 55, 65, 75, 85, 95]),
        zero_mode=True,
    )

    # --- Accept both Unit IDs 0 and 1 ---
    context = ModbusServerContext(slaves={0: slave_data, 1: slave_data}, single=False)

    identity = ModbusDeviceIdentification()
    identity.VendorName = "GitHub"
    identity.ProductCode = "GH"
    identity.ProductName = "Async Modbus TCP Server"
    identity.MajorMinorRevision = "3.6.8"

    print("🚀 Starting Async Modbus TCP Server on 127.0.0.1:5020 ...")
    print("   Accepting connections for Unit IDs 0 and 1\n")

    await StartAsyncTcpServer(
        context=context,
        identity=identity,
        address=("127.0.0.1", 5020),
    )


if __name__ == "__main__":
    asyncio.run(run_server())
