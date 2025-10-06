*** Settings ***
Documentation     Modbus Automation Suite using Robot Framework
Library           OperatingSystem
Library           Process
Suite Setup       Log To Console    Starting Modbus Automation Suite...
Suite Teardown    Log To Console    Modbus Automation Suite Completed!

*** Variables ***
${CLIENT_SCRIPT}    modbus_client_read_coils.py
${SERVER_SCRIPT}    modbus_server.py
${LOG_DIR}          logs

*** Test Cases ***
Start Modbus Server
    [Documentation]    Starts the Modbus server process.
    Create Directory    ${LOG_DIR}
    Run Process    python    ${SERVER_SCRIPT}    stdout=${LOG_DIR}/server_output.log    stderr=${LOG_DIR}/server_error.log    shell=True
    Sleep    5s
    Log To Console    Modbus server started successfully.

Run Modbus Client
    [Documentation]    Runs the Modbus client to read coils.
    Run Process    python    ${CLIENT_SCRIPT}    stdout=${LOG_DIR}/client_output.log    stderr=${LOG_DIR}/client_error.log    shell=True
    Log To Console    Modbus client executed successfully.

Run Modbus Orchestrator
    [Documentation]    Runs the orchestrator script (run_modbus.py).
    Run Process    python    run_modbus.py    stdout=${LOG_DIR}/run_output.log    stderr=${LOG_DIR}/run_error.log    shell=True
    Log To Console    Orchestrator executed successfully.

Verify Logs Exist
    [Documentation]    Ensures all log files exist after execution.
    Directory Should Exist    ${LOG_DIR}
    File Should Exist         ${LOG_DIR}/server_output.log
    File Should Exist         ${LOG_DIR}/client_output.log
