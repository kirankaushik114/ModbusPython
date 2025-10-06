#!/usr/bin/env python3
"""
✅ Modbus TCP Client
Reads and writes all Modbus data types from the local server.
Compatible with Python 3.10+ and pymodbus 3.6.8
"""

from pymodbus.client import ModbusTcpClient

HOST = "127.0.0.1"
PORT = 5020
UNIT_ID = 0  # can be 0 or 1 — both accepted by the server

client = ModbusTcpClient(HOST, port=PORT)

if client.connect():
    print(f"✅ Connected to Modbus server at {HOST}:{PORT} (Unit ID: {UNIT_ID})\n")

    # --- Read Coils ---
    print("📡 Reading Coils (0–9)...")
    coils = client.read_coils(0, 10, unit=UNIT_ID)
    if coils.isError():
        print(f"❌ Error reading coils: {coils}")
    else:
        for i, bit in enumerate(coils.bits[:10]):
            print(f"   Coil[{i}] = {'ON' if bit else 'OFF'}")

    # --- Write Coils ---
    print("\n✏️ Writing Coil 0 -> OFF, Coil 1 -> ON")
    client.write_coil(0, False, unit=UNIT_ID)
    client.write_coil(1, True, unit=UNIT_ID)

    # --- Verify Coils ---
    print("\n🔄 Reading Updated Coils (0–9)...")
    coils_updated = client.read_coils(0, 10, unit=UNIT_ID)
    if coils_updated.isError():
        print(f"❌ Error reading coils: {coils_updated}")
    else:
        for i, bit in enumerate(coils_updated.bits[:10]):
            print(f"   Coil[{i}] = {'ON' if bit else 'OFF'}")

    # --- Holding Registers ---
    print("\n📗 Reading Holding Registers (0–9)...")
