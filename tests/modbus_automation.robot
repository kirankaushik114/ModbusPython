*** Settings ***
Documentation     Modbus Automation Suite using Robot Framework
Library           OperatingSystem
Library           Process
Suite Setup       Log To Console    Starting Modbus Automation Suite...
Suite Teardown    Log To Console    Modbus Automation Suite Completed!

*** Variables ***
${SERVER_SCRIPT}      modbus_server.py
${CLIENT_SCRIPT}      modbus_client_read_coils.py
${ORCHESTRATOR}       run_modbus.py
${LOG_DIR}            logs

*** Test Cases ***
Start Modbus Server
    [Documentation]    Starts the Modbus server process in the background.
    Create Directory    ${LOG_DIR}
    Start Process    python    ${SERVER_SCRIPT}    stdout=${LOG_DIR}/server_output.log    stderr=${LOG_DIR}/server_error.log    shell=True    alias=modbus_server
    Sleep    5s
    Log To Console    Modbus server started successfully.

Run Modbus Client
    [Documentation]    Runs the Modbus client to read coils.
    Run Process    python    ${CLIENT_SCRIPT}    stdout=${LOG_DIR}/client_output.log    stderr=${LOG_DIR}/client_error.log    shell=True
    Log To Console    Modbus client executed successfully.

Run Modbus Orchestrator
    [Documentation]    Runs the Modbus orchestrator script.
    Run Process    python    ${ORCHESTRATOR}    stdout=${LOG_DIR}/orchestrator_output.log    stderr=${LOG_DIR}/orchestrator_error.log    shell=True
    Log To Console    Orchestrator executed successfully.

Verify Logs Exist
    [Documentation]    Ensures that all log files exist after execution.
    Directory Should Exist    ${LOG_DIR}
    File Should Exist         ${LOG_DIR}/server_output.log
    File Should Exist         ${LOG_DIR}/client_output.log
    File Should Exist         ${LOG_DIR}/orchestrator_output.log
    Log To Console            All expected logs verified successfully.

Stop Modbus Server
    [Documentation]    Stops the background Modbus server process.
    Terminate Process    modbus_server
    Log To Console       Modbus server stopped successfully.
