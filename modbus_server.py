#!/usr/bin/env python3
"""
✅ Modbus TCP Server (pymodbus 3.x)
Runs a simple synchronous Modbus TCP server on localhost:5020
Compatible with pymodbus>=3.0 (tested on 3.6.8)
"""

from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification

def run_modbus_server():
    # --- Create a simple data store ---
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0] * 10),                 # Discrete Inputs
        co=ModbusSequentialDataBlock(0, [1] * 10),                 # Coils
        hr=ModbusSequentialDataBlock(0, list(range(10, 110, 10))), # Holding Registers
        ir=ModbusSequentialDataBlock(0, list(range(5, 105, 10))),  # Input Registers
        zero_mode=True,
    )
    context = ModbusServerContext(slaves=store, single=True)

    # --- Server Identity (optional, for diagnostics) ---
    identity = ModbusDeviceIdentification()
    identity.VendorName = "GitHub Automation"
    identity.ProductCode = "MODBUS3X"
    identity.VendorUrl = "https://github.com/"
    identity.ProductName = "Python Modbus Server"
    identity.ModelName = "LocalHost"
    identity.MajorMinorRevision = "3.6.8"

    print("🚀 Starting Modbus TCP Server on 127.0.0.1:5020 ...")
    print("   Holding registers initialized with values 10..100")
    print("   Press Ctrl+C to stop.\n")

    # --- Start the server (blocking) ---
    StartTcpServer(
        context=context,
        identity=identity,
        address=("127.0.0.1", 5020)
    )


if __name__ == "__main__":
    run_modbus_server()
