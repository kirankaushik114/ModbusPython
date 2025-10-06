#!/usr/bin/env python3
import requests
import json

def test_echo_json():
    # Step 1: Base URL
    base_url = "https://httpbin.org"

    # Step 2: Payload
    payload = {"name": "robot", "value": "framework"}

    print("=== Payload being sent ===")
    print(json.dumps(payload, indent=4))

    # Step 3: Send POST request
    url = f"{base_url}/post"
    response = requests.post(url, json=payload, verify=True)

    # Step 4: Print response info
    print("\n=== Response Info ===")
    print(f"Status Code: {response.status_code}")
    print(f"URL: {response.url}")
    print(f"Reason: {response.reason}")

    # Step 5: Parse and print JSON response
    response_json = response.json()
    #print(f"Check: {response_json}")

    print("\n=== Full Response JSON ===")
    print(json.dumps(response_json, indent=4))

    # Step 6: Extract echoed data
    print("\n=== Extract echoed data ===")
    echoed_name = response_json['json']['name']
    echoed_value = response_json['json']['value']

    print("\n=== Extracted Data from Response ===")
    print(f"name: {echoed_name}")
    print(f"value: {echoed_value}")

    # Step 7: Simple verification
    print("\n=== Simple verification ===")
    assert echoed_name == "robot"
    assert echoed_value == "framework"

    print("\n✅ Test passed! The server echoed the correct JSON values.")

# ✅ Add this at the bottom so your function runs automatically:
if __name__ == "__main__":
    test_echo_json()
