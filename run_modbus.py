#!/usr/bin/env python3
"""
✅ Reliable Modbus Orchestrator for GitHub Actions
Uses synchronous ModbusTcpServer in a background process so that
the client always gets valid replies.
"""

import os
import time
import multiprocessing
from datetime import datetime
from pymodbus.server.sync import ModbusTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
from pymodbus.client import ModbusTcpClient

# --- log setup ---
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_dir = os.path.join("logs", timestamp)
os.makedirs(log_dir, exist_ok=True)


def run_server():
    """Blocking Modbus server running in its own process."""
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*10),
        co=ModbusSequentialDataBlock(0, [1]*10),
        hr=ModbusSequentialDataBlock(0, list(range(10,110,10))),
        ir=ModbusSequentialDataBlock(0, list(range(5,105,10))),
    )
    context = ModbusServerContext(slaves=store, single=True)
    server = ModbusTcpServer(context, address=("127.0.0.1", 5020), defer_start=False)
    server.serve_forever()


def run_client():
    """Simple client interacting with the server."""
    client_log = os.path.join(log_dir, "client_output.txt")
    with open(client_log, "w") as log:
        c = ModbusTcpClient("127.0.0.1", port=5020)
        if not c.connect():
            print("❌ Could not connect to server.", file=log)
            return
        print("✅ Connected to Modbus server.", file=log)

        coils = c.read_coils(0, 10)
        print(f"📡 Coils: {getattr(coils, 'bits', coils)}", file=log)

        c.write_coil(0, False)
        c.write_coil(1, True)

        hr = c.read_holding_registers(0, 10)
        print(f"📗 Holding Registers: {getattr(hr, 'registers', hr)}", file=log)

        ir = c.read_input_registers(0, 10)
        print(f"📙 Input Registers: {getattr(ir, 'registers', ir)}", file=log)

        c.close()
        print("🔌 Client disconnected.", file=log)


if __name__ == "__main__":
    # --- start server in background process ---
    p = multiprocessing.Process(target=run_server, daemon=True)
    p.start()
    time.sleep(3)        # give server time to start

    # --- run client ---
    run_client()

    # --- stop server ---
    p.terminate()
    p.join(timeout=2)

    with open(os.path.join(log_dir, "run_summary.txt"), "w") as f:
        f.write("✅ Completed successfully at " + time.ctime() + "\n")

    print(f"✅ Logs written to {os.path.abspath(log_dir)}")
