#!/usr/bin/env python3
"""
✅ Modbus TCP Client (pymodbus 3.x)
Connects to localhost:5020 and interacts with the Modbus server.
Reads coils, holding registers, and input registers.
"""

from pymodbus.client import ModbusTcpClient

HOST = "127.0.0.1"
PORT = 5020

def run_modbus_client():
    client = ModbusTcpClient(HOST, port=PORT)

    if not client.connect():
        print("❌ Could not connect to Modbus server.")
        return

    print(f"✅ Connected to Modbus server at {HOST}:{PORT}\n")

    # --- Read Coils ---
    print("📡 Reading Coils (0–9)...")
    coils = client.read_coils(0, 10)
    if coils.isError():
        print(f"❌ Coil read failed: {coils}")
    else:
        print("✅ Coils:", coils.bits[:10])

    # --- Write Coils ---
    print("\n✏️ Writing Coil 0 -> OFF, Coil 1 -> ON")
    client.write_coil(0, False)
    client.write_coil(1, True)

    # --- Verify Coil Writes ---
    updated_coils = client.read_coils(0, 10)
    if updated_coils.isError():
        print(f"❌ Coil verify failed: {updated_coils}")
    else:
        print("✅ Updated Coils:", updated_coils.bits[:10])

    # --- Read Holding Registers ---
    print("\n📗 Reading Holding Registers (0–9)...")
    hr = client.read_holding_registers(0, 10)
    if hr.isError():
        print(f"❌ HR read failed: {hr}")
    else:
        print("✅ Holding Registers:", hr.registers)

    # --- Read Input Registers ---
    print("\n📙 Reading Input Registers (0–9)...")
    ir = client.read_input_registers(0, 10)
    if ir.isError():
        print(f"❌ IR read failed: {ir}")
    else:
        print("✅ Input Registers:", ir.registers)

    client.close()
    print("\n🔌 Disconnected from Modbus server.")


if __name__ == "__main__":
    run_modbus_client()
